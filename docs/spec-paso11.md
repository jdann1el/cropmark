# Spec — Paso 11: clear subjects, credible print, one CTA, honest controls

Frozen for implementation on **2026-10-26**. Source of owner review: **John + orchestrator, 2026-10-26**. This document specifies future work; it does not report that work as completed. The spec writer inspected the Paso 10 full boards and their 168/360 px previews directly.

`R` = `evals/art-direction/diagnostic-2026-10-22/renders/`; `S11` = `R/step11/`. All abbreviated output paths below are relative to S11. Earlier artifacts are read-only.

## In

- Improve three fictional briefs: one 1280×720 portfolio thumbnail, one 1080×1350 vinyl-event flyer, and one three-slide 1080×1350 Taller Barro carousel.
- Start from the **owner's Paso 10 winners: thumbnail C, flyer A, carousel B2**. Winner means preferred in that review; none has Behance-level approval. Flyer A and B2 originate in earlier pasos but remain the winners selected at Paso 10.
- Correct subject/type collisions, visible sleeve perspective and title hierarchy, and carousel fragmentation, empty space and repeated apparent CTAs. Reuse clean generated assets before requesting new ones.
- Compare each piece against a documented **NO-SKILL direct-generation baseline**, with the same communication brief, required copy and facts. Keep the actual Paso 10 winner unchanged as a second comparator.
- Preserve reproducible candidate compositions, exact prompts, provenance, measurements, boards and a verification report from a **separate fresh session**. No parallel agents or subagents.

## Out

No implementation, rendering, image generation, code changes or commits by this spec-writing session. Later builders may create compositions and evidence only under S11. No edits to Cropmark skill files, QA code/thresholds, prior renders, acceptance ledgers or historical feedback in this paso. The surface rules added in `efe56a4` remain **CANDIDATE / unvalidated**.

No 18-run benchmark, general validation of Cropmark, causal attribution, CTR claim, merge, publish, deployment, push, branch creation or checkout to other branches. No paid provider/model API setup or fallback generator. Existing local fonts/assets may be read; reference pixels may be studied but never incorporated into deliverables.

## Evidence and baseline decision

Read inputs: the supplied AGENTS.md instructions (no on-disk AGENTS.md found in the repository/ancestor locations checked), `docs/spec-paso10.md`, `docs/human-feedback-paso9.md`, Paso 10 boards, measurements, surface/layout evidence, correction log, strict QA reports and `qa/independent-verification.md`. Also reviewed the `efe56a4` changes to `skills/cropmark/techniques/{typography,imagery}.md` and `skills/cropmark/qa/checklist.md` and the earlier direct-generation prompts/render paths.

Owner findings override the optimistic Paso 10 report: C crowds/overlaps the lower-right robot; flyer C starts metadata with `·` and looks nearly flat; B4's separate windows weaken continuity, slide 3 has a small image in a large dark field, and the first two uppercase actions still read as CTAs. Paso 10's verification document explicitly says it ran in the main session; it does **not** satisfy this paso's independent-session requirement.

| Piece | Existing A provenance checked | Decision for the required NO-SKILL row/cell |
|---|---|---|
| Thumbnail | `step9/prompts.md`, global call 4; `step9/imagegen-log.json`; `step9/thumbnail/A-source.png` → `A.png` via raster normalization in `render_s9.py`. Prompt requests a finished image with the headline; no Cropmark invocation, supplied rules, reference image or editable overlay in this condition. Source SHA-256: `f9dccd716e68b698df332970069358ee49d13090b2c5534bb617e535a657858a`. | **Reuse `step9/thumbnail/A.png`** after T1 verifies the source hash and normalization. Its tokens/folio and C's robots/grid are different creative responses to the same video premise, not matched imagery. |
| Flyer | Same files, global call 6; `step9/flyer/A-source.png` → `A.png`. Direct finished raster, not a Cropmark composition. Source SHA-256: `76565aa408da02828f77856dee40bd1c3c07fcf7369e18e0241e1d50020cc73f`. | **Reuse `step9/flyer/A.png`**. This is also the owner's Paso 10 winner. The first two board cells must therefore be identical, honestly labelled; do not invent another winner to hide that the direct condition won. |
| Carousel | `step7/A/prompts.txt`, `A/slide-1.png`…`slide-3.png`; `render_step7.py` only fits these direct finals to `A/final-1.png`…`final-3.png`. Historical A is genuinely direct generation at the prompt/output level. It includes all three old action strings; the inspected row also contains pill treatments. | Preserve historical A as provenance, but **generate a new three-slide direct baseline** for the revised one-CTA copy below. Historical A is not a matched control for the revised brief. Do not remove its CTAs by retouching and call that no-skill. |

