# Changelog

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
