# Cropmark brief — Portfolio agents thumbnail (fictional test)

Fictional test brief. Keep the supplied video title distinct from the thumbnail overlay. Keep all copy verbatim and add no outcome claims.

## 1. Job

- Format: thumbnail 1280×720
- Platform: YouTube
- Language: English
- Number of pieces: 2 thumbnail conditions, A and B
- A/B wanted? yes; compare execution method while holding concept, scene premise, and exact overlay copy constant.
  - A: one direct image_gen call produces the final raster thumbnail, including the exact overlay `3 AIs. 1 Portfolio.`; no Cropmark skill instructions in the generation prompt.
  - B: one image_gen text-free base with no letters/logos, then Cropmark code overlay using the same exact copy and premise.

## 2. Copy given, verbatim

- Video title/context: `I let 3 AI agents redesign my portfolio`
- Headline/only image overlay: `3 AIs. 1 Portfolio.`
- Supporting copy: none
- CTA: none
- Word-cap reference: overlay is exactly `3 AIs. 1 Portfolio.` (four words); add no other image copy.

## 3. Facts allowed

Only the supplied video title and exact overlay. No agent result, winner, success claim, metric, or before/after outcome is supplied.

## 4. Assets that really exist

No supplied image asset. Use `gen-image`. A is direct image_gen output as the final raster with exact overlay requested. B is a text-free image_gen conceptual base without letters, logos or watermark, then exact Cropmark code overlay in a bundled OFL font. Preserve both generation prompts and outputs.

## 5. Brand locks

- Fixed colours: none
- Fixed fonts: none; B uses a bundled OFL font and records its file
- Other identity constraints: fictional test only; no real platform, agency, or agent identity
- Keep in draw: none

```yaml
colors: []
typography: []
```

## 6. Subject inventory (8–12 items)

Conceptual nouns only; these do not assert real agent capabilities or results.

1. Three distinct agent tokens
2. One portfolio folio
3. A blank portfolio page
4. Three pointers aimed at one canvas
5. A shared design canvas
6. Cursor marks without legible interface text
7. Three parallel layout grids
8. A frame containing alternative page shapes

## 7. Anti-references

- Nearest real competitor/feed, if known: none supplied
- What this piece must not resemble: a fake product dashboard, benchmark, winner podium, or fabricated before/after result

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format thumbnail --brief skills/cropmark/briefs/example-portfolio-agents-thumbnail-test.md --have gen-image --seed 20261025 --options 3
```

- Seed and three dealt options: `20261025`; `face-plus-proof`, `split-contrast`, `stakes-stack`. Draw noted widening from two asset-feasible directions to five format-matching directions; see the S9 deal record.
- Chosen direction and one-line reason naming its inventory item: `split-contrast` / `split-transformation`; three agent tokens and the single blank portfolio folio make two readable opposing masses without suggesting an outcome or winner.
- Redraws and reasons, if any: none before generation.

## 9. Idea sentence + competitor test

“In this piece, **three distinct agent tokens** become **three simultaneous approaches to one portfolio canvas**.” The overlay must not imply a winner or outcome.

## 10. Concept (3 lines)

- Idea: make the video's three-agents/one-portfolio premise visible without claiming what the agents produce.
- What the image shows without reading: three distinct inputs meet one blank portfolio canvas.
- Style card selected from the direction: `split-transformation` (`split-contrast`).

## 11. Hooks / variants

1. Three distinct tokens converge on one blank portfolio page.
2. Three pointers meet at a single shared design canvas.
3. Three parallel layout grids frame one blank folio.
- Selected hook: three agent tokens face one blank folio; A and B use this same hook and copy, with only the generation/overlay method changing.
- For A/B, A is one direct image_gen final raster; B is a text-free image_gen base plus exact Cropmark overlay. No seed rerolls as variants.

## 12. Carousel page plan

Not applicable.

- Set-continuity device: not applicable.

## 13. Log (fill at delivery)

- Direction sheet path and seed: `evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/direction.md`; deal seed `20261025`; choice `split-contrast` / `split-transformation`.
- Reference IDs consulted; local images viewed?: no reference pixels; record any read-only visual study separately.
- Rubric scores: not used as approval evidence
- Fixes made: none before generation
- Images used and their sources: none yet; A planned direct image_gen final, B planned text-free image_gen base and exact Cropmark text overlay.
