# Melody Killa Enhance

A piano roll script for **FL Studio 21+** that conjures new melodies.
Write anything – even just a rhythm on a single note – and turn the **Magic**
knob until you hear a melody you like. Fine-tune it with the other knobs,
hit **Accept** and keep editing as usual.

## Installation

1. Copy `Melody Killa Enhance.pyscript` to
   `Documents\Image-Line\FL Studio\Settings\Piano roll scripts\`
   (Mac: `Documents/Image-Line/FL Studio/Settings/Piano roll scripts/`)
2. Restart FL Studio.
3. In the piano roll: **Tools (wrench) → Scripting → Melody Killa Enhance**

## Knobs

| Knob | What it does |
|---|---|
| **Magic** | Every number = a new melody. Same number = same result, so you can always go back to one you liked. |
| **Magic amount** | How much the melody changes. Low = stays close to your melody, full = completely new. |
| **Range** | Small steps ↔ big leaps (up to an octave). |
| **Rhythm** | Left = long sustained notes, right = chopped into short hits, 0 = your rhythm. |
| **Ornaments** | Triplet runs, rolls and grace notes. |
| **Bounce** | Accents on the beats and livelier velocity. |
| **Harmony** | Second voice: third above / fifth below / octave below. |
| **Key, Scale** | `Auto` = detected from your melody. Everything on C5 gives C minor. |

The tuning knobs (Range, Rhythm, Ornaments, Bounce, Harmony) never change the
magic itself – you can polish a melody you like without losing it.

- If you select only some notes, only those are changed.
- All knobs at 0 = the original melody.
- Made for monophonic melodies – overlapping notes get shortened.

## How the magic works

1. **Pitches** – a random walk on the scale around the register of your melody,
   chord tones on strong beats, ending on the tonic. The second bar starts like
   the first and ends differently (call and response).
2. **Rhythm** – chops or merges notes.
3. **Ornaments, bounce, harmony.**

## Troubleshooting

- **Script not in the menu:** check the file ends with `.pyscript` (not `.txt`)
  and is in the right folder, then restart FL Studio.
- **Script shows an error:** open **View → Script output** and copy the error text.

## Tests

Outside FL Studio the script is tested against a `flpianoroll` mock in `tests/`:

```
python3 -m unittest discover -s tests
```
