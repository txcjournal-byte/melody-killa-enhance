# Melody Killa Enhance

Piano roll skript pro **FL Studio 21+**, který z obyčejné melodie udělá trapový lead:
triolové běhy, rolly, grace noty, oktávové skoky, call & response, harmonie a bounce.

## Instalace

1. Zkopíruj `Melody Killa Enhance.pyscript` do
   `Dokumenty\Image-Line\FL Studio\Settings\Piano roll scripts\`
2. V piano rollu: **Tools (klíč) → Scripting → Melody Killa Enhance**

## Použití

- Napiš jednoduchou melodii (jednohlasou). Když označíš jen část not, upraví se jen ty.
- **Varianta** – nová verze. Stejné číslo = stejný výsledek.
- **Síla** – celková míra úprav. 0 = původní melodie beze změny.

| Ovladač | Co dělá |
|---|---|
| Styl | Trap Bounce / Dark (skoky dolů, víc grace not) / Crazy (víc všeho, rolly po 1/32) |
| Tónina, Stupnice | `Auto` = zjistí se z melodie. Jde nastavit jen jedno a druhé nechat na Auto. |
| Triolové běhy | 1/16 triolový běh na konci noty, který vede do další noty |
| Rolly | opakování noty na jejím začátku |
| Grace noty | krátká nota (1/32) ze sousedního stupně těsně před notou |
| Oktávové skoky | posun noty o oktávu (hlavně v druhé půlce) |
| Call & Response | druhá půlka („odpověď“) je výraznější a končí jinak |
| Harmonie | druhý hlas: tercie nad / kvinta pod / oktáva pod |
| Bounce | akcenty na doby + lehká humanizace velocity |

## Testy

Mimo FL Studio se skript testuje proti mocku `flpianoroll` v `tests/`:

```
python3 -m unittest discover -s tests
```
