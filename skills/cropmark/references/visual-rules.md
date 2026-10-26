# Visual rules — evidence before polish

Apply these to actual renders. See `rulebook.html` for deliberately constructed teaching examples and `casebook.md` for provenance-backed observations. Teaching fixtures show a defect; they are not measured evidence that the skill improves an autonomous result.

| ID | Look for | Required action and verification | Legitimate exception |
| --- | --- | --- | --- |
| R01 Purpose | Short rules, crosses, dots and crop marks with no job | Remove the mark and compare at feed size. Keep only information, structure, identity or a visible compositional purpose. | A brand mark, measurement, grouping line or faithful reference that needs it. |
| R02 Copy | Invented micro-labels, coordinates, dates, mood words | Retain the brief's content; replace filler with meaningful subject matter or redistribute scale/space. | Necessary attribution, real specifications, sequence or navigation. |
| R03 Type roles | Arbitrary family/weight/style changes | Set display, support and metadata roles. Use actual font files; compare width, weight and voice with imagery. Keep equivalent roles consistent. | Deliberate expressive lettering or a faithful reconstruction. |
| R04 Hierarchy | Many similar sizes; every element shouts | Choose the first read and subordinate support. Squint: distinct masses should establish order. | An intentionally even list or grid whose reading order is still clear. |
| R05 Alignment | Near-shared edges and unrelated centres | Choose each group’s left/right/centre anchor and containing region; compare actual ink edges, not just nominal text boxes. Keep a semantic phrase visibly grouped. | Deliberate stagger or asymmetry supporting the idea. |
| R06 Padding | Equivalent containers use different insets | Declare a short spacing scale. For centred groups compare left/right and top/bottom visible gaps around the whole group; for equivalent panels reuse inset pairs. Distinguish fitted panels from large colour fields. | Optical allowance for a curve, icon or descender, checked in the render. |
| R07 Separation | Independent blocks touch or crowd | Group related words before separating independent blocks. Both crowding and an unmotivated gulf between a premise and its answer break the relationship. Measure the actual clear space at feed size. | Intentional overlap with a clear foreground and legible message. |
| R08 Tangency | Letter/object edges almost touch; ambiguous cuts | Either separate clearly or overlap decisively. Inspect masks and edges at 100%. | A deliberately constructed lockup with visible control of the joint. |
| R09 Typesetting | Widows, weak breaks, clipped descenders | Break at meaning units; adjust measure, composition and spacing before shrinking the type. Check accents and loaded glyphs. | A faithful line break, expressive fracture or required legal copy. |
| R10 Effects | Shadows, strokes and texture applied by habit | Identify what depth, contrast, material or identity each effect supplies. Compare removal. | Effects that demonstrably supply those functions. |
| R11 Image/type | Photo and heading behave as unrelated blocks | Compose crop, gaze, scale and available quiet space with the actual words. | A deliberately separate information panel with a clear relation to the image. |
| R12 Sequence | Repeated layouts without narrative; arbitrary variety | Map slide/post roles; maintain type, palette roles and brand while varying what the argument needs. Integrate the wordmark into the composition; do not default every post to a footer bar. | Repetition is the concept or a comparison requires matched geometry. |
| R13 Photo craft | Halos, implausible light, wrong perspective/material | Compare source identity and mask on light/dark; match scene light, scale, contact and reflections. | Declared surrealism may bend physics, while identity and edges still need control. |
| R14 Substance | Clean frame with no specific idea or useful content | Restate the message and the visible device. Recompose or change concept when they do not connect. | Deliberate restraint with a strong typographic or photographic statement. |

## Exceptions are evidence, not permission slips
Record the relevant brief/reference and the visible purpose. A written explanation cannot rescue a collision or unreadable required content. Distinguish a technical failure from a house preference; no font, colour, serif, gradient, line or palette is inherently an AI detector. Avoid replacing one universal fashion with another.

## What can be checked
`../qa/design_check.py` checks a declared layout contract: safe margins, finite boxes, actual supplied font paths, common axes, declared/balanced padding, bounded gaps and set tokens. Use it for fitted text panels and promised axes/gaps, rather than omitting a failed relationship. It does not infer these from pixels and does not judge whether an overlap or font is tasteful. Declare only relationships the composition actually promises, and inspect the raster independently. Record intentional bleeds/overlaps/optical offsets explicitly; metadata can be inaccurate.

For detailed grouping, centred padding and expressive alternatives to repeated ornaments, read `../techniques/typography.md`.

For a fitted panel, declare the union of its actual text ink as children and compare vertical gaps with balanced_axes y by default; add x when centring is promised. A deliberately asymmetric large field can use explicit insets instead. Give optical offsets a visible reason and check the raster; do not change the declaration to excuse an accidental mismatch.

## Review order
Message and concept → focus and composition → type and image integration → colour and spacing → effects and small detail. Name up to three observed problems per round with image/region, rule ID, correction and observed outcome. Three correction rounds maximum; changing concept uses a round. Do not invent a problem just to use the allowance.
