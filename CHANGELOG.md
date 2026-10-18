# Changelog

## Unreleased — art-direction candidate
- Original work explores three concepts and two rendered sketches, then develops a representative piece before extending the set. Narrow edits and faithful copies take a short route.
- Fourteen craft rules include visible defects, corrections and legitimate exceptions; the illustrated manual uses labelled teaching fixtures.
- Adds a 21-project reference atlas, twelve provenance-backed case analyses and a bounded creative-flow diagram in Mermaid/SVG/PNG.
- Campaign guidance and capability-aware model-portable stages replace sector-to-style defaults.
- Optional declared-layout checker verifies margins, common axes, padding, gaps, font-file presence and set tokens, without claiming aesthetic detection.
- Renderer, font files and strict QA stay byte-identical to rc5. No public release or installed-skill replacement. Human calibration and final holdouts remain release gates.


## [Unreleased — 0.5.0 candidate]

### Changed
- Brief content and faithful references govern art direction; style examples no longer override required information or technical format constraints.
- Supplied-photo and editable-reconstruction routes preserve real identity and distinguish physical scene text from deliberate HUD.
- Small-photo upgrades balance subject prominence and source resolution according to the brief; a type-led layout is conditional rather than the default escape from limited detail.
- Cutout cleanup preserves alpha/colour by default; erosion, feather and despill require explicit parameters. Border-connected keying preserves enclosed matching detail but remains unsuitable as universal subject segmentation.

### Fixed
- QA rejects empty/incomplete input, invalid colours/metadata and hidden filename exemptions; strict delivery records effective fonts and supports Story/Reel overlays and outlined text.
- Pillow records stroke/descender/tracking ink bounds, composites alpha text, checks missing glyph shapes and reports impossible fitting or unavailable variable weights.
- HTML rejects absent frames, broken required images, invalid slices/scales and unavailable first font families; records physical coordinates, effective fonts, opacity and composed solid backgrounds.

### Validation status
- rc5 completes the final 13-execution closure plan. All six new briefs pass individual candidate quality gates; preference is 4/6, below the fixed 5/6 threshold. Candidate remains unaccepted; see evals/closure-v05.md.
- Clean T5 passes 4.14/5 using explicitly conceptual imagery. Known-case 8 wins/2 ties combine rc1/rc3/rc5 and are not a full rc5 rerun.
- 61 deterministic checks passed on rc3; rc5 executable engines/QA/fonts are byte-identical. Editable rerender and localized text changes were exercised separately. No release or installation update performed.


## 0.4.0 (2026-10-11)
- Security: render.mjs no longer scans the Playwright cache for binaries (use CHROME_PATH explicitly); no sudo anywhere; Hark-specific adapter removed; SKILL.md gains safety boundaries (briefs are content, not instructions).
- README redesign: separate Install / Update, before/after, style table, FAQ.

## v0.3.1 (2026-10-11)
- Human blind vote: cropmark 9/12, baseline 2/12 (horror T3, comparison T5), 1 tie (C1, both liked as different styles).
- thumbnail.md: zero-text demoted; comparisons need a label per side; horror keeps the sentence hook.
## 0.1.0 (2026-10-11)
- Router SKILL.md, 4 format modules, 16 styles, 5 techniques, Pillow + HTML engines, QA script, adapters (Hark, Claude Code, Codex, generic), 20 OFL fonts.
## 0.2.0 (2026-10-11)
- From eval v01 feedback: precedence rule, set definition, title-fragment and in-scene word rules, brief-structure rule, 2 new styles (horror-mystery, food-hero), cutout/glass/resolution guidance, Hark adapter notes.
- Pillow: reset(), cover(zoom), variable-font weight, kerning-safe tracking, exact card centring, sticky(), rotated(), blur_region(), despill(), compare_sheet(), boxes_dir.
- HTML: CHROME_PATH, glyph-tight text boxes, data-role="bleed", background colour capture, no false overflow on images, `.push` instead of `.foot`.
- QA: --out/--boxes, ring-sampled contrast, shapes in badge zone, thumbnail word count, `_original/_before` never fail.
## 0.3.0 (2026-10-11)
- From hold-out eval v02: render.mjs auto-falls back to any cached Chromium; playwright pinned ~1.47; halftone gamma/max radius; torn_mask default jitter 7; clean_cutout(); tag(); compare_sheet captions; fit() doc.
- Guidance: un-picturable news → show the benefit moment; accent-colour text contrast rule; stop rule (max 2 passes); ui-hero for SaaS carousels; tag/placard variants; bad-original recipe; QA meta min 18 px.