Here NO-SKILL means a direct finished image generated from the content brief without supplying Cropmark instructions, rules, reference studies, sketches, typography layers or render code. The records support that operational distinction; they do not prove that the historical prompt author had never read Cropmark. Record that limitation. T1 must flag any contrary evidence; an unsupported baseline must be replaced within the same six-call cap or marked **comparison incomplete**, never silently certified.

The new baseline operator uses a fresh Herdr session containing only the neutral content brief and image-generation tool instructions. Do not give it this specification's design thresholds, owner critique, winner images or Cropmark materials. The one-CTA copy/count is a shared brief requirement, not a secret advantage for the candidate. Preserve baseline defects and first successful outputs; no aesthetic rerolls or post-generation lettering repair. Only recorded aspect-ratio normalization and equal preview resampling are permitted.

JEV was consulted once on a synthetic summary of the comparison protocol, with no recalled memories supplied. It recommended reuse for unchanged briefs plus a new matched carousel control: score 80.5, confidence 0.523; alternatives all-new 33.1 and all-historical 27.3. This is methodological advice, not visual verification or objective proof.

## Frozen content

| Piece | Required content and facts |
|---|---|
| Thumbnail | Video premise: `I let 3 AI agents redesign my portfolio`. Printed headline exactly `3 AIs. 1 Portfolio.`; four words, no other copy. Three distinguishable agents act on one shared portfolio. No winner, fabricated outcome, metrics or before/after claim. |
| Flyer | Fictional Barcelona listening event. Title `Noche de vinilos`; metadata `Sala Taller · 14 nov · 21:00`. All four semantic units remain in order. The separator between the title and metadata is replaced by the group/line break; only the two internal metadata separators are printed. No address, price, year, performers, availability or ticket claim. |
| Carousel, every slide | Brand `TALLER BARRO`, descriptor `CERÁMICA`. Preserve Spanish accents and the headline/support strings below; `/` means a line break and is never printed. |

| Slide / role | Headline | Support | Action |
|---|---|---|---|
| 1 / form | La forma / toma cuerpo. | Una pieza empieza con un gesto. | **None. Remove `EXPLORA EL TALLER`.** |
| 2 / process | Del giro / nace el borde. | El torno acompaña cada movimiento. | **None. Remove `SIGUE EL PROCESO`.** |
| 3 / trace and close | Cada huella / deja memoria. | Un rastro queda en la superficie. | `MIRA LAS PIEZAS` |

Removal is the selected owner-permitted remedy, shared by the new NO-SKILL carousel and Paso 11. Do not retain sentence-case imperatives as additional apparent actions. The untouched B2 comparison row retains its historical copy and must be labelled **historical copy: three action lines**; use the new direct row, not B2, for the same-brief value comparison.

## Measurement contract

All numeric limits below are frozen **Paso 11 acceptance requirements**, not newly validated universal design rules. Candidate finals must pass; comparators are measured honestly and may fail. Never repair or weaken a comparator to create a win.

- Coordinates are master-image pixels, origin top-left; boxes are `[left, top, right, bottom]`. Save text alpha masks, clean pre-type backgrounds, subject polygons/bboxes, fonts and transforms. Measure visible ink, not font size, advance width or transparent padding. Use alpha ≥0.5 for ink bounds and ≥0.98 for glyph-core contrast; report segmentation uncertainty for raster controls.
- Gap between a text group and a subject is the shortest Euclidean distance between its ink and that subject's tight visible bbox, zero for overlap. Include complete robot silhouettes/limbs and the portfolio board as subjects; do not shrink a box to exclude an inconvenient part. Supply an annotated overlay and the closest pair of coordinates.
- Cap height uses the same rendered uppercase test glyph for comparisons: common visible `P` for the thumbnail; an `H` rendered through the actual font/transform at each group's local position for other pieces, cross-checked against final letter pixels. For perspective text report minimum/maximum local cap height across the group. Never substitute rectified-plane cap height divided by three for the projected measurement.
- Preview sizes: thumbnail **168×95**, **320×180**, **360×203**; flyer/carousel **360×450** per image. Render from the final PNGs with the same Lanczos resampling, without sharpening or enlarged text. Assess at 100% display size, without zoom or captions. Use 168 px for thumbnail headline/subject recognition; the flyer and carousel require every word at 360 px, not microscopic metadata at 168 px.
- For each candidate text group, compute linearized-sRGB glyph-core contrast against the actual clean background and final integrated ink. **P05 ≥3:1 for large headlines, ≥4.5:1 for all small copy**; record median and percentage below target too. Region averages or QA's surrounding-background estimates are insufficient. Reading failure overrides a passing statistic.
- No cut-off, obscured or missing required text: **0 clipped/occluded required-ink pixels**. Short lines use natural left/center alignment: no forced justification or stretched word spaces. No drop shadows by default, no dark text on dark areas, no strokes used to rescue contrast, no boxed/pill CTAs. Physical lighting/shadows already in photographs are permitted.

