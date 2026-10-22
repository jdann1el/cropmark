#!/usr/bin/env python3
"""Render the original NOCHE LENTA Step 3 image/text relationship study."""
from pathlib import Path
import json
import argparse
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm

OUT = Path(__file__).resolve().parent / "renders/step3"
FONT_DIR = ROOT / "skills/cropmark/fonts"
BG = (32, 51, 49)             # #203331
BG_ART = (43, 63, 59)         # quiet surface, same on every card
CREAM = (245, 239, 222)       # #f5efde
ACCENT = (217, 200, 147)      # #d9c893
MUTED = (113, 132, 122)       # #71847a
LEFT = 187
FRAME = (1080, 1350)
HEADLINE_SIZE = 86
HEADLINE_TOPS = (324, 434)
ART_A = (555, 440)
ART_B_R0_X = {"cover": 300, "inner": 300}
# R1 changes only the horizontal framing of direction B's illustrations.
ART_B_R1_X = {"cover": 390, "inner": 470}
ART_B_R2_X = {"cover": 390, "inner": 510}
ART_SIZE = (280, 190)
RULE_Y = 672

SLIDES = [
    {
        "id": "cover",
        "role": "portada",
        "headline": ["Lo pendiente", "va en…"],
        "subline": ["Escribe una línea.", "Suelta el resto por hoy."],
        "cta": "CIERRA EL DÍA",
        "art": "notebook",
        "art_label": "libreta cerrada",
        "art_description": "libreta: respuesta visual a «va en…»",
        "footer": "NOCHE LENTA  ·  01 / 02",
    },
    {
        "id": "inner",
        "role": "interior",
        "headline": ["Mañana empieza", "con esto:"],
        "subline": ["Elige una sola cosa", "para dejar preparada."],
        "cta": "ELIGE UNA SOLA COSA",
        "art": "checklist",
        "art_label": "lista breve",
        "art_description": "lista: referente visual de «esto»",
        "footer": "NOCHE LENTA  ·  02 / 02",
    },
]


def union(boxes):
    boxes = [b for b in boxes if b]
    return ([min(b[0] for b in boxes), min(b[1] for b in boxes),
             max(b[2] for b in boxes), max(b[3] for b in boxes)] if boxes else None)


def text_top(im, text, font, x, top, color, role, tracking=0):
    return cm.text(im, (x, top - font.getbbox(text)[1]), text, font,
                   fill=color, tracking=tracking, role=role)


def draw_notebook(im, x, y):
    """Own vector illustration; a closed book that answers the cover phrase."""
    d = ImageDraw.Draw(im)
    # Offset page block and cover create a readable closed, horizontal notebook.
    d.rounded_rectangle([x + 12, y + 9, x + 276, y + 185], radius=13,
                        fill=BG, outline=MUTED, width=3)
    d.rounded_rectangle([x + 4, y + 3, x + 267, y + 176], radius=13,
                        fill=BG_ART, outline=ACCENT, width=4)
    d.line([x + 30, y + 9, x + 30, y + 169], fill=ACCENT, width=3)
    d.line([x + 39, y + 13, x + 39, y + 165], fill=MUTED, width=2)
    # Small closed-book mark and restrained ruled strokes.
    d.ellipse([x + 72, y + 50, x + 104, y + 82], outline=ACCENT, width=3)
    d.arc([x + 79, y + 57, x + 97, y + 75], start=185, end=355, fill=ACCENT, width=2)
    d.line([x + 79, y + 70, x + 98, y + 70], fill=ACCENT, width=2)
    label = cm.font("Outfit-Bold", 20)
    text_top(im, "HOY", label, x + 120, y + 47, CREAM, "illustration-label")
    d.line([x + 120, y + 91, x + 235, y + 91], fill=MUTED, width=3)
    d.line([x + 120, y + 112, x + 217, y + 112], fill=MUTED, width=3)
    d.line([x + 120, y + 133, x + 228, y + 133], fill=MUTED, width=3)
    cm._BOXES.append({"role": "illustration", "text": "", "box": [x, y, x + 280, y + 190],
                      "label": "libreta cerrada original, vectorial"})
    return [x, y, x + 280, y + 190]


