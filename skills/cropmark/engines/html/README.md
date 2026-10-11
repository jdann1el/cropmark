# HTML engine (layout-heavy posts, carousels, panoramas)
Setup once: `cd engines/html && npm i && npx playwright install chromium` (on Linux, missing system libraries are listed by Playwright; install them yourself).
Write one HTML with `<section class="frame" id="c1-cover">` per output (fixed px sizes). For a seamless carousel make ONE `<section class="frame pano" data-slices="4" style="width:4320px">` and place elements across borders.
Render: `node engines/html/render.mjs page.html out 1` → `out/01-<id>.png` + `.boxes.json` (text boxes for QA). Font families = file stems in `fonts/` (e.g. `font-family:"Anton-Regular"`, `"InstrumentSerif-Italic"`).
Images: reference local files with relative paths; use `object-fit:cover` + `object-position` chosen from the subject.

Notes
- QA boxes are measured on the text glyph lines (not element boxes); mark text that intentionally bleeds off-frame with `data-role="bleed"`.
- Optional: set `CHROME_PATH` to the full path of a Chrome/Chromium you already installed to skip the Playwright download.
- Pre-process images (halftone, torn paper, grading, despill) with the Pillow helpers in `engines/pillow/cm.py`, save PNGs, then reference them in the HTML.
- Seamless panoramas: keep objects that cross a border out of full-width rows/lists; reserve a clear band where they cross.
