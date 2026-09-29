import importlib.machinery
import importlib.util
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import flpianoroll as flp  # noqa: E402  (mock)

SCRIPT = os.path.join(HERE, '..', 'Melody Killa Enhance.pyscript')
loader = importlib.machinery.SourceFileLoader('mke', SCRIPT)
spec = importlib.util.spec_from_loader('mke', loader)
mke = importlib.util.module_from_spec(spec)
loader.exec_module(mke)

PPQ = flp.Score.PPQ
# A minor melody: A C E D C A G A (quarter notes)
MELODY = [57, 60, 64, 62, 60, 57, 55, 57]


def load(pitches=MELODY, length=PPQ, selected=None):
    flp.score.clear()
    for i, p in enumerate(pitches):
        n = flp.Note()
        n.number, n.time, n.length = p, i * PPQ, length
        n.selected = bool(selected and i in selected)
        flp.score.addNote(n)


def run(**vals):
    form = mke.createDialog()
    form.values.update({k.replace('_', ' '): v for k, v in vals.items()})
    mke.apply(form)
    return sorted(((n.time, n.number, n.length, round(n.velocity, 4))
                   for n in flp.score.notes))


ZERO = dict(Magic_amount=0.0, Groove=1, Chords=0, Rhythm=0.0, Ornaments=0.0,
            Bounce=0.0, Harmony=0)
ALL_C5 = [72] * 8


def snap():
    return sorted((n.time, n.number, n.length, round(n.velocity, 4))
                  for n in flp.score.notes)


def pitches_of(notes):
    return [p for _, p, _, _ in notes]