def draw_checklist(im, x, y):
    """Own vector illustration; a short list that answers the inner phrase."""
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([x + 12, y + 9, x + 276, y + 185], radius=13,
                        fill=BG, outline=MUTED, width=3)
    d.rounded_rectangle([x + 4, y + 3, x + 267, y + 176], radius=13,
                        fill=BG_ART, outline=ACCENT, width=4)
    d.line([x + 24, y + 40, x + 247, y + 40], fill=ACCENT, width=3)
    label = cm.font("Outfit-Bold", 20)
    text_top(im, "MAÑANA", label, x + 24, y + 13, CREAM, "illustration-label")
    for index, yy in enumerate((y + 65, y + 105, y + 145)):
        d.rounded_rectangle([x + 26, yy, x + 47, yy + 21], radius=4,
                            outline=ACCENT, width=3)
        if index == 0:
            d.line([x + 30, yy + 11, x + 36, yy + 17, x + 45, yy + 5],
                   fill=CREAM, width=3)
        d.line([x + 63, yy + 10, x + (225 if index != 1 else 198), yy + 10],
               fill=MUTED if index == 2 else CREAM, width=3)
    cm._BOXES.append({"role": "illustration", "text": "", "box": [x, y, x + 280, y + 190],
                      "label": "lista breve original, vectorial"})
    return [x, y, x + 280, y + 190]


def add_pill(im, label, top):
    font = cm.font("Outfit-Regular", 22)
    tracking = 0.045
    text_width = font.getlength(label) + tracking * font.size * max(0, len(label) - 1)
    width, height = round(text_width + 54), 58
    box = [LEFT, top, LEFT + width, top + height]
    ImageDraw.Draw(im).rounded_rectangle(box, radius=29, fill=BG, outline=ACCENT, width=3)
    cm._BOXES.append({"role": "pill-shape", "text": "", "box": box,
                      "fill": list(BG), "outline": list(ACCENT), "stroke_width": 3})
    bb = font.getbbox(label)
    center_top = top + (height - (bb[3] - bb[1])) / 2
    cm.text(im, (LEFT + width / 2, center_top - bb[1]), label, font,
            anchor="ma", tracking=tracking, fill=ACCENT, role="cta")
    return box


def draw_slide(spec, direction, revision="R0"):
    im = cm.new(*FRAME, BG)
    if direction == "A":
        image_xy = ART_A
    else:
        art_x = {"R0": ART_B_R0_X, "R1": ART_B_R1_X,
                 "R2": ART_B_R2_X, "R3": ART_B_R2_X}[revision][spec["id"]]
        image_xy = (art_x, ART_A[1])
    if spec["art"] == "notebook":
        art_box = draw_notebook(im, *image_xy)
    else:
        art_box = draw_checklist(im, *image_xy)

    # Same copy, alignment, size, fonts and colours for both directions.
    logo_font = cm.font("Outfit-Regular", 27)
    descriptor_font = cm.font("Outfit-Regular", 18)
    text_top(im, "NOCHE LENTA", logo_font, LEFT, 164, CREAM, "logo", tracking=0.105)
    text_top(im, "RITUALES DE DESCANSO", descriptor_font, LEFT, 202,
             CREAM, "descriptor", tracking=0.13)

    title_font = cm.font("DMSerifDisplay-Regular", HEADLINE_SIZE)
    title_boxes = []
    for line, top in zip(spec["headline"], HEADLINE_TOPS):
        title_boxes.append(text_top(im, line, title_font, LEFT, top, CREAM,
                                    "headline"))
    headline_box = union(title_boxes)
    headline_width = headline_box[2] - headline_box[0]

    rule_width = round(headline_width * 1.02)
    ImageDraw.Draw(im).line([LEFT, RULE_Y + 1, LEFT + rule_width - 1, RULE_Y + 1],
                            fill=CREAM, width=3)
    rule_box = [LEFT, RULE_Y, LEFT + rule_width, RULE_Y + 3]
    cm._BOXES.append({"role": "rule", "text": "", "box": rule_box,
                      "fill": list(CREAM), "size": 3})

    sub_font = cm.font("Outfit-Regular", 30)
    sub_boxes = [text_top(im, line, sub_font, LEFT, 712 + index * 40,
                          CREAM, "subline") for index, line in enumerate(spec["subline"])]
    sub_box = union(sub_boxes)
    pill_box = add_pill(im, spec["cta"], 846)

    footer_font = cm.font("Outfit-Regular", 18)
    marker_color = MUTED if revision == "R0" else ACCENT
    text_top(im, spec["footer"], footer_font, LEFT, 1138, marker_color,
             "page-marker", tracking=0.09)

    path = OUT / f"direction-{direction}-{spec['id']}-{revision}.png"
    cm.save(im, str(path))
    sidecar = Path(str(path) + ".boxes.json")
    metadata = json.loads(sidecar.read_text())
    metadata["study"] = {
        "step": 3,
        "direction": direction,
        "relationship": ("illustration follows the phrase and supplies its missing referent"
                         if direction == "A" else
                         "illustration sits behind the headline; letters visibly occlude its surface"),
        "slide_role": spec["role"],
        "frame_px": list(FRAME),
        "headline_size_px": HEADLINE_SIZE,
        "headline_ink_width_px": headline_width,
        "rule_to_headline_width_pct": round(rule_width * 100 / headline_width, 2),
        "illustration_box_px": art_box,
        "illustration": spec["art_description"],
        "illustration_source": "drawn in code; no third-party pixels",
        "image_text_variable": "illustration placement relative to headline",
        "revision": revision,
        "fixed_comparison_tokens": {
            "left_inset_px": LEFT,
            "headline_font": "DM Serif Display Regular",
            "support_font": "Outfit Regular",
            "headline_size_px": HEADLINE_SIZE,
            "background": "#203331",
            "headline_colour": "#f5efde",
            "accent": "#d9c893",
            "illustration_surface": "#2b3f3b",
            "page_marker": "#71847a" if revision == "R0" else "#d9c893",
            "copy": spec["headline"],
        },
    }
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    return {
        "path": path,
        "direction": direction,
        "role": spec["role"],
        "headline": headline_box,
        "headline_width": headline_width,
        "rule": rule_box,
        "subline": sub_box,
        "pill": pill_box,
        "art": art_box,
    }


