# Cropmark brief — Taller Barro B3 (fictitious ceramics studio)

Preparation brief for a fictional test. Preserve every supplied string exactly. `/` in a headline indicates its line break and is not printed.

## 1. Job

- Format: carousel 3×1080×1350
- Platform: Instagram feed
- Language: Spanish
- Number of pieces: 1 carousel, 3 slides
- A/B wanted? no; B3 is a single third carousel condition for comparison with preserved A and B2 files.

## 2. Copy given, verbatim

- Title / mark on all slides: `TALLER BARRO`
- Descriptor on all slides: `CERÁMICA`
- Headline by slide: `La forma / toma cuerpo.`; `Del giro / nace el borde.`; `Cada huella / deja memoria.`
- Supporting copy by slide: `Una pieza empieza con un gesto.`; `El torno acompaña cada movimiento.`; `Un rastro queda en la superficie.`
- CTA by slide: `EXPLORA EL TALLER`; `SIGUE EL PROCESO`; `MIRA LAS PIEZAS`
- Copy treatment: preserve all three exact strings. Only final-slide `MIRA LAS PIEZAS` receives CTA treatment; `EXPLORA EL TALLER` and `SIGUE EL PROCESO` remain plain integrated text, with no button or pill styling.
- Word-cap reference: Cropmark SKILL.md non-negotiable 2.

## 3. Facts allowed

None. Taller Barro is fictional. These are sample creative lines; add no prices, provenance, process claims beyond the supplied copy, durability, inventory, or performance claims.

## 4. Assets that really exist

No supplied image asset. Use `gen-image` for three generated conceptual photographic bases: a pottery form, a potter's wheel with clay, and a clay surface/mark. Each base must contain no text, letters, typography, logo, watermark, or legible marks. Add all exact copy, including `TALLER BARRO` and `CERÁMICA`, as controllable Cropmark code overlays in bundled OFL fonts. Do not use reference pixels.

## 5. Brand locks

- Fixed colours: none
- Fixed fonts: none; use bundled OFL fonts and record the actual files later
- Other identity constraints: fictional studio name only; no real studio identity
- Keep in draw: none

```yaml
colors: []
typography: []
```

## 6. Subject inventory (8–12 items)

Illustrative nouns only; these do not assert facts about a real studio.

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
- What this piece must not resemble: a wellness post, generic beige craft template, catalog grid, or ungrounded clay-colour blob

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format carousel --brief evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/brief-taller-barro-copy.md --have gen-image --seed 20261024 --options 3
```

- Seed and three dealt options: `20261024`; `duel`, `frame-system`, `artefact-in-scene`. The deal noted that fewer than three fresh directions remained and recent picks were allowed to fill the deal; see `dealt-options.json`.
- Chosen direction and one-line reason naming its inventory item: `frame-system` / `cinematic-editorial`; the wheel and clay spiral make a repeatable system possible while crop, headline scale/position, and image/type relation vary by ceramic stage; only `MIRA LAS PIEZAS` receives CTA treatment, while the first two strings stay integrated text.
- Redraws and reasons, if any: none before generation.

## 9. Idea sentence + competitor test

“In this piece, **the coiled clay ribbon** becomes **a material line that shapes a vessel beside the headline**.” It belongs to a ceramics studio; if it still fits a generic café, replace the clay gesture.

## 10. Concept (3 lines)

- Idea: the sequence moves from a vessel taking form, through the turning action, to a mark left in clay.
- What the image shows without reading: a recognizable vessel, wheel-and-clay movement, then a close clay trace; the image/headline relationship changes across the sequence.
- Style card selected from the direction: `cinematic-editorial` (`frame-system`).

## 11. Hooks / variants

1. A vessel lip echoes the cover headline's rising form, with clear separation from every glyph.
2. The wheel's circular motion crosses behind the interior headline as a directional arc, clear of copy and key wheel/clay detail.
3. A thumbprint or incised clay trace sits beside the closing headline as a visible material echo.
- Selected hook: shape → turn → trace with vessel-rim echo on cover, wheel-arc relation on process, and thumbprint beside headline on close. Vary headline scale/position, crop, and image/headline relation; keep all copy and key details clear.
- For A/B, describe different hook types or directions for each variant; not applicable to this single B3 condition.

## 12. Carousel page plan

| Slide | Role | Hook | Image source | Layout intent |
|---|---|---|---|---|
| 01 | Cover | `La forma / toma cuerpo.` | Existing generated conceptual pottery base, text-free; use a tall medium crop with vessel to the left | Establish shape with the vessel lip echoing the headline's rising silhouette across a clean gap. Headline is the largest treatment and sits upper-right; title/descriptor occupy a separate small upper-left zone; support and plain `EXPLORA EL TALLER` sit in separate lower-right groups. No button or pill. Keep the rim outside every text box. |
| 02 | Process | `Del giro / nace el borde.` | Existing generated conceptual wheel-and-clay base, text-free; use a wider crop that reveals the wheel arc and clay coil | Shift headline to the lower-left and reduce its scale from slide 01; let its line angle/measure answer the wheel's circular motion, without crossing the wheel rim, hands, coil, or glyphs. Place title/descriptor at upper-right; support in a distinct upper-left quiet zone; plain `SIGUE EL PROCESO` near the lower-right, away from the headline. No button or pill. |
| 03 | Close | `Cada huella / deja memoria.` | Existing generated conceptual clay-surface/mark base, text-free; use a close macro crop that preserves the whole thumbprint/incised trace | Change the crop and scale again: headline medium-sized in the upper-left, beside (not over) the trace; title/descriptor move to a quiet lower-left edge; support occupies a separate mid-right zone; only `MIRA LAS PIEZAS` receives CTA treatment, centered in a clear lower zone distinct from support and trace. |

- Exact mark and descriptor on every slide: `TALLER BARRO` / `CERÁMICA`.
- Set-continuity device: shape → turn → trace, recurring clay material and shared type character. Do not lock headline scale/position, crop, or CTA location across slides; the repeated mark and type system provide continuity while each frame's geometry changes.

### Copy zones and type minimum

Treat each text group as its own bounded zone: title, descriptor, headline (keep each two-line headline together), support, and CTA/plain integrated closing line. Keep at least 42 px cap height for supporting/descriptor/other small required copy in the 1080×1350 master (14 px at the 360×450 feed preview); the headline and title may be larger. Preserve generous gaps between groups and between each group and the ceramic detail. The crop/placement plan must leave the vessel rim, wheel rim/coil, or full surface trace visible and keep all glyphs clear. Only `MIRA LAS PIEZAS` receives CTA treatment; `EXPLORA EL TALLER` and `SIGUE EL PROCESO` stay plain integrated text.

## 13. Log (fill at delivery)

- Direction sheet path and seed: `evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/direction.md`; deal seed `20261024`; choice `frame-system` / `cinematic-editorial`.
- Reference IDs consulted; local images viewed?: no reference pixels; record any read-only visual study separately.
- Rubric scores: not used as approval evidence
- Fixes made: none before generation
- Images used and their sources: none yet; planned generated conceptual photos contain no text/logos and receive exact code overlays with bundled OFL fonts.