## Per-piece fixes and acceptance

### Thumbnail — preserve C's idea and mass, clear all subjects

Reuse `step9/thumbnail/B-base-R1-source.png` and the controllable C composition in `step10/thumbnail/render_thumb_c.py` as inputs. Reposition/reframe the scene and headline to create a real copy zone. Do not solve the collision by hiding the robot, deleting an agent, shrinking the headline below the A benchmark or blanking the portfolio. Flat type remains appropriate; do not invent a photographed plane.

| Check | Required candidate result |
|---|---|
| Canvas/count | One **1280×720** final; headline exactly `3 AIs. 1 Portfolio.`. |
| Subject separation | Minimum ink-to-**every subject bbox ≥32 px** at master size (4.2 px at 168, 9 px at 360). **0 overlap** and no near-tangency at feed size, including the lower-right robot. |
| Headline mass | Visible common `P` cap **≥126 px** and **≥17.5%** of 720; normalized P ink fill **≥0.6613**, measured by the same connected-component method as `step10/thumbnail/measurements.json`. Retain open counters; weight tricks that merge letters fail visual review. |
| Secondary line | `3 AIs.` cap **≥10 px at 168**; the `1 Portfolio.` P cap is ≥16.54 px at 168 from the benchmark above. Both lines remain one coherent headline group. |
| Safe zones | All essential type/subject detail **≥40 px** from frame edges and outside lower-right duration rectangle **x ≥1049.6, y ≥612** (18% W ×15% H). Measure in float coordinates; no rounding exemption. |
| Readability/story | Fresh verifier transcribes all four words correctly at **168, 320 and 360 px**, identifies **three agents and one shared portfolio** at 168, and locates their redesign activity at 360. Record the unassisted reading before showing rationale. |

Outputs: `thumbnail/final.png`, `thumbnail/final-{168,320,360}.png`, editable composition source, `thumbnail/final.png.boxes.json`, masks/subject annotations, and `thumbnail/measurements.json`. Comparison: **`thumb-board.png`** plus `thumb-board-{168,360}.png`, ordered NO-SKILL A → Paso 10 winner C → Paso 11.

### Flyer — A remains the craft target; make sleeve typography visibly physical

Use A as the visual benchmark, not as an editable text-free base. First inspect/reuse `step9/flyer/B-base-source.png`; the old C plane is almost frontal, so an accurate homography alone does not satisfy this brief. Use a coherent whole-scene reframe/projective treatment only if credible and safe, otherwise spend a reserved call on a new clean sleeve scene. Never tilt only the text, falsify sleeve corners, or erase A's raster letters and imply an untouched source.

Corners are ordered TL, TR, BR, BL. Fit the visible sleeve edges from the **clean source image**, record occluded-edge extrapolation and its uncertainty, then map through the recorded crop/resize to final coordinates. Let L/R be the lengths of the left/right sleeve edges in the final image.

