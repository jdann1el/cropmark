# Pillow engine
`import sys; sys.path.insert(0, '<skill>/engines/pillow'); import cm`
Typical thumbnail: `im = cm.cover('base.png', 1280, 720, focus=(.5,.4)); im = cm.grade(im); im = cm.shade(im,'left',.55); cm.text(im,(70,90),'HOOK\nWORDS', cm.fit('HOOK\nWORDS','Anton-Regular',560), stroke=0, shadow=(0,8,18,.6)); cm.save(im,'out/thumb.jpg')`
Functions: reset, font(weight=), new, cover(zoom=), grade, shade, vignette, text (tracking keeps kerning/leading/stroke/shadow/align), fit, rounded, card, pill, sticky (rotated note), rotated, blur_region, halftone, torn_mask, key_out, despill, paste, compare_sheet (before/after sheet), save(boxes_dir=) → .boxes.json for QA.
Call `cm.reset()` once per output (cover() no longer clears boxes, so composites keep them).
