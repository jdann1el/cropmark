# Frozen held-out validation — technical evidence, human gate pending

Candidate art-direction-rc2 was frozen at cc36200d787d3500a56734052f669376f9b7e910 before six new briefs were authored. H1/H2 are thumbnails, H3/H4 four-frame carousels, H5/H6 three-post campaigns. Each ran once with no design skill, frozen rc5 and frozen rc2:18 trials,48 final PNGs. Native requested configuration:gpt-6.1-sol,low. Served telemetry and complete costs are unavailable.

All conditions had identical supplied imagery/logos/fonts, neutral rendering mechanics and an offline visual study bank. Reference captures were for study only, not output assets. This differs from the initial calibration's text-reference limitations; the two phases must not be pooled as one experiment. Four conceptual photographs were generated once before trials and shared byte-for-byte; the real supplied shaker and its printed identity were retained. Autonomous imagery sourcing/generation inside trials was not tested.

The coordinator verified all frozen source/input/brief hashes, exact PNG counts and dimensions, required metadata copy, original source assets and font licences, persisted byte-identical copied-package renders, actual edited-pixel locality, and freshly rerun strict raster QA. All18 technical file audits pass. Localized edits and copied renderers provide evidence of editability, not general portability across OS/rasterizer versions. Technical metadata is not OCR or a visual approval.

Quota interruptions preserve partial work and attempts; resumed workers continued the same trials. No result was discarded or rerun to seek a win. Worker records retain visual limitations, including a frozen-rc5 product carousel below its own visual shipping rubric at its correction limit. The coordinator did not improve weak held-out results after exposure.

Final human review is pending. Anonymous labels are balanced across groups; every condition occupies A/B/C twice. The ballot asks all three pairwise preferences and absolute reference-quality approval separately. Blank votes remain pending; ties/neither are not wins. Release requires ≥5/6 candidate wins against EACH comparator, ≥5/6 absolute approvals, an approved case per family, and technical/editable correctness. No acceptance or claim of superiority is established yet.

`score_blind.py` consumes a user-supplied ballot, the separately stored label map and a technical report. The caller must verify human provenance; a JSON human flag is not proof. The script does not publish or merge. Seven unit tests cover threshold, ties, separate comparators, blank votes, technical failure and invalid maps/votes.

```sh
python3 evals/art-direction/score_blind.py HUMAN_BALLOT.json PRIVATE_LABEL_MAP.json --technical-report TECHNICAL_REPORT.json
```

Exit0 means the supplied evidence meets the gate;1 means pending/fail;2 means invalid input. Keep ballot, label map, source images, failed attempts and audit report together in the private evidence package, outside the public skill.
