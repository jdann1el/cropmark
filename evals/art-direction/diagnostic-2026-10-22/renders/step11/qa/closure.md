# Paso 11 closure

## Requirements matrix

| Area | Result | Evidence |
|---|---|---|
| Protected feedback and scope | PASS | Guardrail SHA-256 unchanged; no tracked files changed. Existing untracked `renders/step3/qa-report.json/` left untouched. |
| Generation/correction budgets | PASS at cap | `imagegen-log.json`: ordinals 1–6, all success/hash matches; correction logs R1–R3. |
| Direct baselines and normalization | PARTIAL | Historical A files match exact Lanczos normalization; three fresh carousel baseline sources match normalized finals and revised copy. Session-scope claims are recorded but actual Herdr transcript/context is unavailable, so full isolation is unverified. |
| Finals, previews and boards | PASS | Five finals and all required previews open; dimensions and hashes match; board cell crops match source pixels and external label bands; flyer's first two cells are identical. |
| Thumbnail technical | FAIL | Board top edge at y=29 px violates 40 px safe zone. Some custom glyph-core contrast and exact geometry remain unresolved. |
| Flyer technical | FAIL / incomplete | Projected title baseline and metadata cap checks are unresolved; corner residual and line-fit evidence is not verifier-certified. |
| Carousel technical | FAIL | Slide 2 headline P05 1.05:1 (<3:1); slide 1 descriptor P05 4.16:1 (<4.5:1); slide 2 largest empty component 24.8% (>20%); trace estimate 75 px (<90); descriptor cap 13.33 px (<14); slide 3 headline/support cap ratio 1.87 (<2); brand top inset 60 px (<64). |
| Strict QA | PASS, limited | Thumb/post/carousel strict commands each exit 0. Their surrounding-region contrast checks do not cover all frozen acceptance criteria. |
| Reproducible handoff | FAIL | `package/`, `qa/reproduction.md`, and `handoff-manifest.json` are absent; external-folder render, pixel equality and edit proof cannot be checked. |
| Independent ordering | FAIL | First reads preceded key reveal, but producer manifest/key/plane values were opened before all independent pixel calculations. |
| Design/value | FAIL | Direct wins 2/3, flyer loss; owner comparison has one loss. Absolute reference level remains unverified. |

## Honest value result

Local preference over the matched direct baseline: **2/3 pieces** (thumbnail win, flyer loss, carousel win). Against Paso 10 owners: **1 win, 1 tie, 1 loss**. The required 3/3 direct wins, zero owner-winner losses, and passing technical set are not achieved. No general causal Cropmark claim is supported by this exercise.

## Unresolved items

1. Missing T14 portable package, reproduction record and handoff manifest.
2. Verification-order breach limits independent attestation.
3. Thumbnail top edge violates safe placement; exact gap/contrast records are incomplete.
4. Flyer projected typography/cap measurements and independent corner residual need valid remeasurement.
5. Carousel contrast, empty-component, trace-scale, descriptor-cap, closing hierarchy and safe-margin failures need correction and a new verifier pass.
6. No suitable local close-reference IDs were available; all three absolute reference-level judgments remain unverified.
7. Historical model/session context cannot be independently authenticated from the saved scope note alone.

No staging or commit was performed because OVERALL is FAIL.

## T14 addendum (2026-10-27)

The portable package was reproduced from a temporary directory outside `step11`: all five finals match decoded pixels exactly (0 differing pixels), and local text edits changed pixels in each piece. The package contains 32 hashed files (37,694,379 bytes); see `qa/reproduction.md` and `handoff-manifest.json`. Design verdicts and `OVERALL: FAIL` remain unchanged.
