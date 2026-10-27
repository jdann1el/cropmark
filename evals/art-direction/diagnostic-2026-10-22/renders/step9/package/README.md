# Paso 9 editable package

The `evals/.../step9/render_s9.py` script is the canonical editable overlay source. B text remains exact and is recorded in PNG `.boxes.json` sidecars and duplicate SVG text layers. To change copy, edit the relevant text literal in the script and rerun it. Source images and bundled local font files are included.

A files are direct imagegen raster finals; lettering is embedded raster and its font is unknown. The script only normalizes dimensions by centered crop and resize.

The package includes `skills/cropmark/engines/pillow/cm.py` and the four OFL font files used by B. See `skills/cropmark/fonts/OFL-LICENSES.txt`.
