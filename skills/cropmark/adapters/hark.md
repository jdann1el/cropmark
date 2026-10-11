# Adapter: Hark
- Imagery: `deferred_tool` → `generate_image`. Notes learned in testing:
  - Files are saved to the **project root**, not the shell's working directory: move them into your work folder right away (and never leave strays).
  - Output size is fixed per aspect (≈1376-1408x768 landscape, 928x1152 portrait): crop with `cm.cover`; keep heroes large in the prompt to avoid upscaling.
  - `transparent_background` gives a cutout (check for green spill → `cm.despill`). Editing with a reference image (`image_paths`) works well to fix an artefact in an otherwise good base.
- Engines run in the sandbox shell (Python 3 + Pillow; Node + Playwright for HTML). Browsers/apt libs don't persist between sessions. `cd engines/html && npm i` (render.mjs auto-falls back to any cached Chromium if the version it wants is missing); `npx playwright install chromium` only if nothing is cached. Manual override: `export CHROME_PATH=$(ls -d ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell | tail -1)`. Missing libs: `sudo apt-get install -y libatk1.0-0t64 libxcomposite1 libxdamage1 libatspi2.0-0t64`.
- Parallel agents: each writes to its own folder and passes `--out <own dir>` to qa.py; keep `.boxes.json` out of delivery folders with `cm.save(..., boxes_dir=...)` / `qa.py --boxes`.
- Look at every output with `read_file` (full size + qa contact sheet). Deliver with `display_file`.
