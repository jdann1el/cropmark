# Spec — Paso 10: John's Paso 9 feedback

Frozen 2026-10-25. Candidate trial; no validation, causality claim or gate change.

## In

`S10` = `evals/art-direction/diagnostic-2026-10-22/renders/step10/`. Reuse real generated assets/code with provenance. Baselines: carousel **B2**, thumbnail **B-R1**, flyer **A**.

| Requirement | Acceptance evidence |
|---|---|
| Human feedback | New `docs/human-feedback-paso9.md`, dated 2026-10-25, source John, preserves all three preferences/reasons in meaning. |
| Candidate rules | Add surface-bound typography to `skills/cropmark/techniques/{typography,imagery}.md` and measured plane QA to `skills/cropmark/qa/checklist.md`. Every added rule is **CANDIDATE / unvalidated**. |
| Physical surface case | Record four measured surface corners, homography, projected type bounds and safe inset ≥5% of the rectified surface dimensions. Independent corner/plane alignment residual MUST be ≤max(3 px, 0.5% of the surface's short edge) at master size. Type MUST inherit substrate lighting/shading and subtle print texture. Record integration evidence and judge whether it reads as printed. |
| No surface case | Declare per piece; flat type MUST occupy a clean copy zone. |
| Thumbnail C1 | 1280×720; preserve B-R1's scene concept and exact four-word headline `3 AIs. 1 Portfolio.`. C MUST match/exceed A's measured visible cap height as a percentage of frame height and exceed B-R1's; compare A/B/C using the same glyph method. Measure normalized stem weight and inspect headline dominance at 168 px. Keep essential content ≥40 px from edges and outside the lower-right duration zone (18%×15%). |
| Flyer C2 | 1080×1350; exact copy `Noche de vinilos · Sala Taller · 14 nov · 21:00`. Apply the physical-surface case. Title MUST be heavier than metadata, with cap height ≥24 px at 360 and ≥1.75× metadata. Metadata cap MUST be ≥14 px at 360, grouped coherently; no line starts or ends with `·`. |
| Carousel B4 | Three 1080×1350 slides; preserve B2 palette, contrast approach and no shadows. Use three distinct layouts; record each relationship. Headline-to-body gap MUST be ≤one headline cap height. Small copy cap MUST be ≥14 px at 360. Only final `MIRA LAS PIEZAS` gets thin underline/arrow CTA treatment; no boxes/pills. |

Carousel copy, in order; slash denotes a line break. Brand `TALLER BARRO` and descriptor `CERÁMICA` remain on every slide.

| Slide | Headline | Support | Action |
|---|---|---|---|
| 1 | La forma / toma cuerpo. | Una pieza empieza con un gesto. | EXPLORA EL TALLER |
| 2 | Del giro / nace el borde. | El torno acompaña cada movimiento. | SIGUE EL PROCESO |
| 3 | Cada huella / deja memoria. | Un rastro queda en la superficie. | MIRA LAS PIEZAS |

Scenario: GIVEN a photo surface, WHEN copy sits there, THEN measured perspective, inset and substrate integration MUST pass; otherwise clean-zone flat type applies.

Scenario: GIVEN all final candidates, WHEN inspected at 168/360 px and independently measured, THEN copy, hierarchy, layout variation and technical evidence MUST satisfy the table; technical PASS alone MUST NOT imply aesthetic success.

## Out

No 18-run benchmark, merge, publication, new branches, reference-image/CDN imports, or QA threshold/code changes. Never stage Step 3's `qa-report.json/` or `__pycache__`. The feedback JSON MUST remain byte-identical: SHA-256 `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`.

## Done

Max **8 image_gen calls globally**, including failures; log exact prompts/status/assets in `S10/imagegen-log.json`. Max **3 QA/correction rounds per piece**, recording defects and outcomes. No clipping, forced justification, default shadows, dark-on-dark type or boxed/pill CTAs. Run strict format QA; glyph-core contrast P05 ≥3:1 for large headlines and ≥4.5:1 for small copy.

Required comparisons: `S10/thumb-ABC.png` plus 168/360 versions; `S10/flyer-AC.png` plus 360 version; `S10/carousel-B2B4-feed.png` (B2/B4 rows) plus 360 version. Cells MUST derive from real finals.

**gpt-6.1-sol/high** owns spec/final verdicts: whether C/B4 beats its baseline and remaining Behance-level gaps. **gpt-6-luna/high** owns separate generation, composition, documentation and QA tasks; parallel writers use detached worktrees. **gpt-6-luna/low** handles copying/contact sheets/staging. A fresh **gpt-6-luna/high** verifier re-measures independently. No Astra. Integration MUST follow the user's approval, identity, single-command staging and branch-only push instructions; verify HEAD equals origin. Save memory only after the user's approval.

## Final verification and verdicts — 2026-10-26

All three strict format QA runs pass (thumbnail C, flyer C, carousel B4 3/3). The comparison boards open at their expected dimensions: `thumb-ABC.png` 3840×720, `flyer-AC.png` 2160×1350, and `carousel-B2B4-feed.png` 3240×2700; feed previews are 1080×203/504×95, 720×450, and 1080×900 respectively. The independent in-session checks re-read the final files, remeasured the shared thumbnail P glyph, recomputed flyer plane margins and corner alignment from the clean source, recalculated carousel gaps/caps from final sidecars/fonts, and confirmed the protected feedback hash. Technical PASS is separate from these visual verdicts.

| Piece | Verdict against Paso 9 winner | Evidence and remaining gap to Behance-level |
|---|---|---|
| Thumbnail C vs B-R1 | **C wins.** It keeps B-R1's three-agent/one-portfolio scene and gives the headline A-level mass. | The common P cap is 126 px / 17.500% of frame for A, 66 px / 9.167% for B-R1, and 143 px / 19.861% for C; normalized P fill is 0.6613 / 0.5794 / 0.6721. At 168 px, C's P cap is 18.77 px and dominates. Cream-on-dark contrast passes; there is no clipping. Remaining gap: the large line crowds some of the robot/board action, and the scene still reads more like a physical board than a digital portfolio. |
| Flyer C vs A | **A remains stronger overall; C closes the surface-integration gap but does not beat A.** | C's title and metadata are perspective projected on the measured sleeve and inherit its light/grain; independent corner residuals are 0.59/2.20/1.16/0.20 px against a 3.4 px limit. Minimum transformed text inset is 38.83 px against 34 px required. Feed caps are 27.33 px title and 15.33 px metadata (1.783×); the full supplied copy is present on one title line plus one grouped metadata line, with no line ending in `·`. Remaining gap: A's lettering feels more naturally composed on the sleeve; C's leading separator reads somewhat like a bullet and its bold treatment is less nuanced. |
| Carousel B4 vs B2 | **B2 remains stronger overall; B4 does not beat it.** | B4 keeps B2's palette/contrast, uses three distinct layouts, has headline/body gaps of 53/58/35 px against headline caps of 59/70/73 px, keeps small-copy caps at ≥14 px at 360, and treats only the final CTA. No shadows, clipping or dark-on-dark copy. Remaining gap: B4's separate photo windows/flat fields feel more segmented than B2's cohesive imagery and type rhythm; subtitle sizes sit at the minimum. |

R1 used one correction per affected piece (thumbnail weight, flyer grouping/hierarchy, carousel slide 1 gap). Image generation calls: **0/8**. No surface is invented for the thumbnail or carousel; their copy remains flat in clean zones. All three added surface-bound rules are **CANDIDATE / unvalidated**. This trial does not validate Cropmark or claim causal improvement.

Independent verification evidence: `S10/qa/independent-verification.md`. Protected SHA-256 remained `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`.
