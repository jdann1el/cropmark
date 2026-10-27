# Paso 10 independent verification

**Run:** 2026-10-26, in the main session after stopping the stalled reviewers. This review re-opened the final boards, final PNGs, sidecars, QA reports and protected feedback hash; it did not rely on agent reports.

## Technical checks

- Strict QA exit 0 for thumbnail C, flyer C and carousel B4 (3/3). The three board files and reduced previews are readable at the dimensions recorded in `comparison-manifest.json`.
- Thumbnail common P glyph, remeasured from final pixels: cap A 126 px / 17.500% of frame, B-R1 66 px / 9.167%, C 143 px / 19.861%. At 168 px, C's cap is 18.77 px. P fill ratio is A 0.6613, B-R1 0.5794, C 0.6721. Cream headline on the dark band; no clipping or duration-zone collision.
- Flyer C uses a four-corner homography on the sleeve. Independent Canny/Hough line intersections from the clean source differ from the declared final corners by 0.59, 2.20, 1.16 and 0.20 px (maximum 2.20 px; limit 3.40 px). The minimum inverse-projected text inset is 38.83 px on a 720×680 plane (minimum required 34 px). Visible caps at 360 are 27.33 px title / 15.33 px metadata; ratio 1.783. Metadata is one group and no line ends in `·`. It follows the sleeve plane and its luminance/grain; dark brown on cream, no shadow.
- Carousel B4 final sidecars and font files give headline/support gaps 53/58/35 px against headline caps 59/70/73 px. Small-copy cap minimum is 14 px at 360. Layouts differ per slide; only slide 3 has underline/arrow CTA treatment; no shadows or dark-on-dark type.
- The full supplied flyer copy is present. All image and text boxes remain in frame; preview inspection found no accidental cut-off. Thumbnail/carousel type occupies flat clean copy zones, not invented physical surfaces.
- `imagegen-log.json` has 0 calls (0/8). Added surface-bound guidance in typography, imagery and QA checklist is marked **CANDIDATE / unvalidated**. `docs/human-feedback-paso9.md` is dated 2026-10-25 and attributes the preferences to John.
- `docs/recalibration-v3-human-feedback.json` SHA-256 is `31a2b18ad793fe67de21dd4605c8bd801c19a1cba3c229de9286e4ecbd32fb38`.

## Visual verdicts

- **Thumbnail:** C beats B-R1 for feed impact and A-level type mass; its physical-board scene still takes attention away from the digital portfolio premise.
- **Flyer:** C fixes perspective and hierarchy, but A remains more resolved overall. C's leading separator reads as a bullet, and the bold face is less naturally fitted to the sleeve.
- **Carousel:** B2 remains stronger overall. B4 meets its layout/readability checks but its separate photo windows and flat copy fields feel more segmented than B2.

Technical QA passing is not evidence that the candidate rules are validated or that any piece reaches Behance-level craft.