def make_feed_sheet(slides, output):
    thumb_w, thumb_h = 360, 450
    pad, gap, label_h = 22, 20, 44
    sheet = Image.new("RGB", (pad * 2 + thumb_w * 2 + gap,
                               pad * 2 + (thumb_h + label_h) * 2 + gap), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(str(FONT_DIR / "Outfit-Bold.ttf"), 18)
    slots = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for item, (col, row) in zip(slides, slots):
        x = pad + col * (thumb_w + gap)
        y = pad + row * (thumb_h + label_h + gap)
        caption = f"DIRECCIÓN {item['direction']}  ·  {item['role'].upper()}"
        draw.text((x, y + 8), caption, fill=CREAM, font=label_font)
        thumb = Image.open(item["path"]).convert("RGB").resize(
            (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (x, y + label_h))
    sheet_path = Path(output)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path)
    return sheet_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", choices=("R0", "R1", "R2", "R3"), default="R0")
    parser.add_argument("--directions", choices=("A", "B", "both"), default="both")
    parser.add_argument("--slides", choices=("cover", "inner", "both"), default="both")
    parser.add_argument("--final-feed", action="store_true",
                        help="build final sheet from A-R1, B-cover-R2 and B-inner-R3")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.final_feed:
        final_slides = []
        for direction, revision in (("A", "R1"), ("B", "R2")):
            for spec in SLIDES:
                item_revision = "R3" if direction == "B" and spec["id"] == "inner" else revision
                final_slides.append({
                    "path": OUT / f"direction-{direction}-{spec['id']}-{item_revision}.png",
                    "direction": direction,
                    "role": spec["role"],
                })
        sheet = make_feed_sheet(final_slides, OUT / "final-feed-2x2.png")
        print(sheet)
        return
    results = []
    directions = ("A", "B") if args.directions == "both" else (args.directions,)
    specs = SLIDES if args.slides == "both" else [s for s in SLIDES if s["id"] == args.slides]
    for direction in directions:
        for spec in specs:
            results.append(draw_slide(spec, direction, args.revision))
    if args.revision == "R0" and args.directions == "both":
        sheet = make_feed_sheet(results, OUT / "R0-feed-2x2.png")
    else:
        sheet = None
    for item in results:
        print(f"{item['path']} | headline={item['headline']} ({item['headline_width']}px) "
              f"rule={item['rule']} art={item['art']} subline={item['subline']} pill={item['pill']}")
    if sheet:
        print(sheet)


if __name__ == "__main__":
    main()
