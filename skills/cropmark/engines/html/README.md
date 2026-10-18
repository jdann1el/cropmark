# HTML engine (layout-heavy posts, carousels, panoramas)
Setup once: `cd engines/html && npm i && npx playwright install chromium` (on Linux, missing system libraries are listed by Playwright; install them yourself).
Write one HTML with `<section class="frame" id="c1-cover">` per output (fixed px sizes). For a seamless carousel make ONE `<section class="frame pano" data-slices="4" style="width:4320px">` and place elements across borders.
Render: `node engines/html/render.mjs page.html out 1` → `out/01-<id>.png` + `.boxes.json` (text boxes for QA). Font families = file stems in `fonts/` (e.g. `font-family:"Anton-Regular"`, `"InstrumentSerif-Italic"`).
Images: reference local files with relative paths; use `object-fit:cover` + `object-position` chosen from the subject.

Notes
- QA boxes are measured from CSS text ranges (not exact glyph ink or element boxes); mark text that intentionally bleeds off-frame with `data-role="bleed"`.
- Optional: set `CHROME_PATH` to the full path of a Chrome/Chromium you already installed to skip the Playwright download.
- Pre-process images (halftone, torn paper, grading, despill) with the Pillow helpers in `engines/pillow/cm.py`, save PNGs, then reference them in the HTML.
- Seamless panoramas: keep objects that cross a border out of full-width rows/lists; reserve a clear band where they cross.

Validation and metadata
- Scale must be positive and finite. Empty documents, invalid `data-slices` (positive integers only), unsafe or duplicate frame IDs, failed image decoding inside frames, unavailable first requested font families, and non-bleed text bounds outside a frame exit nonzero with an `ERROR cropmark HTML` diagnostic. IDs may contain letters, digits, `_` and `-`, starting with a letter or digit. Validation happens before any PNG export.
- Font stacks are accepted when the first family is available. Generic CSS families and installed system fonts are supported; missing first families fail even if the browser could silently use the next fallback. System availability uses width probes across three generic families; this is a detection heuristic, not a complete glyph-coverage guarantee. Bundled fonts retain their file-stem family names. Output `effectiveFonts` comes from Chromium and describes the text's parent element, including descendants; inspect it for glyph fallback.
- All `size`, text `box`, text `size`, and `strokeWidth` values in `.boxes.json` use physical output pixels, including scale 2. Top-level size is read from the PNG. Slice boxes retain cross-border portions for seamless panoramas.
- Text bounds are CSS Range rectangles expanded by half the CSS text-stroke width and rounded outward. They are not exact raster ink bounds: glyph overhang, shadows, and transforms can extend farther. `boundsKind` and `boundsNote` disclose this limit. Non-bleed bounds extending outside a frame are errors; intentionally overflowing text remains supported with `data-role="bleed"`.
