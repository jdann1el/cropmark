# Style: text-in-scene
Formats: thumbnail
Best for: Tech, tutorials, DIY, reviews, lifestyle

## Signature
The only words live inside the scene: phone notification, review card with stars, sticky note, tape label, chat bubble, price tag. Lowercase, 2-5 words.

## Recipe
Card: white rounded 24-32 px, shadow 0 12 30 rgba(0,0,0,.35), InstrumentSans Bold 44-64 px at 1280 wide; sticky note: NothingYouCouldDo/Caveat on yellow, rotated 4-8°.

Variants: phone notification (cm.card + icon), review card, sticky note (cm.sticky), kraft hang tag (cm.tag) — a blank tag with a question is fine when there is no price; museum placard, receipt, label tape.

## Avoid
Cards covering the face or main object; more than one card.

## Physical plane or HUD
Choose explicitly. A physical panel/sign is a surface: identify its four corners, typeset editable text on a separate flat layer, map the whole layer to that quadrilateral with a projective transform (a rotation alone is insufficient), then apply matching light and foreground occlusion. Keep letters inside the panel and record transformed corner/ink bounds. Review at full size and feed.

A deliberate screen overlay/HUD stays in canvas coordinates; it need not inherit a photographic panel's perspective. A review rating, notification time, price or chart requires supplied evidence. Use a conceptual label without a fabricated result when evidence is absent. The style's example card is an option, not a requirement to add a floating rectangle.