| Check | Required candidate result |
|---|---|
| Canvas/content | One **1080×1350** final; exact title and metadata from the frozen content. **0 lines starting or ending with `·`** after trimming whitespace; no isolated dot; exactly **2** printed metadata separators. Check final pixels as well as source strings. |
| Visible angle | Sleeve's top and bottom edges each have absolute angle **≥5° to horizontal**, with the same slope sign. Projected title and metadata baselines also each show **≥5°** visible inclination. Rotation alone does not satisfy the next check. |
| Visible keystone | **abs(L−R)/max(L,R) ≥0.04**. Record L/R and top/bottom widths, not just an angle label. The source sleeve and its printed type must visibly share that plane. |
| Independent corner fit | For **each** final corner, verifier-vs-builder residual **≤max(3 px, 0.005 × final sleeve short-edge length)**. Measure using separately fitted source-image edges; record all four residuals. A transform's own round-trip/reprojection residual is not independent evidence. Uncertainty exceeding the tolerance means unverified. |
| Actual type-plane fit | Inverse-project observed title/metadata baselines using the independently fitted plane: each baseline deviates **≤1°** from rectified horizontal. Its sampled endpoints/midpoint deviate from the declared projected line by **≤3 px** at master size. Record projected text quadrilaterals and at least **3 samples per baseline**. |
| Plane inset | Every projected text-ink point lies inside the sleeve. In the rectified plane: horizontal inset **≥5% of plane width**, vertical inset **≥5% of plane height**, on all four sides. Also keep required ink **≥64 px** from image edges. |
| Hierarchy | Minimum projected title cap **≥32 px at 360**; minimum metadata cap **≥14 px at 360**. Conservative title/metadata cap ratio **min(title caps)/max(metadata caps) ≥2.25**. The event title is the first typographic read; no horizontal squeezing or forced justification of metadata. |
| Print/material | Ink inherits sleeve shading and fine grain, with **0 cast-shadow layers**, sticker outlines or opaque backing panels. Save clean sleeve, ink mask and integration layers; show **3 paired 100% crops** (light, midtone, darker sleeve region). Verifier must judge “printed on sleeve” at master and 360; metrics alone cannot pass this check. |
| Legibility | Fresh verifier transcribes title, venue, date and time with **0 word/number errors at 360** and confirms the title dominates the metadata. Vinyl grooves, platter and tonearm remain recognisable. |

Outputs: `flyer/final.png`, `flyer/final-360.png`, editable source, `flyer/final.png.boxes.json`, masks/paired crops and `flyer/surface-evidence.json`. Comparison: **`flyer-board.png`**, `flyer-board-360.png`, ordered NO-SKILL A → Paso 10 winner A → Paso 11. First two image cells are intentionally identical.

### Carousel — recover B2's continuity; remove the two extra actions

Reuse `step8/B2/base-1.png`…`base-3.png` first. Retain B2's teal/cream material world, contrast approach and cohesive photographic space; develop from B2 rather than polishing B4's isolated photo windows. Form → wheel/process → material trace must remain legible. Compose cover and demanding close before extending the middle slide. These piece-specific image-area requirements do not become general Cropmark rules.

| Check | Required candidate result |
|---|---|
| Canvas/count/copy | Exactly **3 ×1080×1350** finals, all brand/descriptor/headline/support strings intact. No printed `/`. The two removed action strings have **0 occurrences**, including hidden rendered layers. |
| CTA semantics and styling | **CTA count across the entire set =1**, on slide 3 only, exactly `MIRA LAS PIEZAS`. No action line, arrow, underline, button or pill on slides 1–2. Brand/descriptor uppercase is identity, not an action. Final CTA uses a fine underline **1–2 px at 360** and/or one unboxed arrow; no filled container. Verifier counts apparent actions from the pixels, not just sidecar `role` values. |
| Continuous image space | On **every slide**, photographic image coverage **≥65% of frame area**; the main photograph reaches **at least 2 frame edges**. No isolated inset-photo card. Mark photo masks; extending the mask across flat fill does not count. |
| Closing image scale | Slide 3's principal material/ceramic subject tight bbox occupies **≥25% of frame area**, and the identifiable thumbprint/incised trace has maximum dimension **≥90 px at master** (30 px at 360). Preserve the actual trace detail, not a tiny pot alone. |
| Empty area | **Empty cells ≤35%** of the frame and largest 4-connected empty component **≤20%**, measured by the grid procedure below. No slide 3 dark void rescued by decorative filler or texture. |
| Hierarchy/readability | At 360, minimum headline cap **≥28 px** and **≥2×** the maximum cap of its support; every small-copy group, brand, descriptor and final CTA has cap **≥14 px**. Headline/support nearest ink gap **12 px to one headline cap height** at master. Every word is readable at 360 with **0 transcription errors**. |
| Safe placement | Required ink **≥64 px** from frame edges; **0** required-copy or key-detail occlusion. Keep at least **24 px** between copy ink and the tight bbox of a key hand/rim/trace; no accidental tangency. |
| Rhythm/coherence | **≥2 visibly different image–headline relationships** across the three slides, with named geometry and annotated evidence; changing the photo alone does not count. Preserve shared type roles and palette. Variation must not reintroduce B4's separate photo/text panels. |

