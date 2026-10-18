# Pillow engine
`import sys; sys.path.insert(0, '<skill>/engines/pillow'); import cm`
Typical thumbnail: `im = cm.cover('base.png', 1280, 720, focus=(.5,.4)); im = cm.grade(im); im = cm.shade(im,'left',.55); cm.text(im,(70,90),'HOOK\nWORDS', cm.fit('HOOK\nWORDS','Anton-Regular',560), stroke=0, shadow=(0,8,18,.6)); cm.save(im,'out/thumb.jpg')`
Functions: reset, font(weight=), new, cover(zoom=), grade, shade, vignette, text (tracking keeps kerning/leading/stroke/shadow/align), fit, rounded, card, pill, sticky (rotated note), rotated, blur_region, halftone, torn_mask, key_out, despill, paste, compare_sheet (before/after sheet), save(boxes_dir=) → .boxes.json for QA.
Call `cm.reset()` once per output (cover() no longer clears boxes, so composites keep them).


v0.5 candidate contracts:
- `text()` records actual font file and conservative ink bounds including stroke. Alpha fills composite onto the image. Glyphs matching the font's missing-glyph shape raise `ValueError`; this is not a complete Unicode shaping validator.
- `fit(..., stroke=0)` returns a fitting font or raises `ValueError` when the minimum cannot fit. It does not silently return an overflowing font. Change layout or report the conflict.
- Use exact font stems from `fonts/`. A requested variable weight must exist and be within its axis range; static fonts use their actual file, without a pretend weight override.
- `key_out()` keys matching border-connected background only. Enclosed matching subject details survive, but border-connected matching colours remain ambiguous. Use a verified mask or the intact photo for real hair/materials.
- `clean_cutout()` defaults to no erosion/feather/despill. Opt into each operation for a demonstrated defect; `despill_strength` is in [0,1]. Keep original photo, mask and processed layer separately. See `../../techniques/photography.md`.
- `save(..., text_free=True)` explicitly declares a composition with no text. Otherwise all visible text requires boxes and font evidence, including any manually drawn text. Use strict delivery QA with the expected file count; empty or shapes-only metadata is incomplete without that declaration.
- Sticky/tag metadata bounds are conservative rotated-layer bounds, not exact glyph masks. Photo contrast and outline legibility still need visual review.
