# Paso 11 design verdict

Session `p11-verify-20261026-155908Z`. The blind files were inspected before `qa/blind/key.json` or producer rationale was opened. Preference is a qualitative judgment, separate from technical checks.

## Thumbnail

- Technical: **FAIL**. The portfolio board begins 29 px from the top edge, below the 40 px safe-zone requirement. Pixel-based headline separation and ink fill look good, but glyph-core contrast and all edge measurements were not fully independently certified.
- Vs NO-SKILL direct baseline: **win**. The candidate shows three agents working on one shared portfolio; the direct image uses three unrelated agent symbols and a separate blank sleeve.
- Vs Paso 10 winner C: **win**. The new copy zone separates both headline lines from the portfolio and lower-right robot; the owner winner crowds the lower-right robot with its headline.
- Absolute reference-level: **unverified**. No two identified close thumbnail references were available in the local reference set.
- Visible observations: (1) all three robot figures remain present and the board reads as their shared work surface; (2) the two-line cream headline has strong mass against the navy field; (3) at 168 px, the message and three-agent/shared-board story remain recognizable; (4) the board's top edge sits only 29 px from the canvas edge.
- Remaining defects: top safe-zone failure; own glyph-core contrast summary and exact subject-to-ink gap map are incomplete; T14 handoff package is absent.

## Flyer

- Technical: **FAIL / not fully verified**. Title first-line visible baseline estimate is about 3.8° while the requirement is at least 5°; independent corner residual, full baseline projection residuals and projected cap ratio are not established. Approximate metadata cap at 360 is 13 px against 14 px required.
- Vs NO-SKILL direct baseline: **loss**. The direct image presents the event title on one line with larger, clearer metadata. Candidate perspective is stronger but its title breaks across two lines and supporting line reads smaller.
- Vs Paso 10 winner A: **loss**. Paso 10 A is the identical direct cell. Candidate does not improve the title's first read or metadata scale enough to offset the more angled treatment.
- Absolute reference-level: **unverified**. No two identified close flyer references were available locally.
- Visible observations: (1) the sleeve edges slope down-right at about 7.16° top and 5.41° bottom; (2) the wordmark is visibly placed on the paper plane and paper grain remains visible through the ink crops; (3) the title wraps into “Noche de / Vinilos,” weakening the first read relative to the direct cell; (4) the venue/date/time are present in the requested order with two separators.
- Remaining defects: projected title/metadata baselines and insets lack a verifier-owned full fit; metadata cap is borderline below threshold; corner-fit uncertainty reaches the acceptance tolerance; no portable handoff package.

## Carousel

- Technical: **FAIL**. Slide 2 headline glyph-core P05 is 1.05:1 (required 3:1); slide 1 descriptor P05 is 4.16:1 (required 4.5:1); slide 2 largest empty component estimate is 24.8% (limit 20%); slide 3 trace estimate is 75 px at master (limit 90 px); descriptor cap is 13.33 px at 360 (limit 14 px); slide 3 headline/support cap ratio is about 1.87 (limit 2.0); top brand ink starts at about 60 px (edge inset minimum 64 px).
- Vs NO-SKILL direct baseline: **win**. The candidate has stronger shared teal/cream system and a much larger closing trace, while the direct row uses three unrelated sepia treatments. This is a local visual preference, not a causal Cropmark claim.
- Vs Paso 10 winner B2: **tie**. Candidate removes the two extra action lines and increases the closing trace, while B2 keeps the second-slide headline on a clearer background and has steadier feed-size hierarchy.
- Absolute reference-level: **unverified**. No two identified close carousel references were available locally.
- Visible observations: (1) the teal wall/table world links the three slides and photographs reach all frame edges; (2) slides 1 and 2 have no apparent action; slide 3 carries the only underlined CTA; (3) slide 3 shows a large ceramic vessel and incised thumbprint trace; (4) slide 2's dark first headline line nearly disappears into the teal wall and its empty grid component is oversized.
- Remaining defects: slide 2 contrast and empty-area failures; slide 1 descriptor contrast failure; small descriptor cap and closing hierarchy ratio failures; trace scale short of 90 px; safe margin and fully independent mask remeasurement remain unresolved.

## Overall design result

Direct-baseline wins: **2/3** (thumbnail and carousel); losses: **1/3** (flyer). Against the Paso 10 owner winners: **1 win, 1 tie, 1 loss**. The Paso 11 acceptance rule requires 3/3 direct wins and zero owner-winner losses, so this is not an accepted Paso 11 result. No technical-to-aesthetic shortcut is used.