Empty-area procedure: evaluate each 360×450 preview on a **20×25 grid of 18×18 px cells**. Record tight subject polygons and actual text ink expanded by **8 px** at this scale. A cell is empty when ≥90% of it is outside those occupied masks and its background has linear-luminance standard deviation **≤0.025**. Count empty cells /500 and the largest 4-connected empty component /500. Save the grid and masks. The verifier redraws subject annotations before comparing values. Do not label the entire photograph “subject” or add noise/ornament to bypass the test; an obvious dead field still fails the visual review even if texture escapes this proxy.

Outputs: `carousel/final-{1,2,3}.png`, matching `final-{1,2,3}-360.png`, editable source/sidecars/masks, `carousel/layout-evidence.json` and `carousel/empty-area.json`. Comparison: **`carousel-board.png`**, `carousel-board-360.png`: rows NO-SKILL revised brief → Paso 10 winner B2 (historical copy) → Paso 11; columns slides 1–3.

## Boards, provenance and value judgment

Boards derive from real finals without retouching. Use equal cell sizes and identical resampling. Put labels in external bands, never over artwork. Each condition label includes source paso/path, direct-raster vs editable treatment, and historical-copy caveats. Record source and output hashes, dimensions and cell coordinates in `comparison-manifest.json`.

- `thumb-board.png`: three **1280×720** artwork cells; previews three **168×95** / **360×203** cells.
- `flyer-board.png`: three **1080×1350** cells; preview three **360×450** cells.
- `carousel-board.png`: **3 rows ×3 columns**, each **1080×1350**; preview each **360×450**. Label bands are additional space with dimensions in the manifest.

Also export anonymous comparison copies under `qa/blind/`, with randomized condition labels and a sealed mapping in `qa/blind/key.json`. A fresh judge records first reads and preference before opening the mapping or producer rationale. Flyer baseline/winner duplication is disclosed after the first comparison; it is one unique comparator, not two independent wins.

Per piece, `qa/design-verdict.md` must record: technical PASS/FAIL; Paso 11 vs direct baseline **win/tie/loss**; Paso 11 vs owner winner **win/tie/loss**; absolute reference-level **yes/no/unverified**; at least **3 visible observations** and remaining defects. No forced positive conclusion. To claim this paso demonstrates useful value, require **3/3 pieces preferred over their direct baselines**, **0 regressions against the owner winners**, and all candidate technical checks passed. Otherwise report the actual fraction and the specific formats where value remains unproved.

That is evidence for these local executions only: historical controls, different generated imagery, repeated candidate iteration and changed carousel copy prevent a causal/general skill claim. A technical PASS or numerical score does not establish Behance-level work. Compare against **2 close finished references per format** at equal feed size, using available read-only local references, IDs and observations only. Record at least **3 concrete craft gaps or resolved relationships per format**. If suitable references are unavailable, absolute reference level stays unverified. Only a separate recorded owner decision can establish owner acceptance; do not invent it or modify historical feedback.

## Budget and correction limits

**Absolute global cap: 6 image_gen calls for Paso 11**, shared by every session, including failures, retries, edits, guides and discarded outputs. Log the ordinal before dispatch and reconcile status afterward in `imagegen-log.json`: purpose, condition, exact prompt, references (if any), session, status, output path/hash and remaining budget. No parallel requests. Baseline uses no reference images.

Planned allocation: **3 calls** for the new direct carousel, **0** for reused thumbnail/flyer baselines, **up to 3 reserved** for demonstrated candidate asset needs or a provenance-invalid baseline. Reuse B-R1/B2/clean sleeve first. Do not spend the reserve automatically. If a required replacement would exceed six, stop generation and report incomplete requirements; do not borrow budget from earlier pasos or switch providers. If the generation tool fails or is unavailable, record the blocker; no alternate generation route.

