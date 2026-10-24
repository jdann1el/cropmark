# Review the actual final PNGs

Run strict `qa.py` for the format and expected count. Inspect every full render, every feed preview (320 px thumbnail / 360 px post) and a contact sheet of the full set. Passing a command is technical evidence only.

1. Content: all required words, facts, identities and outputs survive; charts, gestures and before/after do not imply invented proof.
2. First read: what is understood immediately, and which element leads? For typographic work, the words and their composition can carry the idea.
3. Specificity: name the subject detail and visual device. A self-score is not evidence of a strong concept.
4. Composition: crop, gaze, axes, safe zones, spacing, tangencies and intentional bleed/overlap. Apply `../references/visual-rules.md` R01–R15 to observed defects.
5. Type: actual fonts and glyphs, meaningful breaks, clear roles, ink bounds and no clipped descenders; required copy remains readable at feed size.
   - For a headline–object relation, record the words, surface/gesture, layer order and covered-ink fraction; at 360 px check that the object and complete phrase remain clear.
   - On photographic backgrounds, record local contrast beneath each actual text group using linearized sRGB luminance, P05, median and share below target under glyph cores. Treat about 4.5:1 for small copy and 3:1 for a large headline as provisional design targets, not changes to the existing QA gate. Verify brand, descriptor, headline, support and CTA, including every word, at 360 px.
6. Image: identity preserved where required; masks, materials, light, scale, perspective and shadows coherent. Inspect critical edges on light/dark.
7. Sequence: all slides work alone and as a family; variation and repetition serve their roles. Confirm brand, type and palette continuity.
8. Correction: record image/region, defect, proposed action and observed effect. Re-inspect the whole set after a global change. Use at most three correction rounds after the initial developed set.
9. Package: copy sources/assets/fonts into a new directory, rerender, compare pixels, then make one localised text change to prove editability. Declare external runtime dependencies and any rasterised parts.
10. Report checks actually performed, the design rationale and remaining limitations. An unresolved visual gate remains unresolved at the iteration limit.

For each main group, identify its containing region and promised anchor. Compare actual ink gaps: paired padding for centred lockups, shared edges for editorial blocks, proximity between linked phrases and separation between unrelated groups. Inspect brand scale and the reason for any strip/frame. Declare these relationships in design_check only where the composition actually promises them; an intentional asymmetry must remain visibly controlled.

Fitted text panels and promised axes/gaps require a declared layout check. For a note/panel, register the outer box and all actual text-ink children, then check balanced top/bottom padding (and left/right when centred). Declare a maximum gap for linked copy where relevant. A failed check is corrected or disclosed; do not skip the contract or redefine its targets to make accidental geometry pass. Large asymmetric fields and intended overlaps keep their explicit, visually verified exception.

Before declaring the visual pass, use `../references/composition-study.md`: inspect the representative beside a close finished reference at the same feed size, without its rationale. Record what the viewer understands/wants and where ours is weaker. Check actual crop survival, not just type safe zones; visible logo ink, not transparent raster bounds; linked phrase gaps, not only permissive maxima. A metadata PASS cannot override an unattractive subject presentation or unexplained graphic device.
