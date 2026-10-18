# Format: YouTube thumbnail (1280x720, 16:9)

Technical dimensions/safe zones apply; layout, word-count and style patterns below are suggestions. The content contract and faithful reference take precedence over aesthetic prescriptions. Typography-only work is valid when it serves the brief.

Spec: 1280x720 master (YouTube accepts up to 3840x2160, ≤2 MB on phone upload). Bottom-right ~18%x15% clear (duration badge). ≥40 px from edges. Feed test at 320 px wide (and 168 px for silhouette).

Sources: own practice (2 training rounds, 17 niches), studied portfolios, and community thumbnail rules; own wording.

## Goal and honesty
- One job: make the right viewer click in under a second at 320 px wide. Test: **can you tell what the video is about without reading?**
- Never promise what the video doesn't contain: no invented numbers, results, props or demonstrations. Text hooks come from the video/title.
- Don't claim CTR gains; treat a redesign as an A/B hypothesis (YouTube Studio has native title/thumbnail testing). If the original is already strong, present the new one as a variant, not a fix.
- AI-recreated faces are mock-ups only; for a real client use their photo/cutout and keep AI to background/props.

## Diagnose first (one line)
Too much text · subject too small · no single focus · low contrast · typos · collage clutter · text repeats title.

## Composition
- One subject, big: face or main object fills **30-50%** of the frame, placed left or right third; text/prop in the other side.
- **One** extra focal element only: number, prop, arrow, logo, or in-scene card.
- Gaze leads: eyes to camera (connection) or toward the object/text (direction).
- Keep ~40% of the frame calm for text or breathing; map the subject before placing text (face position, silhouette edge, largest quiet zone) and never put text across a face or the key object.
- Bottom-right corner empty (duration badge).
- Consistent series mark (small channel logo/colour bar) in the same corner every time, if the channel wants recognition.

## Text
- 2-4 words (5 max). A hook phrase, never a sentence, never the whole title. A title *fragment* is fine when it names the stake (a year, a person, a price given in the brief). Words inside in-scene cards/UI count separately (≤5 per card, one card).
- Heavy condensed display (Anton-like) for V1; clean sans in lowercase for in-scene cards (V2). Stroke/shadow for separation, not glow soup.
- Hook types: stakes ("$1 vs $1000"), outcome ("so easy"), confession ("I quit"), warning ("don't do this"), question mark word ("winner?"), timer ("15 min"). Prefer words already in the video.

## Colour & contrast
- Two dominant colours + one accent (yellow, red, cyan work in most feeds). Pick brand colours if they exist.
- Squint test: subject, text and background must separate as three value levels.
- V2 grading: high saturation, deep blacks, complementary or teal/orange split, extreme sharpness, rim light on faces.

## Faces
- Expression is the message: shock (wide eyes, open mouth), curiosity (raised brow, smirk, look off-frame), confidence (direct eye contact), frustration (tension, gesture). Exaggerate one notch beyond natural.
- Large, crisp, well lit; crop tight (forehead may be cut, never the eyes/mouth).
- Faces aren't mandatory: hands-on-instrument, product duel or scene-only can beat a face for tutorials, ambience and product niches. (charlie insists on a face; see conflicts.md.)

## Two tiers
- **V1 (mid-tier, fast)**: cutout subject + 2-4 giant words + one badge/number on a clean graded background. Good for small channels and SMBs; quick to produce.
- **V2 (premium, default for proposals)**: the image tells the story; text shrinks or lives inside the scene.
  1. *Story in one frame*: conflict, contrast or stakes visible (half-dirty/half-clean car, wreck behind the subject, person in an absurd setting).
  2. *Text inside the scene*: review card with stars, phone notification, chat bubble, sticky note, masking-tape label, sign; lowercase, 2-5 words, white rounded card with soft shadow.
  3. *Text as object*: a prop or person replaces a letter in the word.
  4. *Faces at the limit* (see above).
  5. *Split before/after* (vertical split) for transformations: restoration, detailing, fitness, renovation, makeup.
  6. *Character frame*: several reacting characters framing the hero (gaming, reactions, animation).
- Offer V1 and V2 as an A/B pair when the channel's style is unclear.

## Story techniques by niche (proven patterns)
- Makeup: half face bare / half done, contrast exaggerated so it reads at 320 px + timer card ("15 min").
- DIY/woodwork: raw scraps and finished piece on the same bench + tilted handwritten sticky note.
- Product reviews/duels: two products face to face, equal hero light or the underdog lit warmer, one "winner?"/"worth it?" card. Price tags only with prices from the brief. Real product identity needs real product photos (generators can't draw logos): with none, use generic look-alikes and let the card/title name them.
- Tech/app: face lit by phone + iOS-style notification card; never cover face or phone.
- Lessons/tutorials: close-up hands on the tool + tape strip "start here". No face needed.
- Ambience/study-with-me: the scene is the hook; just a LIVE chip + mono timer. V2 adds least here.
- Fitness: dark workout-app card with progress ring + duration; stronger with sweat, a real clock or a before/after.

## Image generation hygiene
- Generate the base image with **no text, letters, logos, signs or banners**; models leave blank signs or garble words. Add all text programmatically (HTML/CSS or Pillow) afterwards.
- Prompt skeleton: "hyperreal 16:9 thumbnail photo, high saturation, crisp detail" + the concrete story + "no text".
- If a reference image drags the composition back to the old layout, regenerate without the reference.
- Known model failures: before/after difference too subtle (ask for exaggeration), ignores layout words like "zig-zag", stray UI on screens.

## Brief format (internal or client)
Composition (subject side, % of frame, gaze) · Text (hook, placement) · Palette (2 + accent, hex) · Focal element · Tone · Tier (V1/V2).

## QA (always, by looking at the render)
At 1280 full size and at 320 px: hook readable, subject clear, one focus, no clipped text, bottom-right clear, no typos, nothing the video doesn't contain. Deliver as a before/after sheet when redesigning.

## Portfolio-level additions (from studied 2025-26 Behance work)
- **Stakes stack (zero-text allowed)**: huge subject in the foreground cut by the frame edge, hero object mid-ground, threat/context in the background (police lights, helicopters, smoke). 3 depth layers, cinematic night/storm grade, one colour accent. A recurring character look (mask, chain, jacket) becomes the channel brand.
- **UI as hero**: an app card (balance, chart, notification, scoreboard) at 40-50% of the frame, big number *inside* the UI, face + gesture on the other side, background coloured by the emotion (green gain, red loss, orange hype). A blurred figure teases without lying.
- **Two-line header pattern**: line 1 small coloured caps, line 2 bigger in a white or accent box with outline. Use only for V1/education niches.
- Thumbnails at portfolio level almost never use more than 4 words. Zero text works only when the image alone states the stake (a chase, a wreck, a face mid-reaction); human blind vote (2026-10) preferred 2-4 word hooks over zero-text for horror and for comparisons.
- **Keep the hook words when** the stake lives in a sentence ("the lights never went out") or the video compares named things: a VS/comparison needs a label on each side ("CHEAPEST" / "MACBOOK AIR"); a lone "winner?" bubble does not identify the contenders.
