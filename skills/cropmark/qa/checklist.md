# Delivery QA — inspect the actual final files

Run `python qa/qa.py <thumb|post|carousel|story|reel> --strict --expected-count N <final files>` on outputs only. Keep poor references separate; filenames do not waive validation. Fix every FAIL/ERROR. A zero exit code covers only the reported technical checks.

1. Complete requested set, exact dimensions, correct order and copy/data from the content contract. Every required item is present; input references are not counted as new output.
2. Open every PNG at full resolution and at feed (320 px thumbnail / 360 px post). Check legibility, focus, contrast on the real background, stroke, descenders, accents and line breaks. Background-ring contrast estimates do not certify a photograph or gradient.
3. Check safe zones and timestamp corner. Intentional decorative bleed is separate from required text/identity. Inspect readable stroke as well as fill; metadata is not proof that every visible pixel is contained.
4. Compare supplied subjects to their sources. Check mask edges on light/dark, interior holes, printed logos, colour, hair, transparency and reflections. No unexplained substitutions of real subjects.
5. Physical scene text follows its surface, light and occlusion. Keep it inside the intended panel; distinguish deliberately flat HUD. Rounded cards and tilted text alone do not establish perspective.
6. Verify effective fonts and required glyphs. Empty text metadata requires explicit `text_free: true`; shapes-only metadata cannot account for visible text. Manually drawn text needs equally complete metadata.
7. Truth: all claims and numbers are supplied; visual results, charts, UI confirmations, price cues and before/after do not imply evidence absent from the brief. Fictional interface examples must remain clearly conceptual.
8. Set coherence and completeness: content, numbering and CTA survive across all slides. Variation is optional when a repeated grid serves the brief or fidelity target.
9. Specificity: remove filler labels, interchangeable motifs and unreadable decorative microcopy. Check whether each device communicates something useful for this brief. No automatic bans on colours, fonts, pills or gradients.
10. Score using `rubric.md`. Inspect faithful copies against their reference and verify a rerender plus an actual text edit from packaged sources. Initial result plus at most two refinements; disclose anything unresolved.