Candidates get R0 plus **at most 3 correction rounds for the whole set**, not three per slide/session. A concept replacement consumes a round. Record defect, affected region, principal change, expected effect, actual image and observed result in `rounds/Rn/correction-log.json`. Retain prior outputs. Baseline outputs are frozen after the first successful direct generation and normalization; no aesthetic selection loop. At a cap, report remaining failures instead of lowering thresholds.

## Sequential tasks — T1…T18

One named session owns each task. **Tn depends on completion of T(n−1)**; no overlap, parallel subagents or hidden worker sessions. Herdr sessions below are launched by the orchestrator/human, not spawned by this spec writer. Reusing a builder session for successive tasks is allowed. Baseline operator and final verifier must be distinct fresh sessions, with the information boundaries specified here.

| Task | Single owner / work | Inputs | Outputs | Evidence file under S11 |
|---|---|---|---|---|
| T1 | Builder: snapshot guardrails and audit baseline provenance. | This spec; supplied AGENTS instructions; historical prompts/logs/sources/renderers; current Git state. | Source/hash inventory, initial protected-file hash/status, reused-control decision for each piece; initialize shared budget at 0/6. | `provenance-audit.md`, `input-manifest.json`, `imagegen-log.json` |
| T2 | Baseline operator, fresh session: freeze neutral carousel generation input without reading Cropmark/design evidence. | Only frozen carousel content, fictional subject, count/size, one closing CTA and tool instructions, passed by orchestrator as a minimal brief. | Three exact direct-final prompts; no thresholds, winner images or skill-derived layout prescriptions. | `baseline/brief.md`, `baseline/prompts.md`, `baseline/session-scope.md` |
| T3 | Same baseline operator: generate direct slide 1. | T2 slide-1 prompt; shared call ledger. | Untouched source, normalized `baseline/carousel-1.png`; retain defects. | `baseline/slide-1-provenance.json` and ledger entry |
| T4 | Same baseline operator: generate direct slide 2. | T2 slide-2 prompt; remaining ledger. | Source and `baseline/carousel-2.png`. | `baseline/slide-2-provenance.json` and ledger entry |
| T5 | Same baseline operator: generate direct slide 3 and freeze baseline set. | T2 slide-3 prompt; preceding baseline outputs/normalization records. | Source and `baseline/carousel-3.png`; immutable baseline hashes. | `baseline/slide-3-provenance.json`, `baseline/frozen-manifest.json` |
| T6 | Builder: fix thumbnail and measure subject clearance. | C renderer/final, clean B-R1 source, historical A, thumbnail checks. | Editable thumbnail, masks, final/previews, measured gaps and cap/fill values. | `thumbnail/measurements.json`, `thumbnail/clearance-overlay.png` |
| T7 | Builder: resolve flyer source plane before adding type. | Clean sleeve base; A benchmark; angle/keystone requirements; ledger. | Approved clean photographic source/crop, independent-of-type edge annotations and transform plan; use reserve only if reuse fails visibly. | `flyer/plane-plan.json`, `flyer/clean-source-review.md` |
| T8 | Builder: compose physical flyer type and verify content/hierarchy. | T7 source/plane, frozen copy, flyer checks. | Final/previews, editable text/integration layers, safe insets and projected measurements. | `flyer/surface-evidence.json`, `flyer/copy-check.json` |
| T9 | Builder: develop carousel cover from B2 continuity. | B2 clean bases; revised copy; carousel requirements. | Representative slide 1 at master/feed, relation/mask annotations and reference comparison. | `carousel/cover-review.md` |
| T10 | Builder: resolve demanding carousel close. | Approved cover/system, clean trace base, final-only CTA. | Representative slide 3 with adequate material scale/occupied area; review beside cover before extending. | `carousel/close-review.md`, preliminary `carousel/empty-area.json` |
| T11 | Builder: compose middle slide and inspect the complete sequence. | T9/T10 system, process base and slide-2 copy. | All three editable finals/previews; coherent roles, two relationships, one CTA. | `carousel/layout-evidence.json`, final `carousel/empty-area.json` |
| T12 | Builder: run mechanical QA and bounded corrections. | All five candidate images, masks/contracts, frozen criteria, shared rounds/call budget. | Per-piece strict QA and pixel measurements; correct observed defects sequentially within R1–R3, then rerun only affected checks. Baselines remain frozen. | `qa/producer-checks.md`, `qa/{thumbnail,flyer,carousel}/`, `rounds/Rn/correction-log.json` |
| T13 | Builder: assemble the three comparison boards and anonymous copies. | Frozen baseline/winner/candidate finals; board contract. | Required named master/feed boards, anonymous comparisons, cell/source hashes. | `comparison-manifest.json`, `qa/blind/key.json` |
| T14 | Builder: freeze reproducible handoff. | Finals, composition sources, actual fonts/licences, baseline sources, manifests. | S11-only portable package; render outside original folder; compare decoded pixels; local text-edit proof; final hash inventory. No commit. | `package/`, `qa/reproduction.md`, `handoff-manifest.json` |
| T15 | Verifier, separate fresh session: independently remeasure thumbnail and flyer. | Frozen handoff, raw clean sources/fonts, this spec; no producer conclusions. | New annotations/calculations, full/preview inspection, own raw values and PASS/FAIL per criterion. | `qa/independent/thumbnail.json`, `qa/independent/flyer.json`, annotated images |
| T16 | Same verifier: independently remeasure carousel and controls/boards. | Three finals, raw bases, baseline provenance, board manifest/spec. | Own CTA count, empty grid/masks, photo/subject areas, caps/gaps, board cell checks and baseline audit. | `qa/independent/carousel.json`, `qa/independent/boards.json` |
| T17 | Same fresh verifier acting as design judge: judge anonymously, then reveal. | Anonymous comparisons first; afterward source mapping, owner winners and close read-only reference IDs. | Pairwise and absolute verdicts with visible evidence; unresolved craft gaps; session independence attestation. | `qa/design-verdict.md`, `qa/independent-verification.md` |
| T18 | Orchestrator/coordinator: close evidence without altering judgments. | Independent reports, ledger, handoff and starting Git/hash snapshot. | Requirements matrix, honest value result and unresolved list; confirm exclusions/protected hash. No commit/merge/publish/push. | `qa/closure.md` |