class EnhanceTest(unittest.TestCase):
    def test_all_zero_is_original(self):
        load()
        orig = sorted((n.time, n.number, n.length, round(n.velocity, 4))
                      for n in flp.score.notes)
        self.assertEqual(run(**ZERO), orig)

    def test_deterministic(self):
        load(); a = run(Magic=7)
        load(); b = run(Magic=7)
        load(); c = run(Magic=8)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_monotone_input_becomes_melody(self):
        counts = []
        for seed in range(1, 30):
            load(ALL_C5)
            notes = run(Magic=seed, Ornaments=0.0)
            counts.append(len(set(pitches_of(notes))))
        self.assertGreaterEqual(min(counts), 2)
        self.assertGreaterEqual(sum(counts) / len(counts), 3)

    def test_valid_output_all_knobs(self):
        for seed in range(1, 25):
            for rh in (-1.0, -0.4, 0.0, 0.5, 1.0):
                for pitches in (MELODY, ALL_C5):
                    load(pitches)
                    notes = run(Magic=seed, Rhythm=rh, Range=seed % 5 / 4.0,
                                Ornaments=1.0, Bounce=1.0, Harmony=seed % 4)
                    self.assertTrue(notes)
                    for t, p, L, vel in notes:
                        self.assertGreaterEqual(t, 0)
                        self.assertTrue(0 <= p <= 127)
                        self.assertGreaterEqual(L, 1)
                        self.assertTrue(0 < vel <= 1.0)

    def test_melody_is_mono_without_harmony(self):
        for seed in range(1, 30):
            load()
            notes = run(Magic=seed, Ornaments=1.0, Rhythm=0.6)
            for (t1, _, L1, _), (t2, _, _, _) in zip(notes, notes[1:]):
                if t2 > t1:
                    self.assertLessEqual(t1 + L1, t2)

    def test_notes_in_fixed_key(self):
        pcs = {(9 + i) % 12 for i in mke.SCALES['Natural Minor']}
        for seed in range(1, 30):
            load(ALL_C5)
            notes = run(Magic=seed, Ornaments=1.0, Rhythm=0.8,
                        Key=10, Scale=1)
            for p in pitches_of(notes):
                self.assertIn(p % 12, pcs)

    def test_rhythm_knob(self):
        load(); base = run(Magic=3, Ornaments=0.0)
        load(); chop = run(Magic=3, Ornaments=0.0, Rhythm=1.0)
        load(); long_ = run(Magic=3, Ornaments=0.0, Rhythm=-1.0)
        self.assertGreater(len(chop), len(base))
        self.assertLess(len(long_), len(base))

    def test_polish_keeps_magic(self):
        # Bounce/Harmony must not change the generated pitches
        load(); a = run(Magic=11, Ornaments=0.0, Bounce=0.0)
        load(); b = run(Magic=11, Ornaments=0.0, Bounce=1.0)
        self.assertEqual([(t, p) for t, p, _, _ in a], [(t, p) for t, p, _, _ in b])

    def test_only_selection_changes(self):
        load(selected={0, 1, 2})
        run(Magic=3, Rhythm=1.0)
        untouched = [(n.time, n.number) for n in flp.score.notes if not n.selected]
        self.assertEqual(sorted(untouched),
                         [(i * PPQ, p) for i, p in enumerate(MELODY)][3:])

    def test_detect_key(self):
        load()
        src = [mke.snapshot(n) for n in flp.score.notes]
        self.assertEqual(mke.detect_key(src), (9, 'Natural Minor'))
        self.assertEqual(mke.detect_key(src, roots=[9])[0], 9)
        self.assertEqual(mke.detect_key(src, scales=['Major'])[1], 'Major')

    def test_regenerate_gives_new_melody(self):
        load(ALL_C5)
        form = mke.createDialog()
        mke.apply(form)
        first = snap()
        seen = {tuple(first)}
        for _ in range(4):
            load(ALL_C5)
            mke.apply(form)  # same knobs again = Regenerate
            seen.add(tuple(snap()))
        self.assertGreaterEqual(len(seen), 4)

    def test_tuning_after_regenerate_keeps_melody(self):
        load(ALL_C5)
        form = mke.createDialog()
        form.values['Ornaments'] = 0.0
        mke.apply(form)
        load(ALL_C5)
        mke.apply(form)  # Regenerate
        regen = [(t, p) for t, p, _, _ in snap()]
        load(ALL_C5)
        form.values['Bounce'] = 1.0  # tune a knob
        mke.apply(form)
        self.assertEqual([(t, p) for t, p, _, _ in snap()], regen)

    def test_magic_numbers_stay_reproducible(self):
        load(); form = mke.createDialog(); form.values['Magic'] = 5
        mke.apply(form); a = snap()
        load(); mke.apply(form)  # Regenerate
        load(); form.values['Magic'] = 6; mke.apply(form)
        load(); form.values['Magic'] = 5; mke.apply(form)
        self.assertEqual(snap(), a)

    def test_trap_groove_is_syncopated_and_sparse(self):
        q = PPQ // 4
        for seed in range(1, 30):
            load(ALL_C5)
            notes = run(Magic=seed, Ornaments=0.0)
            for t, _, _, _ in notes:
                self.assertEqual(t % q, 0)           # on the 16th grid
            self.assertLessEqual(len(notes), 12)     # 2 bars, sparse
            self.assertLessEqual(max(t + L for t, _, L, _ in notes), 8 * PPQ)

    def test_keep_mine_keeps_rhythm(self):
        load()
        notes = run(Magic=4, Groove=1, Ornaments=0.0)
        self.assertEqual([t for t, _, _, _ in notes], [i * PPQ for i in range(8)])

    def test_chords_under_melody(self):
        for seed in range(1, 20):
            load(ALL_C5)
            mel = run(Magic=seed, Ornaments=0.0)
            load(ALL_C5)
            full = run(Magic=seed, Ornaments=0.0, Chords=2)
            extra = sorted(set(full) - set(mel))
            self.assertTrue(extra)
            self.assertLess(max(p for _, p, _, _ in extra),
                            min(p for _, p, _, _ in mel))
            self.assertLessEqual(max(t + L for t, _, L, _ in full), 8 * PPQ)

    def test_harmony_adds_notes(self):
        load(); plain = run(Magic=5)
        load(); harm = run(Magic=5, Harmony=3)
        self.assertGreater(len(harm), len(plain))


if __name__ == '__main__':
    unittest.main()
