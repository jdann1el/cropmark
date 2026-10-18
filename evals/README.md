# Evals
- `briefs.md`: 12 frozen briefs (5 thumbnails, 4 posts, 3 carousels). `holdout.md`: 5 unseen briefs.
- Method: same briefs made without the skill (baseline) and with it; blind A/B + rubric (qa/rubric.md).
- Results (2026-10-11, self-scored, one agent family; treat as indicative): baseline avg 3.3 → skill v0.1 avg 4.2, 11/12 pairs won + 1 tie; hold-out with v0.2 avg 4.1 (all ≥4.0).


## v0.5 candidate: practical evaluation

The final closure plan completed 13 creative executions: one clean T5 regression and six new briefs in two conditions (v0.4 and rc5). Earlier baselines, candidate iterations and contingency attempts remain preserved by version; they are not pooled as fresh rc5 trials. The older 28+6 plan and exhaustive 369-run protocol are superseded. See [closure outcome](closure-v05.md) and [structured results](rc5-validation.json). The six new cases all pass individual candidate quality gates, but rc5 wins 4/6 pairs against the required 5/6 and remains unaccepted.

All new executions use GPT-6.1 Sol / low with fixed available tools/assets and initial output plus at most two refinements. Preserve every attempt, literal prompts, read modules, sources and model/tool limits. Do not invent image-model seeds or claim Hark parity.

Technical regressions are fast and separate from creative executions:

```sh
python3 evals/run_technical.py --out /absolute/new-evidence-directory --node /absolute/node --node-modules /absolute/node_modules --browsers /absolute/playwright-browsers
```

The command installs nothing and needs existing Pillow, Playwright and Chromium. Use a new output directory; it preserves commands, logs, hashes and outcomes. It exercises metadata/color, raster ink containment, fit, font/glyph handling, cutout defaults, HTML load/scale/slices, safe zones and renderer-to-strict-QA integration. Synthetic alpha fixtures do not certify real hair/glass segmentation. Visual truth, faithful reconstruction and content preservation require independent image review.

Acceptance: complete required deliverables, zero S1/visible technical S2, rubric mean ≥4, no criterion <3, legibility/finish ≥4, faithful-copy fidelity ≥4 with editability proof; candidate preferred over v0.4 in ≥8/10 known and ≥5/6 new cases, ties not wins. T3/T5 must preserve useful information and not lose. Outcomes, failures, ties, rubric distributions and limitations must be reported. This is practical case validation, not statistical equivalence.
