# Independent verification record

- Session id: `p11-verify-20261026-155908Z`.
- Start time: `2026-10-26 15:59:08 UTC`.
- Role: fresh verifier for Paso 11; no baseline prompting, generation, candidate composition, correction, producer QA, or board assembly for this paso. No image generation was called by this session.
- Frozen input hashes: [`frozen-input-hashes.json`](independent/frozen-input-hashes.json).
- Protected feedback before verification: `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`.
- Initial Git status: only `docs/spec-paso11.md`, S11, and the pre-existing untracked excluded `renders/step3/qa-report.json/`; no tracked files modified.

## Independence limitation

I inspected the anonymous comparison files and recorded first-read preferences before opening the blind key. I did, however, open `comparison-manifest.json`, `qa/blind/key.json`, and `flyer/plane-plan.json` before finishing my own automated pixel calculations. This violates the spec's required calculate-before-producer-values sequence for some checks. Pixel-derived values in my reports were calculated from finals and clean sources, but this session cannot attest to fully uncontaminated measurement order. The failure is disclosed and the verdict is not presented as a clean independent PASS.

## Commands and inspection actions

Executed from the repository root:

```text
cat /home/box/.codex/skills/jev-local/SKILL.md
cat docs/spec-paso11.md
sha256sum docs/recalibration-v3-human-feedback.json docs/spec-paso11.md evals/art-direction/diagnostic-2026-10-22/renders/step11/imagegen-log.json evals/art-direction/diagnostic-2026-10-22/renders/step11/comparison-manifest.json
python3 evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/independent/independent_measure.py
python3 evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/independent/verify_boards.py
python3 evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/independent/measure_contrast.py
python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 1 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/independent/strict-thumbnail evals/art-direction/diagnostic-2026-10-22/renders/step11/thumbnail/final.png
python3 skills/cropmark/qa/qa.py post --strict --expected-count 1 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/independent/strict-flyer evals/art-direction/diagnostic-2026-10-22/renders/step11/flyer/final.png
python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/independent/strict-carousel evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-3.png
```

All three strict QA commands exited 0; their output and individual statuses are preserved in `independent/strict-qa-run.json`. They check dimensions and broad contrast only; they do not satisfy the separate geometric, empty-area or glyph-core requirements. Master/feed images, anonymous comparisons, paired flyer crops and all three boards were opened at 100% display size. Pixel arithmetic used Pillow/OpenCV and linearized sRGB; masks/annotations and raw counts are under `qa/independent/`.

No design contract JSON was present under S11, so no `design_check.py` contract could be run. T14 package reproduction, decoded-pixel comparison in an external folder and editable-copy proof could not be run because `package/`, `qa/reproduction.md`, and `handoff-manifest.json` are all absent.
