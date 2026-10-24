# Cropmark brief — [subject]

Fill the fixed sections before drawing a direction. Keep copy verbatim and separate sourced facts from creative language. Use `none` where a fact or asset is absent.

## 1. Job

- Format: [thumbnail 1280×720 / post 1080×1350 / carousel N×1080×1350]
- Platform:
- Language:
- Number of pieces:
- A/B wanted? [yes/no; what should differ?]

## 2. Copy given, verbatim

- Title:
- Headline:
- Supporting copy:
- CTA:
- Word-cap reference: Cropmark SKILL.md non-negotiable 2.

## 3. Facts allowed

List the only names, numbers and claims this piece may show, with source URLs. `None` is valid. Do not add inferred or unsourced proof.

## 4. Assets that really exist

List only files/tools available for this job, using draw tags where applicable: `face-photo`, `product-photo`, `screenshot`, `logo`, `brand-colours`, `brand-fonts`, `gen-image`, `brand-asset`. If none exist, write `none`. These become `--have`.

## 5. Brand locks

- Fixed colours:
- Fixed fonts:
- Other identity constraints:
- Keep in draw: [e.g. `palette,type`; or `none`]

```yaml
colors: []
typography: []
```

## 6. Subject inventory (8–12 items)

Use concrete noun phrases that belong to this subject: name/meaning, object, material/colour, place, sourced number, constraint, ritual/time, printed artefact, before/after, stake. Cite a source for factual items; do not invent numbers.

1.
2.
3.
4.
5.
6.
7.
8.

## 7. Anti-references

- Nearest real competitor/feed, if known:
- What this piece must not resemble:

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format [format] --brief "[brief]" --options 3
```

- Seed and three dealt options:
- Chosen direction and one-line reason naming its inventory item:
- Redraws and reasons, if any:

## 9. Idea sentence + competitor test

“In this piece, **[inventory item]** becomes **[direction device]**.” Put the nearest competitor in the sentence. If the sentence still works, replace the first item. Self-check: would this idea fit any similar brief?

## 10. Concept (3 lines)

- Idea:
- What the image shows without reading:
- Style card selected from the direction:

## 11. Hooks / variants

1.
2.
3.
- Selected hook:
- For A/B, describe the different hook type or direction for each variant; do not use seed rerolls as variants.

## 12. Carousel page plan (carousels only)

| Slide | Role | Hook | Image source | Layout intent |
|---|---|---|---|---|
| 01 | Cover |  |  |  |

- Set-continuity device:

## 13. Log (fill at delivery)

- Direction sheet path and seed:
- Reference IDs consulted; local images viewed?:
- Rubric scores:
- Fixes made:
- Images used and their sources:
