# Paso 11 verification checklist and acceptance evidence

Evidence root: `evals/art-direction/diagnostic-2026-10-22/renders/step11/`. A measured judgment marked unresolved is FAIL under the spec; it is not N/A.

## Separate verifier checklist

1. **PASS** — protected feedback SHA-256 `31a2…fb38` matched before/after; Git remained limited to untracked spec, S11 and pre-existing excluded Step 3 path; imagegen ledger has 6/6 successful hashes; correction logs R1–R3 (3/3). No excluded files were edited.
2. **FAIL / PARTIAL** — reused Paso 9 A source-to-final normalization matched decoded pixels for thumbnail and flyer; carousel sources matched normalized finals and revised copy. Prompts/logs have no references; fresh baseline scope is claimed in `baseline/session-scope.md`, but source-session transcript/context is unavailable. Unknown prior familiarity/provenance remains explicit.
3. **PASS** — five candidate finals, comparator images, three master boards and all feed previews opened. Dimensions/hashes match manifest. All board cells equal their expected source/resample; flyer cells 1–2 are identical; external label bands and historical B2 “three action lines” label are present.
4. **PASS** — before reveal, thumbnail transcribed `3 AIs. 1 Portfolio.` at 168/320/360; flyer `Noche de vinilos`, `Sala Taller · 14 nov · 21:00` at 360; each carousel headline/support/brand/descriptor read at 360. Story read: three agents on one shared portfolio. Observations are in design verdict.
5. **FAIL** — thumbnail ink-to-subject gap estimate 100 px (limit 32), overlap 0; P cap 129 px (limit 126), fill 0.6857 (limit .6613), kicker 10.76 px at 168 (limit 10), duration intersections 0. Portfolio board starts y=29 px (<40 safe-zone limit); glyph-core contrast not independently completed.
6. **FAIL / unresolved** — independently fitted sleeve corners TL(37,230), TR(602,301), BR(611,845), BL(83,795); top/bottom edge angles 7.16°/5.41° and keystone 4.02% pass. Corner residual tolerance is max(3 px, 0.5% short edge); hand-fit uncertainty is about 3 px, so residual is not certified. Title baseline estimate 3.76° (<5°); line residuals ≤3 px not established.
7. **FAIL / unresolved** — copy is legible at 360 with exactly two separators and no leading/trailing separator line; three paired 100% crops show pigment following paper texture. Independent plane insets are about 60.3/58.8 px horizontal and 120.3/219.1 px vertical (50 px minimum); glyph-core P05 is 6.45/6.19 title and 5.71 metadata. Title cap is visually about 34 px at 360; metadata about 13 px (<14), conservative projected cap ratio not verified.
8. **PASS** — pixel review CTA counts 0/0/1; both removed phrases occur 0 times. Slides 1–2 have no apparent action; slide 3 uses one unboxed underlined CTA and no pill.
9. **FAIL** — full-bleed photo mask reaches four edges on all slides (100%); closing material bbox estimate is 36.1%. Trace estimate is 25 px at 360 /75 px master (<90). Independent grid estimates: empty cells 27.6/28.8/19.4% (each ≤35); largest components 17.2/24.8/11.4% (slide 2 >20). Raw grids and overlays saved.
10. **FAIL / PARTIAL** — font-derived 360 caps: headline 30.67 px on slides 1–2, 28.67 px slide 3; support 15.33 px; brand 14.33 px; descriptor 13.33 px (<14); CTA 14 px. Slide 3 headline/support ratio about 1.87 (<2). Brand top ink about 60 px (<64). Two distinct image/headline relationships are visible. Zero clipped copy was visually seen; slide 1 support approaches a tool cup; slide 2 headline is low contrast against teal.
11. **FAIL** — glyph-core linear-sRGB P05/median/share below 4.5%: S1 brand 5.82/11.77/1.3, descriptor 4.16/8.80/10.08, headline 6.96/10.27/0, support 10.63/12.49/0; S2 brand 8.33/12.74/0, descriptor 9.47/11.63/0, headline 1.05/8.63/23.8, support 8.39/9.82/0; S3 brand 11.20/12.91/0, descriptor 11.70/13.03/0, headline 12.77/13.93/0, support 13.39/14.74/0, CTA 8.02/9.89/0.7. S2 headline is below its 3:1 target; S1 descriptor is below 4.5:1. Thumbnail P05 is unresolved. No cutoff, default shadow, box/pill on candidate slides 1–2, or forced-justified short line was visually observed.
12. **FAIL / PARTIAL** — strict QA commands exit 0 with counts 1/1/3. No applicable contract JSON exists for `design_check.py`. T14 reproduction failed because package, reproduction.md and handoff manifest are absent.
13. **FAIL / PARTIAL** — blind preferences recorded before key; each format has four visible observations in `design-verdict.md`. Direct comparison results 2 wins/1 loss; owner comparison 1 win/1 tie/1 loss. No two suitable local reference IDs per format; absolute level unverified. Verification ordering was compromised by opening manifest/key/plane measurements before completing automated pixel measurement.

