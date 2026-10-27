# T1 — provenance and guardrail audit

Date: 2026-10-26. Scope: snapshot the current Paso 11 starting state, inspect the already-produced NO-SKILL baseline and ledger, verify historical direct controls and identify reusable inputs. This audit does not reset the ledger or alter any historical asset.

## Starting guardrails

- Protected file `docs/recalibration-v3-human-feedback.json`: SHA-256 `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38` at task start.
- Initial `git status --short`: `?? docs/spec-paso11.md`; `?? evals/art-direction/diagnostic-2026-10-22/renders/step11/`; `?? evals/art-direction/diagnostic-2026-10-22/renders/step3/qa-report.json/`. The Step 3 untracked path is pre-existing and excluded. Current branch: `cropmark-reference-library`; no staged or tracked diff at task start.
- The supplied instructions and spec are the governing instructions. No repository `AGENTS.md` was found in the repository/ancestor locations reported by the spec. No files outside S11 were created or changed by T1.
- The spec, Paso 9/10 sources, baseline records and protected-file hash are inventoried in `input-manifest.json`.

## Existing NO-SKILL carousel baseline and ledger

The shared `imagegen-log.json` already contains successful ordinals 1–3 for `p11-baseline`, with exact prompts, `references: none`, output paths and matching SHA-256 values. All three source paths exist and match their ledger hashes. The normalized files exist at 1080×1350 and are pixel-identical to direct 1080×1350 Lanczos resizing of their corresponding 1122×1402 source images. Baseline provenance records, frozen manifest, neutral brief, exact prompts and session-scope declaration agree on the content and normalization. The baseline session scope says the operator did not read Cropmark/design materials and supplied no winner images or design thresholds. No contrary provenance evidence was found in these records.

Visual inspection confirms the required text and subject for each slide; slide 1/2 have no apparent CTA and slide 3 has the single required `MIRA LAS PIEZAS` CTA rendered inside a pill. That pill is a baseline defect to preserve, not repair. Font identity and the original generation-tool session cannot be independently established from the local image pixels; retain the stated provenance as recorded and label font identity unknown. Operationally, these are direct-final generations from the neutral brief without supplied Cropmark rules or references; this does not prove their prompt author had never read Cropmark.

Budget state is **3/6 used, 3 remaining; next ordinal 4**. The existing ledger was not reset or rewritten. Reconcile its exact records and all source hashes in `input-manifest.json`; any later call must be appended with its ordinal before dispatch.

## Direct controls and reuse decisions

| Piece | Evidence checked | T1 disposition |
|---|---|---|
| Thumbnail | Paso 9 prompt/log global call 4 identifies `thumbnail/A-source.png` as a direct finished image, no reference asset; source SHA-256 `f9dccd716e68b698df332970069358ee49d13090b2c5534bb617e535a657858a`. `render_s9.py` center-crop/Lanczos output `thumbnail/A.png` is an exact pixel match. | Reuse `step9/thumbnail/A.png` as NO-SKILL row. Use clean `step9/thumbnail/B-base-R1-source.png` and the editable Paso 10 C renderer/source for candidate work, as specified. The A creative response differs, so report unmatched imagery as a limitation. |
| Flyer | Paso 9 prompt/log global call 6 identifies `flyer/A-source.png` as a direct finished image, no reference asset; source SHA-256 `76565aa408da02828f77856dee40bd1c3c07fcf7369e18e0241e1d50020cc73f`. `render_s9.py` center-crop/Lanczos output `flyer/A.png` is an exact pixel match. | Reuse `step9/flyer/A.png` as both direct NO-SKILL comparator and Paso 10 owner winner. Keep the first two board cells identical and disclose the duplication after blind first reads. Use `step9/flyer/B-base-source.png` for the candidate, subject to T7 plane review. |
| Carousel | Historical Paso 7 A prompts and `slide-1.png`…`slide-3.png` are direct finals; `render_step7.py` only normalizes to `final-1.png`…`final-3.png`. Their old prompts include `EXPLORA EL TALLER` and `SIGUE EL PROCESO`, so they do not match the frozen revised brief. Paso 8 B2 has reusable clean bases and the owner's Paso 10 winner is its unchanged three-slide final row. | Preserve historical Paso 7 A only as historical provenance. Use the already frozen new Paso 11 direct baseline for the revised brief. Develop the candidate from `step8/B2/base-1.png`…`base-3.png`; use the unchanged `step8/B2/final-1.png`…`final-3.png` as the Paso 10 winner row, labelled “historical copy: three action lines.” |

## T1 result

**PASS for provenance disposition; baseline audit complete with limitations recorded.** The existing three-slide baseline is logged, hashed and normalization-verified; its first outputs remain unretouched. No provenance issue requires replacement. The spec's missing matching carousel control is now supplied by the frozen baseline. Protected-file and status snapshots are in `input-manifest.json`. Continue to T6 with the shared budget at 3/6 and the baseline preserved.
