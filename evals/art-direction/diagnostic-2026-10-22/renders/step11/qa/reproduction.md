# Paso 11 package reproduction (T14)

Run date: 2026-10-27

Renders were run from a temporary copy at `/tmp` outside the original Step 11 folder using the bundled scripts, sources, and licensed fonts. The temporary directory was removed automatically after the checks. Pixel comparison decoded both PNGs to RGB and counted pixels where any channel differed. Text edit checks changed one copy string inside a temporary script copy, confirmed a nonzero pixel change, then discarded the temporary copy.

| Piece | Result | Size | Different pixels | Sum absolute channel difference | Max channel difference | Mean absolute channel difference | Editable text proof |
|---|---|---:|---:|---:|---:|---:|---|
| thumbnail | PASS | 1280×720 | 0 | 0 | 0 | 0.00000000 | PASS (2078 pixels changed) |
| flyer | PASS | 1080×1350 | 0 | 0 | 0 | 0.00000000 | PASS (4097 pixels changed) |
| carousel slide 1 | PASS | 1080×1350 | 0 | 0 | 0 | 0.00000000 | PASS (3903 pixels changed) |
| carousel slide 2 | PASS | 1080×1350 | 0 | 0 | 0 | 0.00000000 | PASS (3679 pixels changed) |
| carousel slide 3 | PASS | 1080×1350 | 0 | 0 | 0 | 0.00000000 | PASS (4732 pixels changed) |

PASS requires zero decoded pixel differences from the frozen final and a nonzero difference after changing copy locally.
