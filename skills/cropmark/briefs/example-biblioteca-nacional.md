# Cropmark brief — Biblioteca Nacional de España

Reference-free example: the subject is not one of the Behance projects in the study. Facts below come from official Biblioteca Nacional de España pages; no third-party artwork or statistics are used.

## 1. Job

- Format: carousel, 5 × 1080×1350
- Platform: Instagram feed
- Language: Spanish
- Number of pieces: one five-slide set
- A/B wanted? no

## 2. Copy given, verbatim

- Title: BNE Digital
- Headline: El pasado cabe en una página
- Supporting copy: Libros, mapas y voces en formato digital.
- CTA: Explorar BNE Digital
- Word-cap reference: Cropmark SKILL.md non-negotiable 2.

## 3. Facts allowed

- The institution's name is Biblioteca Nacional de España. Source: [official BNE site](https://www.bne.es/es).
- Its central seat is at Paseo de Recoletos 20–22, Madrid. Source: [BNE central seat](https://www.bne.es/es/sede/sede-central-recoletos).
- BNE Digital provides access to digitised heritage collections, including books, manuscripts, maps, drawings, prints, posters, photographs, music scores and sound documents. Source: [BNE Digital](https://www.bne.es/es/catalogos/biblioteca-digital-hispanica).
- No statistics, dates, prices or performance claims are allowed. The headline is a metaphor, not a claim about the complete collection.

## 4. Assets that really exist

- No supplied photos, screenshots, logos, brand colours, brand fonts or generation tool.
- `--have`: none. Use typography and original shapes only; no external images.

## 5. Brand locks

- Fixed colours: none supplied.
- Fixed fonts: none supplied.
- Other identity constraints: spell the institution and platform names exactly as written in the allowed facts.
- Keep in draw: none.

```yaml
colors: []
typography: []
```

## 6. Subject inventory (8–12 items)

1. The name Biblioteca Nacional de España.
2. The central-seat address, Paseo de Recoletos 20–22, Madrid.
3. The name BNE Digital and its digital heritage platform.
4. Digitised books.
5. Manuscripts.
6. Maps and atlases.
7. Drawings.
8. Prints and engravings.
9. Posters.
10. Photographs.
11. Music scores.
12. Sound documents.

Items 3–12 name the platform and categories listed by BNE Digital; they do not imply a quantity or a specific item.

## 7. Anti-references

- Nearest real competitor/feed, if known: none selected or studied for this example.
- Avoid a generic library shelf collage, fake archival dates, invented quotations, miniature unreadable labels, or claims about collection size. These are constraints for this brief, not claims about another institution.

## 8. Draw

```sh
python3 skills/cropmark/scripts/draw.py --format carousel --brief "BNE Digital: una invitación tipográfica a explorar patrimonio digital" --seed 4401 --options 3
```

- Seed 4401; options: `across-the-swipe`, `frame-system`, `type-is-the-image`.
- Chosen: `type-is-the-image` — the BNE Digital media categories become the typographic image, tying the concept to inventory items 4–12.
- Choice command: `python3 skills/cropmark/scripts/draw.py --format carousel --brief "BNE Digital: una invitación tipográfica a explorar patrimonio digital" --seed 4401 --direction type-is-the-image --why "La lista de formatos documentales de BNE Digital se convierte en la imagen tipográfica y pertenece a este catálogo."`
- Redraws and reasons: none planned.

## 9. Idea sentence + competitor test

“In this piece, **the Recoletos address becomes an index leading into BNE Digital's listed media types**.” No competitor was selected; against a generic library, the Recoletos address makes the sentence specific to this institution. Self-check: would I make this for any similar brief? Not with that address and this documented mix of media.

## 10. Concept (3 lines)

- Idea: make the range of BNE Digital's recorded media types behave like a browsable index.
- What the image shows without reading: an original typographic arrangement moving from printed forms to sound.
- Style card selected from the direction: `editorial-maximal-yellow` (provisional draw for seed 4401).

## 11. Hooks / variants

1. El pasado cabe en una página.
2. Un mapa también guarda una historia.
3. Hay libros que empiezan por el sonido.
- Selected hook: El pasado cabe en una página.
- A/B: not requested.

## 12. Carousel page plan (carousels only)

| Slide | Role | Hook | Image source | Layout intent |
|---|---|---|---|---|
| 01 | Cover | El pasado cabe en una página | Original type and drawn index marks | Open the idea with a single oversized page-like frame |
| 02 | Books and manuscripts | Una página puede guardar muchas voces | Original typography | Pair two media names on a shared reading axis |
| 03 | Maps and drawings | Un mapa también guarda una historia | Original line drawing | Let one drawn route connect the labels |
| 04 | Posters and photographs | La imagen también forma parte del archivo | Original typography and shapes | Shift from text to a simple image-frame motif |
| 05 | Sound and CTA | Hay libros que empiezan por el sonido | Original type and waveform-like marks | Close with the sourced sound-document category and CTA |

- Set-continuity device: repeat an original index rule and page marker; vary the listed media category.

## 13. Log (fill at delivery)

- Direction sheet path and seed: `.cropmark/direction.json`; seed 4401.
- Reference IDs consulted; local images viewed?: `bh08-fabio-malvezzi`, `bh11-estudio-mona`, `bh21-blu-main`; text cards only, no local images viewed.
- Rubric scores: not assessed; this is a brief example, not a rendered delivery.
- Fixes made: none yet.
- Images used and their sources: none; original shapes only.
