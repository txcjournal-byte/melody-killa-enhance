# Melody Killa Enhance

A piano roll script for **FL Studio 21+** that turns your notes into **trap melodies**.
Write anything – even just a few notes on C5 – and turn the **Magic** knob or press
**Regenerate** until you hear a melody you like. Add chords and bass with one click,
fine-tune it with the other knobs, hit **Accept** and keep editing as usual.

## Installation

1. Copy `Melody Killa Enhance.pyscript` to
   `Documents\Image-Line\FL Studio\Settings\Piano roll scripts\`
   (Mac: `Documents/Image-Line/FL Studio/Settings/Piano roll scripts/`)
2. Restart FL Studio.
3. In the piano roll: **Tools (wrench) → Scripting → Melody Killa Enhance**

## Knobs

| Knob | What it does |
|---|---|
| **Magic** | Every number = a new trap melody. Same number = same result, so you can always go back to one you liked. |
| **Regenerate** (button) | Another new melody on the same Magic number – just keep pressing until you like it. |
| **Magic amount** | How much the melody changes. Low = stays close to your notes, full = completely new. |
| **Groove** | `Trap` = new sparse, syncopated trap rhythm (keeps how busy your melody was). `Keep mine` = your rhythm. |
| **Chords** | `Chords` = a trap chord progression under the melody, `Chords + bass` = plus a bass note. |
| **Range** | Small steps ↔ big leaps (up to an octave). |
| **Rhythm** | Left = long sustained notes, right = chopped into short hits, 0 = as is. |
| **Ornaments** | Triplet runs, rolls and grace notes. |
| **Bounce** | Accents on the beats and livelier velocity. |
| **Harmony** | Second voice: third above / fifth below / octave below. |
| **Key, Scale** | `Auto` = detected from your notes. Everything on C5 gives C minor. |

The tuning knobs (Range, Rhythm, Ornaments, Bounce, Harmony, Chords) never change the
magic itself – you can polish a melody you like without losing it.

- If you select only some notes, only those are changed.
- Magic amount 0 + Groove `Keep mine` + everything else off = the original melody.
- Made for monophonic melodies – overlapping notes get shortened.

## How the magic works

The rules come from studying how trap melody loops are built:

1. **Chord progression** – one of the common minor trap progressions
   (i–VI–III–VII, i–iv–VI–v, i–VI–iv–v …), one chord per bar (two for short loops).
2. **Groove** – sparse, syncopated rhythm on the 16th grid (hits on 1, the "and" of 2, 4 …),
   long notes, 2-bar phrases where the last bar is a calmer ending.
3. **Pitches** – leaps along the chord (3rds, 5ths, octaves) mostly up, steps mostly
   down, chord tones on strong beats, no more than two same notes in a row.
   The second bar starts like the first and ends differently (call and response).
4. **Rhythm, ornaments, bounce, harmony, chords.**

## Troubleshooting

- **Script not in the menu:** check the file ends with `.pyscript` (not `.txt`)
  and is in the right folder, then restart FL Studio.
- **Script shows an error:** open **View → Script output** and copy the error text.

## Tests

Outside FL Studio the script is tested against a `flpianoroll` mock in `tests/`:

```
python3 -m unittest discover -s tests
```
