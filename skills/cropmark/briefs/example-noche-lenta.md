# Cropmark brief — NOCHE LENTA

Paso 4 del diagnóstico. Cuenta ficticia de descanso; el carrusel prueba si la biblioteca ayuda a encontrar una idea visual específica sin recurrir a fotografía.

## 1. Job

- Format: carousel, 3 × 1080×1350
- Platform: Instagram feed
- Language: Spanish
- Number of pieces: one three-slide set (cover, inner, close)
- A/B wanted? no

## 2. Copy given, verbatim

- Title: NOCHE LENTA
- Headline, cover: «Baja el día.»
- Headline, inner: «Prueba una rutina sencilla para darle sitio al descanso.»
- Headline, close: «Suelta por hoy.»
- Supporting copy, cover: «Una pausa suave al final de la tarde.»
- Supporting copy, inner: «Deja una cosa lista para mañana; después, apaga lo que te distrae.»
- Supporting copy, close: «Elige un gesto sencillo para marcar el cierre.»
- CTA, cover: «SIGUE LEYENDO»
- CTA, inner: «PRUEBA ESTA NOCHE»
- CTA, close: «GUARDA ESTA PAUSA»
- Word-cap reference: Cropmark SKILL.md non-negotiable 2.

## 3. Facts allowed

- NOCHE LENTA is a fictional account for this design study.
- The copy is general, creative language. No health, sleep-outcome, or performance claims; no statistics or external facts.

## 4. Assets that really exist

- No photographic images, logo, brand assets, screenshots, or client-supplied files.
- Pillow drawing code and bundled SIL Open Font License fonts are available for original shapes and illustration.
- `--have`: none. Fonts and code drawing are production tools, not supplied image assets.

## 5. Brand locks

- Fixed colours: carry the study palette `#203331`, `#f5efde`, `#d9c893` for comparison continuity.
- Fixed fonts: bundled DM Serif Display and Outfit.
- Other identity constraints: retain the fictitious name NOCHE LENTA; do not imply medical advice.
- Keep in draw: palette,type

```yaml
colors: ["#203331", "#f5efde", "#d9c893"]
typography: ["DM Serif Display", "Outfit"]
```

## 6. Subject inventory (8–12 items)

These are visual prompts for a fictional study, not externally verified facts.

1. The name NOCHE LENTA.
2. The phrase «Baja el día».
3. A last strip of daylight held by a roller blind.
4. The blind's weighted bottom rail.
5. The pull cord that lowers the blind.
6. A bedside lamp and its switch.
7. A closed notebook for one item left for tomorrow.
8. A short note marked «mañana».
9. The act of turning off a distraction.
10. The phrase «Suelta por hoy».
11. A small end-of-day ritual.
12. The shift from the last daylight to a quiet evening.

## 7. Anti-references

- Nearest real competitor/feed, if known: a generic sleep-habits carousel; no specific competitor was supplied.
- Avoid the Paso 3 arrangement of a headline beside or just touching a notebook/list. The image/object must carry part of the words or physically occlude them with a readable purpose. Avoid a generic card pretending to be an object, a second headline made from background type, tangencies, edge-stretched short lines, and empty lower space.

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format carousel --brief skills/cropmark/briefs/example-noche-lenta.md --have none --keep palette,type --seed 4407 --options 3
```

- Seed 4407; options: `duel`, `artefact-in-scene`, `across-the-swipe`.
- Chosen direction: `artefact-in-scene` — the last strip of light held by the roller blind (inventory item 3) becomes the fabric carrying the headline; its lower rail descends over the light through the sequence.
- Redraws and reasons: none planned.

## 9. Idea sentence + competitor test

“En esta pieza, **la última franja de luz retenida por la persiana** se convierte en **la tela que lleva «Baja el día» y las frases de la secuencia mientras el riel desciende**; frente a la alternativa más cercana del Paso 3 —libreta/lista que solo completa o queda bajo el titular—, ¿seguiría funcionando?” No: la libreta/lista no puede retener esa franja de luz ni ser el soporte textil que baja sobre ella. The same blind idea could suit another rest account, so its specificity comes from the exact supplied copy and inventory item, not unique brand assets. The nearest reference visual is the Paso 3 B notebook/list; no external competitor was studied.

## 10. Concept (3 lines)

- Idea: a roller blind is the typesetting surface; across the set, its lower rail descends and closes the last line of light.
- What the image shows without reading: an illustrated roller blind being lowered from cover to close, with its cord and bottom rail visible.
- Style card selected from the direction: `text-in-scene`.

## 11. Hooks / variants

1. «Baja el día.»
2. «Prueba una rutina sencilla para darle sitio al descanso.»
3. «Suelta por hoy.»
- Selected hook: the three supplied lines in cover/inner/close sequence.
- A/B: not requested.

## 12. Carousel page plan (carousels only)

| Slide | Role | Hook | Image source | Layout intent |
|---|---|---|---|---|
| 01 | Cover | Baja el día. | Original vector shapes only | Introduce the shared visual device and open the sequence. |
| 02 | Inner | Prueba una rutina sencilla para darle sitio al descanso. | Original vector shapes only | Show the ritual step with the same device carrying or interacting with the words. |
| 03 | Close | Suelta por hoy. | Original vector shapes only | Resolve the visual action and close the sequence. |

- Set-continuity device: the same illustrated roller blind, woven headline placement, cord and descending lower rail; the last light narrows across the sequence.

## 13. Log (fill at delivery)

- Direction sheet path and seed: `.cropmark/direction.json` (local draw record); 4407. Reproducible brief path: this file.
- Reference IDs consulted; local images viewed?: text cards and project page URLs only; no local images viewed or used.
- Rubric scores: no calibrated numeric score; no comparable external artwork was inspected. See the Paso 4 review in docs/diagnostic-2026-10-22-typographic-carousel.md.
- Fixes made: R1 cord x=953→918; R2 added a woven texture and stitched hem; R3 removed the notebook-like horizontal texture, retaining the stitched hem. Full cause/prediction/observation log is in the Paso 4 review.
- Images used and their sources: none; all imagery is drawn in code.