If verification fails, preserve the fresh verdict. Any remaining-budget repair returns sequentially to the relevant builder task, consumes its applicable round/call, freezes new hashes, and requires the verifier to remeasure changed artifacts. The builder must never author or overwrite the independent reports. No endless verification/correction loop after caps.

## Commands and evidence discipline

Future sessions run from the repository root. These are checks to execute later, not claims that they passed:

```sh
sha256sum docs/recalibration-v3-human-feedback.json
git status --short
git diff --name-only
python3 skills/cropmark/qa/qa.py thumb --strict --expected-count 1 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/thumbnail evals/art-direction/diagnostic-2026-10-22/renders/step11/thumbnail/final.png
python3 skills/cropmark/qa/qa.py post --strict --expected-count 1 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/flyer evals/art-direction/diagnostic-2026-10-22/renders/step11/flyer/final.png
python3 skills/cropmark/qa/qa.py carousel --strict --expected-count 3 --out evals/art-direction/diagnostic-2026-10-22/renders/step11/qa/carousel evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-1.png evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-2.png evals/art-direction/diagnostic-2026-10-22/renders/step11/carousel/final-3.png
```

Declare fitted panels/shared axes/gaps in composition contracts and run `python3 skills/cropmark/qa/design_check.py <contract.json> --out <report.json>` where applicable; log exact resolved paths and stdout/stderr. Candidate strict QA must exit **0**, expected counts **1/1/3**. Add the new geometric/content checks separately; do not change QA code to obtain a PASS. Baseline raster font identity remains unknown unless actually established; do not fabricate font metadata to make strict QA pass. Record baseline failures/limitations alongside direct visual measurements.

## Non-negotiable safeguards

- Never edit `docs/recalibration-v3-human-feedback.json`; expected SHA-256 **`31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`**, checked before/after every handoff. Historical 0/17 reference-level record is unchanged by this local exercise.
- Never commit Behance images, `refs-cache`, CDN URLs, `__pycache__`, or **`renders/step3/qa-report.json/`** (including its full R-prefixed path). That Step 3 directory was already untracked at spec start; leave it untouched. No blanket staging. This paso authorizes **no commits or staging** at all.
- Only this specification is written by the spec session. Future implementation/evidence stays under S11; no other branches, merge, publication or changes to historical winners/controls. Keep private recalled context out of TypeSafe/JEV. Never invent baseline provenance, human approval, independent review or a positive result.

## Separate verifier checklist

