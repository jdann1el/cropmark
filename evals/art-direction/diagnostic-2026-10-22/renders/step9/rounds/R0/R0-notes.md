# Paso 9 R0 compositor record

R0 is held for feed-first review. No correction rounds were consumed. The PNG finals were byte-for-byte unchanged after the metadata reset; only the B3 Cropmark `.boxes.json` registry was corrected to contain that slide’s boxes only. A-condition finals are direct imagegen rasters normalized by centered crop and resize; their embedded lettering remains raster and the font is unknown.

## Exact local contrast and cap checks

Measurements use glyph-core pixels over each exact centered source crop before the text layer is composited. RGB channels were linearized to sRGB relative luminance. No shadow, stroke, or panel contributed to the calculation. Full data: `rounds/R0/contrast-R0.json`.

| Piece / slide | Group | P05 | Median | Pixels under target | Target | Cap at 360 |
|---|---|---:|---:|---:|---:|---:|
| B3 / 1 | `Una pieza empieza con un gesto.` | 1.204 | 2.485 | 73.908% | 4.5:1 | 14.00px |
| B3 / 1 | `EXPLORA EL TALLER` | 1.559 | 2.952 | 73.302% | 4.5:1 | 14.00px |
| B3 / 2 | `SIGUE EL PROCESO` | 2.255 | 4.518 | 49.765% | 4.5:1 | 14.00px |
| B3 / 3 | `TALLER BARRO` | 4.375 | 4.922 | 13.307% | 4.5:1 | 14.33px |
| B3 / 3 | `CERÁMICA` | 4.309 | 4.705 | 27.885% | 4.5:1 | 14.33px |
| B3 / 3 | `Un rastro queda en la superficie.` | 4.267 | 4.868 | 21.929% | 4.5:1 | 14.00px |
| flyer/B | `Sala Taller · 14 nov · 21:00` | 6.806 | 7.427 | 0.000% | 4.5:1 | 13.33px |

All B3 headline cap heights meet the 2× small-copy minimum: slide 1 31.67px vs 14px; slide 2 28.00px vs 14px; slide 3 29.67px vs 14px. The small-copy minimum itself is 14px at 360px.

## Strict QA

Commands, stdout, and machine reports are retained in `qa/R0/`. QA uses its surrounding-ring contrast estimate; the exact glyph-core report above contains the per-pixel check.

| Group | Command | Result |
|---|---|---|
| carousel | `python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step9/B3/final-3.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R0/carousel` | **FAIL** (exit 1; 3/3) |
| thumb | `python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 2 evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/A.png evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/B.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R0/thumb` | **PASS** (exit 0; 2/2) |
| post | `python3 skills/cropmark/qa/qa.py post --strict --expected-count 2 evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/A.png evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/B.png --out evals/art-direction/diagnostic-2026-10-22/renders/step9/qa/R0/post` | **PASS** (exit 0; 2/2) |

Carousel strict QA fails on `Una pieza empieza con un gesto.` (2.5:1), `EXPLORA EL TALLER` (3.4:1), and `SIGUE EL PROCESO` (4.0:1) using its surrounding-background estimate. Thumb and post strict QA pass. Per-piece logs are the source of truth for all individual checks.

## Pending review note

Visual review remains pending. A possible headline-to-vessel-rim collision on B3 slide 1 is flagged for the feed-first review; no visual judgment or corrective change was made in R0. R1 changes wait for Sol review.

The package copy at `package/` rerenders from bundled sources and local fonts. `package/editability-proof.json` records a temporary copy outside the repo where changing one B3 CTA literal changed the corresponding overlay text; project finals were not changed.
