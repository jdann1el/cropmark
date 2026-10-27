# Paso 11 producer checks

Commands run from the repository root on 2026-10-26:

- `python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 1 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/thumbnail evals/art-direction/diagnostic-2026-10-22/renders/step11/thumbnail/final.png` — exit 0; 1280×720; metadata and measured contrast checks pass.
- `python3 skills/cropmark/qa/qa.py post --strict --expected-count 1 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/flyer evals/art-direction/diagnostic-2026-10-22/renders/step11/flyer/final.png` — exit 0; 1080×1350; text metadata and contrast checks pass.
- `python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/carousel evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-3.png` — exit 0; all three 1080×1350; text metadata and contrast checks pass.

Flyer builder measurements: sleeve top/bottom angles 7.214°/5.422° with matching slope; keystone 4.1%; text remains on the sleeve with 5.7% minimum inset; title and metadata projected caps at 360 are 35.24/14.19 px; ratio 2.484; two separators; no shadow layer. These are producer measurements, not independent corner-fit verification.

Carousel: three-slide copy is present, removed action phrases are absent from the copy contract, full-bleed photography, and one closing CTA. The 360 px contact sheet was visually inspected. `carousel/empty-area.json` records ≤35% empty cells on all slides. The zoomed closing thumbprint's ≥90 px master dimension and exact subject bbox still need independent measurement. No aesthetic win or Behance-level approval is claimed.

Thumbnail measurements meet its recorded subject-gap, edge, headline-cap, fill and duration-zone criteria. The image shows three agents around one shared portfolio at full view; independent transcription remains reserved for T15.

The protected `docs/recalibration-v3-human-feedback.json` SHA-256 remained `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`. Image-generation ledger contains ordinals 1–6 and is unchanged; no image generation occurred in this continuation.
