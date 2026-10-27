#!/usr/bin/env python3
"""Render the NOCHE LENTA library-direction study with original vector art."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm

OUT = Path(__file__).resolve().parent / "renders/step4"
FONT_DIR = ROOT / "skills/cropmark/fonts"
FRAME = (1080, 1350)
BG = (32, 51, 49)          # #203331
BG_ART = (43, 63, 59)      # #2b3f3b
CREAM = (245, 239, 222)    # #f5efde
ACCENT = (217, 200, 147)   # #d9c893
MUTED = (113, 132, 122)    # #71847a; decorative only
LEFT = 170
BLIND = (125, 275, 955)
BOTTOMS = {"cover": 790, "inner": 845, "close": 900}
CORD_X = {"R0": 953, "R1": 918, "R2": 918, "R3": 918}
FABRIC_FINISH = {"R0": "flat", "R1": "flat", "R2": "horizontal-weave", "R3": "stitched-hem"}
HEADLINE_SIZE = 76
HEADLINE_PITCH = 88

SLIDES = [
    {
        "id": "cover", "role": "cover",
        "headline": ["Baja el", "día."],
        "support": ["Una pausa suave al final", "de la tarde."],
        "cta": "SIGUE LEYENDO",
    },
    {
        "id": "inner", "role": "inner",
        "headline": ["Prueba una", "rutina sencilla", "para darle sitio", "al descanso."],
        "support": ["Deja una cosa lista para mañana;", "después, apaga lo que te distrae."],
        "cta": "PRUEBA ESTA NOCHE",
    },
    {
        "id": "close", "role": "close",
        "headline": ["Suelta", "por hoy."],
        "support": ["Elige un gesto sencillo", "para marcar el cierre."],
        "cta": "GUARDA ESTA PAUSA",
    },
]


def text_top(im, text, font, x, top, color, role, tracking=0):
    return cm.text(im, (x, top - font.getbbox(text)[1]), text, font,
                   fill=color, tracking=tracking, role=role)


def add_brand(im):
    brand_font = cm.font("Outfit-Bold", 27)
    descriptor_font = cm.font("Outfit-Regular", 14)
    brand = text_top(im, "NOCHE LENTA", brand_font, LEFT, 70, CREAM, "logo")
    descriptor = text_top(im, "RITUALES DE DESCANSO", descriptor_font,
                          LEFT, 108, CREAM, "descriptor", tracking=0.06)
    if descriptor[0] != brand[0] or descriptor[2] > brand[2]:
        raise ValueError("descriptor must share the logo's left edge and remain narrower")
    cm._BOXES.append({"role": "brand-lockup", "box": [*brand[:2], brand[2], descriptor[3]],
                      "label": "descriptor aligned left and narrower than wordmark"})
    return brand, descriptor


def draw_window_and_blind(im, role, revision, bottom=None):
    d = ImageDraw.Draw(im)
    left, top, right = BLIND
    window_bottom = 925
    bottom = BOTTOMS[role] if bottom is None else bottom

    # A window, a last disc of light, and the mechanical roller establish a scene.
    d.rectangle((left, 250, right, window_bottom), fill=BG_ART, outline=MUTED, width=4)
    d.ellipse((440, 720, 640, 920), fill=ACCENT)
    d.line((left + 5, window_bottom - 5, right - 5, window_bottom - 5),
           fill=ACCENT, width=5)

    # Roller housing and end caps.
    d.rounded_rectangle((left - 18, top - 42, right + 18, top + 38),
                        radius=17, fill=ACCENT)
    d.line((left + 18, top - 20, right - 18, top - 20), fill=CREAM, width=3)
    d.ellipse((left - 10, top - 28, left + 18, top + 26), fill=BG_ART)
    d.ellipse((right - 18, top - 28, right + 10, top + 26), fill=BG_ART)

    # The fabric itself is the copy-bearing artefact, with controlled edge and fold detail.
    fabric = (left + 16, top, right - 16, bottom)
    d.rectangle(fabric, fill=CREAM)
    shade = (223, 216, 197)
    d.rectangle((fabric[0], fabric[1], fabric[0] + 8, fabric[3]), fill=shade)
    d.rectangle((fabric[2] - 8, fabric[1], fabric[2], fabric[3]), fill=shade)
    d.line((fabric[0] + 10, fabric[1] + 1, fabric[2] - 10, fabric[1] + 1),
           fill=(255, 250, 238), width=4)
    if FABRIC_FINISH[revision] != "flat":
        # A sewn hem distinguishes cloth from a card without competing with copy.
        weave = (240, 234, 218)
        if FABRIC_FINISH[revision] == "horizontal-weave":
            for yy in range(fabric[1] + 9, bottom - 28, 12):
                d.line((fabric[0] + 10, yy, fabric[2] - 10, yy), fill=weave, width=1)
        seam_y = bottom - 27
        d.line((fabric[0] + 20, seam_y, fabric[2] - 20, seam_y), fill=shade, width=2)
        for xx in range(fabric[0] + 28, fabric[2] - 28, 22):
            d.line((xx, seam_y + 5, xx + 7, seam_y + 5), fill=shade, width=2)

    # Cord and its weighted pull loop stay outside the text-safe textile area.
    cord_x = CORD_X[revision]
    d.line((cord_x, top + 18, cord_x, bottom + 82), fill=ACCENT, width=5)
    d.arc((cord_x - 19, bottom + 52, cord_x + 19, bottom + 96),
          start=0, end=180, fill=ACCENT, width=5)

    # Weighted lower rail: its changing position is the set's visible progression.
    d.rectangle((left + 8, bottom - 9, right - 8, bottom + 12), fill=BG_ART)
    d.line((left + 8, bottom - 9, right - 8, bottom - 9), fill=ACCENT, width=4)
    d.line((left + 14, bottom + 8, right - 14, bottom + 8), fill=MUTED, width=2)

    art_box = [left - 18, top - 42, right + 18, bottom + 96]
    cm._BOXES.append({"role": "illustration", "text": "", "box": art_box,
                      "label": "roller blind, roller, textile, cord, window and light; original vector art"})
    cm._BOXES.append({"role": "window-light", "text": "", "box": [left, 250, right, window_bottom],
                      "label": "last daylight revealed below descending rail"})
    return fabric, bottom, art_box


def draw_headline(im, lines, fabric):
    font = cm.font("DMSerifDisplay-Regular", HEADLINE_SIZE)
    x = LEFT
    max_width = fabric[2] - 42 - x
    total_height = len(lines) * HEADLINE_PITCH
    available = fabric[3] - fabric[1]
    start_y = fabric[1] + max(42, (available - total_height) // 2)
    boxes = []
    for index, line in enumerate(lines):
        box = text_top(im, line, font, x, start_y + index * HEADLINE_PITCH,
                       BG, "headline")
        if box[2] > fabric[2] - 38:
            raise ValueError(f"headline line overflows fabric: {line!r} {box}")
        boxes.append(box)
    group = [min(b[0] for b in boxes), min(b[1] for b in boxes),
             max(b[2] for b in boxes), max(b[3] for b in boxes)]
    if group[0] - fabric[0] != fabric[2] - group[2]:
        # Text is left-aligned, so balanced side padding is not promised here.
        pass
    return group, start_y


def draw_cta(im, label, top):
    font = cm.font("Outfit-Bold", 24)
    text_box = text_top(im, label, font, LEFT, top, ACCENT, "cta", tracking=0.5)
    x = text_box[2] + 24
    y = (text_box[1] + text_box[3]) // 2
    d = ImageDraw.Draw(im)
    d.line((x, y, x + 34, y), fill=ACCENT, width=3)
    d.line((x + 23, y - 10, x + 34, y, x + 23, y + 10), fill=ACCENT, width=3)
    cm._BOXES.append({"role": "navigation-arrow", "text": "", "box": [x, y - 10, x + 35, y + 11],
                      "label": "CTA forward cue"})
    return text_box


def draw_slide(spec, revision="R0"):
    im = cm.new(*FRAME, BG)
    brand, descriptor = add_brand(im)
    fabric, bottom, art_box = draw_window_and_blind(im, spec["role"], revision)
    headline, headline_top = draw_headline(im, spec["headline"], fabric)

    support_font = cm.font("Outfit-Regular", 30)
    support_boxes = [text_top(im, line, support_font, LEFT, 987 + index * 42,
                              CREAM, "subline") for index, line in enumerate(spec["support"])]
    support = [min(b[0] for b in support_boxes), min(b[1] for b in support_boxes),
                max(b[2] for b in support_boxes), max(b[3] for b in support_boxes)]
    cta = draw_cta(im, spec["cta"], 1154)

    if support[3] + 48 > cta[1]:
        raise ValueError(f"support and CTA are too close on {spec['id']}: {support}, {cta}")

    path = OUT / f"slide-{spec['id']}-{revision}.png"
    cm.save(im, str(path))
    sidecar = Path(str(path) + ".boxes.json")
    metadata = json.loads(sidecar.read_text(encoding="utf-8"))
    metadata["study"] = {
        "step": 4, "revision": revision, "slide_role": spec["role"],
        "frame_px": list(FRAME), "direction": "artefact-in-scene",
        "style_card": "text-in-scene", "inventory_item": "last strip of light held by a roller blind",
        "headline_size_px": HEADLINE_SIZE, "headline_pitch_px": HEADLINE_PITCH,
        "headline_ink_box_px": headline, "headline_top_px": headline_top,
        "headline_color": "#203331", "fabric_color": "#f5efde",
        "fabric_box_px": list(fabric), "blind_bottom_rail_y_px": bottom,
        "illustration_box_px": art_box, "illustration_source": "drawn in code; no third-party pixels",
        "image_text_variable": "headline is printed directly on blind textile; rail descends over last light",
        "textile_finish": FABRIC_FINISH[revision],
        "shared_left_edge_px": LEFT,
        "brand_wordmark_ink_box_px": brand, "descriptor_ink_box_px": descriptor,
        "support_box_px": support, "cta_ink_box_px": cta,
        "tokens": {"background": "#203331", "headline": "#203331",
                   "fabric": "#f5efde", "accent": "#d9c893"},
        "copy": {"headline": spec["headline"], "support": spec["support"], "cta": spec["cta"]},
    }
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": path, "role": spec["role"], "headline": headline,
            "support": support, "cta": cta, "rail_y": bottom}


def make_feed_sheet(slides, output):
    thumb_w, thumb_h = 360, 450
    pad, gap, header = 22, 18, 44
    sheet = Image.new("RGB", (pad * 2 + thumb_w * 3 + gap * 2,
                               pad * 2 + header + thumb_h), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(str(FONT_DIR / "Outfit-Bold.ttf"), 19)
    draw.text((pad, pad + 8), "PASO 4 · FEED · SOLO NUESTRAS PIEZAS", fill=CREAM, font=label_font)
    y = pad + header
    for index, slide in enumerate(slides):
        image = Image.open(slide["path"]).convert("RGB").resize(
            (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(image, (pad + index * (thumb_w + gap), y))
    sheet_path = Path(output)
    sheet_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(sheet_path)
    return sheet_path


def add_sketch_window(im, variant):
    d = ImageDraw.Draw(im)
    left, right, top = 125, 955, 275
    d.rectangle((left, 250, right, 925), fill=BG_ART, outline=MUTED, width=4)
    d.ellipse((440, 720, 640, 920), fill=ACCENT)
    bottom = 830
    d.rounded_rectangle((left - 18, top - 42, right + 18, top + 38), radius=17, fill=ACCENT)
    if variant == "A":
        d.rectangle((left + 16, top, right - 16, bottom), fill=CREAM)
        d.line((left + 16, bottom - 9, right - 16, bottom - 9), fill=ACCENT, width=5)
        title_color, title_x = BG, LEFT
        d.line((right - 2, top + 18, right - 2, bottom + 82), fill=ACCENT, width=5)
        d.arc((right - 21, bottom + 52, right + 17, bottom + 96), 0, 180, fill=ACCENT, width=5)
    else:
        # Alternative sketch: copy stays on the wall and the rail crosses its ink.
        d.rectangle((left + 16, top, right - 16, bottom - 10), fill=CREAM)
        font = ImageFont.truetype(str(FONT_DIR / "DMSerifDisplay-Regular.ttf"), 78)
        d.text((LEFT, 370), "Baja el día.", font=font, fill=BG)
        d.rectangle((left + 8, 445, right - 8, 470), fill=BG_ART)
        d.line((left + 8, 445, right - 8, 445), fill=ACCENT, width=4)
        title_color, title_x = BG, LEFT
    if variant == "A":
        font = ImageFont.truetype(str(FONT_DIR / "DMSerifDisplay-Regular.ttf"), 78)
        d.text((title_x, 370), "Baja el", font=font, fill=title_color)
        d.text((title_x, 460), "día.", font=font, fill=title_color)
    return im


def render_sketches():
    OUT.mkdir(parents=True, exist_ok=True)
    sketches = []
    for variant in ("A", "B"):
        im = cm.new(*FRAME, BG)
        add_brand(im)
        add_sketch_window(im, variant)
        path = OUT / f"sketch-{variant}.png"
        cm.save(im, str(path))
        sketches.append(path)
    thumb_w, thumb_h = 360, 450
    pad, gap, header = 22, 20, 50
    sheet = Image.new("RGB", (pad * 2 + thumb_w * 2 + gap,
                               pad * 2 + header + thumb_h + 32), BG)
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype(str(FONT_DIR / "Outfit-Bold.ttf"), 19)
    d.text((pad, pad + 4), "PASO 4 · BOCETOS · SOLO NUESTRAS PIEZAS", fill=CREAM, font=font)
    labels = ["A · tejido que lleva el titular", "B · riel que cruza el titular"]
    for i, path in enumerate(sketches):
        thumb = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + i * (thumb_w + gap)
        sheet.paste(thumb, (x, pad + header))
        d.text((x, pad + header + thumb_h + 4), labels[i], fill=CREAM, font=font)
    sheet_path = OUT / "sketches-feed.png"
    sheet.save(sheet_path)
    print("\n".join(str(x) for x in sketches))
    print(sheet_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sketches", action="store_true")
    parser.add_argument("--revision", choices=("R0", "R1", "R2", "R3"), default="R0")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.sketches:
        render_sketches()
        return
    slides = [draw_slide(spec, args.revision) for spec in SLIDES]
    sheet = make_feed_sheet(slides, OUT / f"{args.revision}-feed-3up.png")
    for item in slides:
        print(f"{item['role']}: {item['path']} headline={item['headline']} support={item['support']} CTA={item['cta']} rail={item['rail_y']}")
    print(sheet)


if __name__ == "__main__":
    main()
