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
# A moll melodie: A C E D C A G A (ctvrtky)
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
    form.values.update(vals)
    mke.apply(form)
    return sorted(((n.time, n.number, n.length, round(n.velocity, 4))
                   for n in flp.score.notes))


class EnhanceTest(unittest.TestCase):
    def test_zero_strength_is_original(self):
        load()
        before = run(Sila=0.0)
        load()
        orig = sorted((n.time, n.number, n.length, round(n.velocity, 4))
                      for n in flp.score.notes)
        self.assertEqual(before, orig)

    def test_zero_strength_ignores_harmony(self):
        load()
        self.assertEqual(len(run(Sila=0.0, Harmonie=3)), len(MELODY))

    def test_deterministic_variant(self):
        load(); a = run(Varianta=7, Sila=1.0)
        load(); b = run(Varianta=7, Sila=1.0)
        load(); c = run(Varianta=8, Sila=1.0)
        self.assertEqual(a, b)
        self.assertNotEqual(a, c)

    def test_all_styles_valid_output(self):
        for style in range(len(mke.STYLES)):
            for v in range(1, 40):
                load()
                notes = run(Styl=style, Varianta=v, Sila=1.0, Harmonie=v % 4)
                self.assertTrue(notes)
                for t, p, L, vel in notes:
                    self.assertGreaterEqual(t, 0)
                    self.assertTrue(0 <= p <= 127)
                    self.assertGreaterEqual(L, 1)
                    self.assertTrue(0 < vel <= 1.0)

    def test_melody_is_mono_without_harmony(self):
        for v in range(1, 40):
            load()
            notes = run(Varianta=v, Sila=1.0, Harmonie=0)
            for (t1, _, L1, _), (t2, _, _, _) in zip(notes, notes[1:]):
                if t2 > t1:
                    self.assertLessEqual(t1 + L1, t2)

    def test_generated_notes_in_scale(self):
        pcs = {(9 + i) % 12 for i in mke.SCALES['Natural Minor']}
        for v in range(1, 30):
            load()
            # A + Natural Minor pevne, bez oktav (ty jen posouvaji original)
            notes = run(Varianta=v, Sila=1.0, Tonina=10, Stupnice=1)
            for _, p, _, _ in notes:
                self.assertIn(p % 12, pcs)

    def test_only_selection_changes(self):
        load(selected={0, 1, 2})
        run(Sila=1.0, Varianta=3, Rolly=1.0, **{'Oktavove skoky': 0.0})
        untouched = [(n.time, n.number) for n in flp.score.notes if not n.selected]
        self.assertEqual(sorted(untouched),
                         [(i * PPQ, p) for i, p in enumerate(MELODY)][3:])

    def test_detect_key(self):
        load()
        src = [mke.snapshot(n) for n in flp.score.notes]
        self.assertEqual(mke.detect_key(src), (9, 'Natural Minor'))
        # pevna tonina, auto stupnice
        self.assertEqual(mke.detect_key(src, roots=[9])[0], 9)
        # auto tonina, pevna stupnice
        self.assertEqual(mke.detect_key(src, scales=['Major'])[1], 'Major')

    def test_harmony_adds_notes(self):
        load(); plain = run(Varianta=5, Sila=1.0)
        load(); harm = run(Varianta=5, Sila=1.0, Harmonie=3)
        self.assertGreater(len(harm), len(plain))


if __name__ == '__main__':
    unittest.main()
