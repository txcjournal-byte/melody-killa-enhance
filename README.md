# Melody Killa Enhance

Piano roll skript pro **FL Studio 21+**, který kouzlí nové melodie.
Napíšeš cokoliv – klidně jen rytmus na jednom tónu – a točíš knobem **Kouzlo**,
dokud neuslyšíš melodii, která se ti líbí. Pak ji ostatními knoby doladíš,
dáš **Accept** a dál normálně edituješ.

## Instalace

1. Zkopíruj `Melody Killa Enhance.pyscript` do
   `Dokumenty\Image-Line\FL Studio\Settings\Piano roll scripts\`
2. V piano rollu: **Tools (klíč) → Scripting → Melody Killa Enhance**

## Knoby

| Knob | Co dělá |
|---|---|
| **Kouzlo** | Každé číslo = nová melodie. Stejné číslo = stejný výsledek, takže se k oblíbené vrátíš. |
| **Síla kouzla** | Jak moc se melodie změní. Nízko = drží se tvé melodie, naplno = úplně nová. |
| **Rozsah** | Malé kroky ↔ velké skoky (i o oktávu). |
| **Rytmus** | Doleva = dlouhé znějící tóny, doprava = rozsekání na malé kostičky, 0 = tvůj rytmus. |
| **Ozdoby** | Triolové běhy, rolly a grace noty. |
| **Bounce** | Akcenty na doby a živější velocity. |
| **Harmonie** | Druhý hlas: tercie nad / kvinta pod / oktáva pod. |
| **Tónina, Stupnice** | `Auto` = zjistí se z melodie. Když napíšeš vše na C5, vyjde C moll. |

Ladicí knoby (Rozsah, Rytmus, Ozdoby, Bounce, Harmonie) nemění samotné kouzlo –
melodii, která se ti líbí, můžeš dolaďovat, aniž by zmizela.

- Když označíš jen část not, kouzlí se jen s nimi.
- Všechny knoby na 0 = původní melodie.
- Určeno pro jednohlasou melodii – překrývající se noty se zkrátí.

## Jak kouzlo funguje

1. **Tóny** – náhodná procházka po stupnici kolem polohy tvé melodie, na silných
   dobách tóny akordu, konec na tónice. Druhý takt začne jako první a skončí jinak
   (otázka / odpověď).
2. **Rytmus** – rozsekání nebo spojení not.
3. **Ozdoby, bounce, harmonie.**

## Testy

Mimo FL Studio se skript testuje proti mocku `flpianoroll` v `tests/`:

```
python3 -m unittest discover -s tests
```
