# QA checklist (open the real PNGs — never sign off unseen)
Run `python qa/qa.py <thumb|post|carousel> out/*.png`, fix every FAIL, then look at `qa_out/contact_sheet.png`.
1. Exact size; files named in order.
2. Feed size (320 px thumb / 360 px post): hook readable, focal point obvious in 1 second.
3. Cover the text: is the idea still understood? (thumbnails and posts)
4. One focal point; quiet zone under text; no text over faces/key objects.
5. Safe zones: thumbnail bottom-right empty; post content inside central 1012 px; story top/bottom bands.
6. Type: chosen pairing, no system defaults, accents render (á ñ ç à), no widows, no clipped descenders.
7. Set coherence (carousel): same system, varied layouts, interior slides have a visual anchor, swipe cue + CTA.
8. AI artefacts: hands, fake text, warped logos, duplicated objects. Regenerate or crop.
9. Truth: every number/claim from the brief; no invented testimonials, ratings, prices, "proven".
10. Score with rubric.md; any criterion < 4 → one more pass (refine, don't add).
