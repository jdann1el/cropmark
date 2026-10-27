# Cropmark brief — Taller Barro (fictitious ceramics studio)

Fill the fixed sections before drawing a direction. Keep copy verbatim and separate sourced facts from creative language. Use `none` where a fact or asset is absent.

## 1. Job

- Format: carousel 3×1080×1350
- Platform: Instagram feed
- Language: Spanish
- Number of pieces: 1 carousel, 3 slides
- A/B wanted? no

## 2. Copy given, verbatim

- Title: TALLER BARRO
- Headline: La forma / toma cuerpo.; Del giro / nace el borde.; Cada huella / deja memoria.
- Supporting copy: Una pieza empieza con un gesto.; El torno acompaña cada movimiento.; Un rastro queda en la superficie.
- CTA: EXPLORA EL TALLER; SIGUE EL PROCESO; MIRA LAS PIEZAS
- Word-cap reference: Cropmark SKILL.md non-negotiable 2.

## 3. Facts allowed

None. This is a fictitious studio and sample creative copy; do not invent prices, provenance, firing method, durability, inventory, or performance claims.

## 4. Assets that really exist

None. Draw the pottery forms, wheel, clay surface, and marks in code. Use bundled OFL fonts only; no reference pixels.

## 5. Brand locks

- Fixed colours: none
- Fixed fonts: none
- Other identity constraints: invented name only; no real studio identity
- Keep in draw: none

```yaml
colors: []
typography: []
```

## 6. Subject inventory (8–12 items)

Illustrative subject nouns only; they do not assert anything about a real studio or product.

1. Coiled clay ribbon
2. Potter's wheel and circular motion
3. Vessel lip and wall
4. Thumbprint in soft clay
5. Rib tool and its curved edge
6. Foot ring under a vessel
7. Slip trail on a surface
8. Incised line in clay
9. Small trimming curls
10. Glaze pool as a colour patch

## 7. Anti-references

- Nearest real competitor/feed, if known: none supplied
- What this piece must not resemble: a wellness post, generic beige craft template, catalog grid, or an ungrounded clay-colour blob

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format carousel --brief "skills/cropmark/briefs/example-taller-barro.md" --options 3
```

- Seed and three dealt options: 20261023; `artefact-in-scene`, `duel`, `type-is-the-image`
- Chosen direction and one-line reason naming its inventory item: `artefact-in-scene` / `text-in-scene`; the coiled clay ribbon can become the vessel lip that carries and crosses the headline.
- Redraws and reasons, if any: R1 redujo el cruce de la cinta y quitó marcas del torno detrás del bloque tipográfico; R2 corrigió el cuello de la vasija y despejó la huella/los apoyos respecto del copy. Dos rondas de composición, no de textura.

## 9. Idea sentence + competitor test

“In this piece, **the coiled clay ribbon** becomes **a physical line that shapes the vessel and carries the headline**.” It belongs to a ceramics studio; if it still fits a generic café, replace the clay gesture.

## 10. Concept (3 lines)

- Idea: a vessel's rim and body are the stage for words about form and movement
- What the image shows without reading: clay rises from a turning coil into a bowl; its rim crosses the low edge of the final headline line
- Style card selected from the direction: `text-in-scene`; interpreted as type on the vessel itself, not as a flat added panel.

## 11. Hooks / variants

1. A clay rim carries and barely occludes the last line of the cover headline.
2. A turning coil curves through the headline measure and ends at a vessel lip.
3. A thumbprint sits within the negative space around the closing line.
- Selected hook: a clay vessel's rim crosses only the bottom edge of the final cover line.
- For A/B, describe the different hook type or direction for each variant; do not use seed rerolls as variants.

## 12. Carousel page plan (carousels only)

| Slide | Role | Hook | Image source | Layout intent |
|---|---|---|---|---|
| 01 | Cover | La forma / toma cuerpo. | Code-drawn vessel | Words sit on the body; the lip crosses only a small lower portion of “toma cuerpo.” |
| 02 | Process | Del giro / nace el borde. | Code-drawn wheel and clay coil | Coil follows the circular motion and helps carry the headline. |
| 03 | Close | Cada huella / deja memoria. | Code-drawn clay surface | A thumbprint sits beside the phrase; CTA closes the sequence. |

- Set-continuity device: one continuous clay coil/rim mark and a shared serif/sans type system

## 13. Log (fill at delivery)

- Direction sheet path and seed: evals/art-direction/diagnostic-2026-10-22/renders/step6b/direction.md; deal seed 20261023; choice recorded as `artefact-in-scene` / `text-in-scene`
- Reference IDs consulted; local images viewed?: `bh11-estudio-mona` 11-02 and `bh19-kings-cafe` 19-06; both inspected at feed size as local read-only references
- Rubric scores: not used as approval evidence
- Fixes made: R0→R1 reduced the ink cover and cleared wheel marks from the copy; R1→R2 reshaped the vessel neck and cleared the closing impression/support from the headline/object edges. The 360 px feed review reads all three full phrases.
- Images used and their sources: code-drawn shapes and bundled OFL fonts only