The verifier session must have performed **no baseline prompting, generation, composition, correction, producer QA or board assembly** for this paso. Record session identifier, start time, role declaration, frozen input hashes and exact commands. Read this spec and source artifacts; calculate independently before consulting producer measurement values. Opening their JSON and agreeing with it is not remeasurement.

- [ ] Verify the protected feedback hash, unchanged historical inputs, Git scope and excluded-path status; reconcile **all sessions' generation calls ≤6** and corrections ≤3 set rounds.
- [ ] Audit direct baselines from exact prompts through raw images and normalization to board cells. Confirm historical A reuse, new carousel's matching revised copy, fresh baseline session scope and no retouch/selection loop. Flag unknown context provenance explicitly.
- [ ] Open all **5 candidate finals**, all comparator images, every master board and every required feed preview. Independently check dimensions, counts, source hashes, external labels, cell equality/resampling, flyer duplicate cells and historical B2 copy disclosure.
- [ ] Before rationale, transcribe thumbnail at **168/320/360**, flyer at **360**, all three carousel slides at **360**. Record actual readings/errors and the identified story/subjects; a supplied source string is not a legibility test.
- [ ] Redraw thumbnail subject boxes from the clean source/final transform; regenerate ink masks; report every gap, closest pair, minimum **≥32 px**, overlap **0**, edge **≥40 px**, duration-zone intersections **0**, common P cap **≥126**, P fill **≥0.6613** and `3 AIs.` cap **≥10 px at 168**.
- [ ] Fit flyer sleeve edges afresh, without seeding producer corners. Measure four corner residuals, **≥5°** edge/baseline tilt, **≥4%** keystone, **≤1°** rectified baseline error and **≤3 px** projected baseline residual; test **5%** insets. Reject self-round-trip evidence and unsupported hidden-corner estimates.
- [ ] Measure final projected flyer caps across the plane: title **≥32 px**, metadata **≥14 px** at 360, conservative ratio **≥2.25**. Count separators **2**, leading/trailing separator lines **0**; inspect paired light/mid/dark print crops and printed-on-sleeve appearance.
- [ ] Independently count carousel apparent CTAs **0/0/1** and confirm the removed phrases occur **0** times. Verify final thin underline/arrow and absence of boxes/pills. Do not accept a “plain text” role declaration for an apparent action.
- [ ] Independently redraw carousel occupancy masks and calculate empty-grid totals **≤35%**, largest component **≤20%**, photo coverage **≥65%**/two edges on every slide, closing subject bbox **≥25%** and trace dimension **≥90 px**. Save raw grid counts and annotated overlays.
- [ ] Remeasure carousel cap hierarchy/small-copy minima, headline/support gaps, **64 px** margins, **24 px** key-detail clearance and **0** clipping/occlusion. Identify at least **2** actual image–headline relationships and assess B2-style continuity from the images.
- [ ] Recompute glyph-core contrast for every candidate text group from clean backgrounds and integrated ink, reporting P05/median/share below target; verify the **3:1 /4.5:1** limits and actual word readability. Inspect absence of default shadows, dark-on-dark text, cutoff and forced-justified short lines.
- [ ] Re-run strict QA with counts **1/1/3** and applicable design contracts using verifier-owned output paths. Reproduce the portable package outside its original folder; check pixel equality and editable-copy proof without overwriting frozen finals.
- [ ] Judge anonymous comparisons before key/rationale; record pairwise win/tie/loss and absolute yes/no/unverified separately, **3 observations per piece**, reference IDs and remaining gaps. Report achieved value fraction; no technical-to-aesthetic shortcut or automatic Behance claim.

## Done-when

**Evidence complete** only when all five candidate finals, required sources/sidecars, three named boards and feed variants, verified controls, budgets/manifests, reproducible package and independently authored reports exist with no missing requirement. Failed criteria remain FAIL, not N/A. Every checklist item has measurements/evidence or a specific unresolved failure.

**Accepted Paso 11 result** additionally requires all candidate numeric/content/visual checks passed, independent verification of that pass, **3/3 wins over direct baselines** and **no losses to the owner winners**. Technical completion, local comparative value and absolute craft level must be reported separately. An incomplete or losing result can be handed back honestly but must not be called accepted or reference-level. Owner approval and any future release action remain separate from this spec.

Spec-writing completion: save this document, check only it was added by this session and the protected SHA-256 is unchanged, save a short AgentMemory note with its path/key thresholds, print a ten-line summary, and stop. Implementation and verification are future sessions' work.
