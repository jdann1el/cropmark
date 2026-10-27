# Cropmark brief — Noche de vinilos flyer (fictional test)

Fictional test brief for a fictional Barcelona event. Preserve the full exact copy; do not add facts or claims.

## 1. Job

- Format: post 1080×1350
- Platform: Instagram feed flyer
- Language: Spanish
- Number of pieces: 2 flyer conditions, A and B
- A/B wanted? yes; compare execution method while holding concept, scene premise, and exact copy constant.
  - A: one direct image_gen call produces the final raster flyer, including the complete exact supplied copy; no Cropmark skill instructions in the generation prompt.
  - B: one image_gen text-free base with no letters/logos, then Cropmark code overlay using the same exact copy and premise.

## 2. Copy given, verbatim

- Title / only flyer copy: `Noche de vinilos · Sala Taller · 14 nov · 21:00`
- Headline: `Noche de vinilos · Sala Taller · 14 nov · 21:00`
- Supporting copy: none
- CTA: none
- Word-cap reference: preserve the exact string and separators; add no other copy.

## 3. Facts allowed

This is a fictional test. The only allowed copy is the exact supplied string. Add no address, price, year, availability, performers, or other claim.

## 4. Assets that really exist

No supplied image asset. Use `gen-image`. A is direct image_gen output as the final raster with exact copy requested. B is a text-free image_gen conceptual vinyl-listening base without letters, logos or watermark, then exact Cropmark code overlay using a bundled OFL font. Preserve both generation prompts and outputs.

## 5. Brand locks

- Fixed colours: none
- Fixed fonts: none; B uses a bundled OFL font and records its file
- Other identity constraints: fictional test only; no real venue identity or performer likeness
- Keep in draw: none

```yaml
colors: []
typography: []
```

## 6. Subject inventory (8–12 items)

Conceptual objects only; do not imply real event logistics beyond the supplied copy.

1. Vinyl record with visible grooves
2. Turntable platter
3. Tonearm and stylus
4. Record sleeve without lettering
5. Listening chair
6. Pool of warm lamplight
7. Hands selecting a record
8. Circular motion in the record grooves

## 7. Anti-references

- Nearest real competitor/feed, if known: none supplied
- What this piece must not resemble: a real club announcement with invented address, lineup, price, year, or availability

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format post --brief skills/cropmark/briefs/example-noche-vinilos-flyer-test.md --have gen-image --seed 20261026 --options 3
```

- Seed and three dealt options: `20261026`; `object-metaphor`, `duel`, `artefact-in-scene`. Draw noted that fewer than three fresh directions remained and recent picks were allowed to fill the deal; see the S9 deal record.
- Chosen direction and one-line reason naming its inventory item: `artefact-in-scene` / `text-in-scene`; the blank record sleeve can carry the exact event string while keeping the vinyl visible and adding no event facts.
- Redraws and reasons, if any: none before generation.

## 9. Idea sentence + competitor test

“In this piece, **the vinyl record's grooves** become **the visual rhythm of a listening event**.” Do not let the idea imply performers or event details not in the copy.

## 10. Concept (3 lines)

- Idea: the physical record and listening gesture make the fictional event legible without extra claims.
- What the image shows without reading: a grooved record on a turntable, with no visible interface text.
- Style card selected from the direction: `text-in-scene` (`artefact-in-scene`).

## 11. Hooks / variants

1. Oversized grooves become the main visual rhythm around the copy.
2. A hand selects one blank sleeve beside the turntable.
3. A tonearm and record form a focused listening scene.
- Selected hook: exact copy on a blank sleeve in a vinyl listening scene; A and B use this same hook and copy, with only the generation/overlay method changing.
- For A/B, A is one direct image_gen final raster; B is a text-free image_gen base plus exact Cropmark overlay. No seed rerolls as variants.

## 12. Carousel page plan

Not applicable.

- Set-continuity device: not applicable.

## 13. Log (fill at delivery)

- Direction sheet path and seed: `evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/direction.md`; deal seed `20261026`; choice `artefact-in-scene` / `text-in-scene`.
- Reference IDs consulted; local images viewed?: no reference pixels; record any read-only visual study separately.
- Rubric scores: not used as approval evidence
- Fixes made: none before generation
- Images used and their sources: none yet; A planned direct image_gen final, B planned text-free image_gen base and exact Cropmark text overlay.