## Acceptance criteria — thumbnail

- **PASS** Canvas/count/copy: `thumbnail/final.png` is 1280×720; visible copy is exact.
- **PASS** Subject separation estimate: min ~100 px (≥32), zero overlap; all three complete agents and board kept visible.
- **PASS** Headline mass: common P visible height 129 px (≥126); connected P fill .6857 (≥.6613); counters open on visual review.
- **PASS** Secondary line: `3 AIs.` ~10.76 px at 168 (≥10); portfolio P equivalent ~16.9 px at 168 (≥16.54).
- **FAIL** Safe zones: portfolio board top y=29 px (<40); text and other subjects appear clear of duration box x≥1049.6,y≥612 (0 intersections).
- **PASS** Read/story: four words transcribed at 168/320/360; three agents and one shared portfolio recognized at 168; redesign activity visible at 360.

## Acceptance criteria — flyer

- **PASS** Canvas/content: 1080×1350; exact title/metadata read; 2 separators, 0 leading/trailing separator line.
- **FAIL / PARTIAL** Visible angle: sleeve top/bottom 7.16°/5.41° same sign; title first baseline estimate 3.76° (<5°), metadata ~5.71°; noisy fits prevent clean pass.
- **PASS, borderline** Keystone: L=566.9 px, R=544.1 px; ratio 4.02% (≥4%).
- **FAIL** Independent corner fit: own manual corner uncertainty ~3 px reaches the max tolerance; no independently robust residual proof for all four corners.
- **FAIL** Type-plane fit: title baseline rectification ≤1° and line residual ≤3 px not established.
- **PASS** Plane inset: rectified horizontal 58.8–60.3 px and vertical 120.3–219.1 px; all ≥50 px.
- **FAIL / PARTIAL** Hierarchy: title cap visually ~34 px at 360 (≥32); metadata ~13 px (<14); conservative title/metadata cap ratio not established.
- **PASS visually** Print/material: ink reads as printed; 3 paired light/midtone/dark crops opened; visible grain; no shadow/sticker/backing seen.
- **PASS** Legibility: exact title, venue, date and time transcribed at 360; platter, grooves and tonearm recognizable.

## Acceptance criteria — carousel

- **PASS** Canvas/count/copy: exactly three 1080×1350 finals; accents and strings read correctly; no slash or removed phrase.
- **PASS** CTA semantics/style: pixel count 0/0/1; exact `MIRA LAS PIEZAS` on slide 3; 1.67 px feed underline; no boxes/pills; no first/second action.
- **PASS** Continuous image space: all slides 100% full-bleed photo and all four frame edges reached.
- **FAIL** Closing scale: bbox estimate 36.1% (≥25%); trace 75 px master (<90).
- **FAIL / PARTIAL** Empty area: empty cells 27.6/28.8/19.4% (≤35); largest component 17.2/24.8/11.4% (slide 2 exceeds 20).
- **FAIL** Hierarchy/readability: headline caps 30.67/30.67/28.67 px; support 15.33 px; descriptor 13.33 px (<14); slide 3 cap ratio 1.87 (<2); S2 P05 1.05:1 (<3); S1 descriptor P05 4.16:1 (<4.5).
- **FAIL** Safe placement: brand top ink y≈60 px (<64); no clipped required copy seen; slide 1 support has near contact with a tool cup and slide 2 headline low contrast.
- **PASS visually** Rhythm/coherence: at least two distinct relations: left type in teal negative field with working form on right (S1), and type crossing the teal/table transition beside wheel/process (S2); shared palette/type roles visible.

OVERALL: FAIL
