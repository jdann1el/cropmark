# Flyer direction record — Noche de vinilos (fictional test)

## Before generation

- Only copy, exactly: `Noche de vinilos · Sala Taller · 14 nov · 21:00`. No added address, price, year, performers, availability, or claims.
- Format: 1080×1350 Instagram feed flyer. The event is fictional; no real venue identity or performer likeness.
- Assets: `gen-image`. A is one direct image_gen final raster with the exact copy requested and no Cropmark skill instructions in its prompt. B is a text-free image_gen base then the same exact Cropmark code overlay. Preserve prompts and outputs.
- Inventory: vinyl record with visible grooves; turntable platter; tonearm/stylus; blank record sleeve; listening chair; warm lamplight; hands selecting a record; circular groove motion.
- Reference inspection: no reference pixels used for this preparation; visual review is pending.

## Concepts

1. **Copy on sleeve** — the blank sleeve becomes a real in-scene carrier for the complete event string; the vinyl remains the recognizable listening cue.
2. **Groove rhythm** — oversized grooves create circular rhythm around an external, clearly grouped event title; the record does not carry lettering.
3. **Listening gesture** — tonearm, platter and a hand selecting a blank sleeve make the event feel like a listening moment; all copy stays in one calm side band.

## Two textual sketches (not rendered)

- **Sketch A — artifact-in-scene:** record and blank sleeve fill the lower-right; the exact event string is set on the sleeve as one clear editorial group. Leave room around the sleeve so the record grooves remain visible. The sleeve is a physical artifact, not a fabricated venue poster.
- **Sketch B — groove rhythm:** large cropped record anchors the lower-right; text sits on an unprinted calm upper-left field. The tonearm leads into the date/time. More legible but less integrated than the sleeve treatment.

## Draw record and choice

- Actual deal: seed `20261026`; options `object-metaphor`, `duel`, `artefact-in-scene`; note: fewer than three fresh directions remained and recent picks were allowed to fill the deal. Records: `dealt-options.json`, `direction.json`.
- Selected direction: `artefact-in-scene`; style card: `text-in-scene`.
- Reason: the inventory's blank record sleeve is a plausible carrier for the exact event string; the vinyl stays recognizable and hierarchy can distinguish event, room, date and time without adding facts.
- JEV option check selected `artefact-in-scene` (confidence 0.89); this is a judgment, not evidence of performance.
- Rejected: `object-metaphor` can let a surreal object overwhelm the information hierarchy; `duel` suggests a contest absent from the copy.
- No visual sketch renders exist yet; the two sketches above are planning descriptions only.

## Prompt zone plan

Both conditions use the same conceptual listening scene, sleeve placement, and exact string. Keep required copy at least 64 px from edges. A asks image_gen for one final raster with the exact text; preserve any malformed lettering. B asks for a photographic text-free scene with no letters, labels, logos or watermark; leave a clean, matte sleeve or adjacent quiet field for the controlled overlay. Do not imply real performers, venue logistics, prices, year, or ticket availability.

| Zone | Plan |
|---|---|
| Main object | Recognizable record and visible grooves on a turntable in the lower-right/lower-center; preserve tonearm and platter edges. |
| Copy carrier | A blank sleeve in the upper-left/center-left, large and quiet enough for the complete exact string; no extra sleeve text. |
| Type hierarchy | Keep `Noche de vinilos` primary; `Sala Taller`, `14 nov`, and `21:00` remain in the exact string and clearly distinguishable as a grouped sequence. Do not add labels or separators beyond supplied `·`. |
| Margins | All essential type and object details remain within 64 px safe margin; avoid crop and busy grooves beneath text. |

## Later review fields

- Sketch-image paths / first read: pending; text sketches only at this stage.
- Full-size and 360×450 review, contrast, copy integrity and A/B limitations: pending; no rendering or review performed.
