# Frozen held-out validation — human gate FAIL

Candidate art-direction-rc2 was frozen at cc36200d787d3500a56734052f669376f9b7e910 before six new briefs were authored. H1/H2 are thumbnails, H3/H4 four-frame carousels, H5/H6 three-post campaigns. Each ran once with no design skill, frozen rc5 and frozen rc2:18 trials,48 final PNGs. Native requested configuration:gpt-6.1-sol,low. Served telemetry and complete costs are unavailable.

All conditions had identical supplied imagery/logos/fonts, neutral rendering mechanics and an offline visual study bank. Reference captures were for study only, not output assets. This differs from the initial calibration's text-reference limitations; the two phases must not be pooled as one experiment. Four conceptual photographs were generated once before trials and shared byte-for-byte; the real supplied shaker and its printed identity were retained. Autonomous imagery sourcing/generation inside trials was not tested.

The coordinator verified all frozen source/input/brief hashes, exact PNG counts and dimensions, required metadata copy, original source assets and font licences, persisted byte-identical copied-package renders, actual edited-pixel locality, and freshly rerun strict raster QA. All18 technical file audits pass. Localized edits and copied renderers provide evidence of editability, not general portability across OS/rasterizer versions. Technical metadata is not OCR or a visual approval.

Quota interruptions preserve partial work and attempts; resumed workers continued the same trials. No result was discarded or rerun to seek a win. Worker records retain visual limitations, including a frozen-rc5 product carousel below its own visual shipping rubric at its correction limit. The coordinator did not improve weak held-out results after exposure.

The final human ballot was supplied on 19 October 2026 and the frozen rc2 candidate **FAILS**: 1/6 wins against the no-skill baseline, 2/6 against rc5, and 2/6 absolute quality approvals (H1 and H6, with qualitative reservations). There is no approved carousel. Required thresholds remain ≥5/6 against EACH comparator, ≥5/6 absolute quality, and at least one approved result per family. A preferred result is not necessarily acceptable; H4 has a preferred condition but no absolute approval.

Human ballot SHA256: `1d9c436a37a5d90b730c5460b0963e89bcc142c467e48f371e4a7129db941c24`. The user-supplied ballot, label map, score and frozen originals remain in the private evidence workspace. Blank votes and ties were not converted to wins. The original human notes remain separate from computed counts.

H1–H6 are now exposed. Any reuse for reference analysis or corrections is development, never another held-out success. New source changes do not alter the frozen rc2 skill or its result. See [post-ballot composition audit](research/composition-client-audit-2026-10-19.md).

The technical audit above checks supplied original bytes and reproducible edits. It does **not** prove proportional logo application, OCR fidelity, preservation of recognisable product parts, or photographic attractiveness. A follow-up manual audit found nonuniform logo resize calls and an already-cropped bread source; these qualify the previous technical scope rather than erase its recorded tests.

`score_blind.py` consumes a user-supplied ballot, the separately stored label map and a technical report. The caller must verify human provenance; a JSON human flag is not proof. The script does not publish or merge. Seven unit tests cover threshold, ties, separate comparators, blank votes, technical failure and invalid maps/votes.

```sh
python3 evals/art-direction/score_blind.py HUMAN_BALLOT.json PRIVATE_LABEL_MAP.json --technical-report TECHNICAL_REPORT.json
```

Exit0 means the supplied evidence meets the gate;1 means pending/fail;2 means invalid input. Keep ballot, label map, source images, failed attempts and audit report together in the private evidence package, outside the public skill.
