#!/usr/bin/env python3
"""Render the Paso 6 NOCHE LENTA composition repair with original vector art."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm

OUT = Path(__file__).resolve().parent / "renders/step6"
FONT_DIR = ROOT / "skills/cropmark/fonts"
FRAME = (1080, 1350)
BG = (32, 51, 49)          # #203331
BG_ART = (55, 78, 70)      # derived from the locked background palette
BG_LIGHT = (77, 102, 88)   # derived window-sky tone
CREAM = (245, 239, 222)    # #f5efde
ACCENT = (217, 200, 147)   # #d9c893
LEFT = 170
WINDOW = (128, 250, 952, 920)
BLIND_TOP = 296
HEADLINE_SIZE = {"R0": 104, "R1": 96, "R2": 96}
HEADLINE_PITCH = {"R0": 108, "R1": 104, "R2": 104}
OCCLUSION_DEPTH = {"R0": 12, "R1": 5, "R2": 5}

HEADLINES = {
    "R0": {
        "cover": ["Baja", "el día."],
        "inner": ["Prueba una", "rutina sencilla", "para darle sitio", "al descanso."],
        "close": ["Suelta", "por hoy."],
    },
    "R1": {
        "cover": ["Baja", "el día."],
        "inner": ["Prueba una", "rutina sencilla", "para darle sitio", "al descanso."],
        "close": ["Suelta", "por hoy."],
    },
    "R2": {
        "cover": ["Baja", "el día."],
        "inner": ["Prueba una", "rutina sencilla", "para darle sitio", "al descanso."],
        "close": ["Suelta", "por hoy."],
    },
}

HEADLINE_TOPS = {
    "R0": {"cover": 390, "inner": 350, "close": 590},
    "R1": {"cover": 390, "inner": 350, "close": 590},
    "R2": {"cover": 390, "inner": 350, "close": 590},
}

SLIDES = [
    {
        "id": "cover", "role": "cover",
        "headline": ["Baja", "el día."],
        "headline_top": 390,
        "support": ["Una pausa suave al final", "de la tarde."],
        "cta": "SIGUE LEYENDO",
    },
    {
        "id": "inner", "role": "inner",
        "headline": ["Prueba una", "rutina sencilla", "para darle", "sitio al descanso."],
        "headline_top": 300,
        "support": ["Deja una cosa lista para mañana;", "después, apaga lo que te distrae."],
        "cta": "PRUEBA ESTA NOCHE",
    },
    {
        "id": "close", "role": "close",
        "headline": ["Suelta", "por hoy."],
        "headline_top": 590,
        "support": ["Elige un gesto sencillo", "para marcar el cierre."],
        "cta": "GUARDA ESTA PAUSA",
    },
]


def text_top(im, text, font, x, top, color, role, tracking=0):
    return cm.text(im, (x, top - font.getbbox(text)[1]), text, font,
                   fill=color, tracking=tracking, role=role)


def add_brand(im):
    brand_font = cm.font("Outfit-Bold", 44)
    descriptor_font = cm.font("Outfit-Bold", 24)
    brand = text_top(im, "NOCHE LENTA", brand_font, LEFT, 62, CREAM, "logo")
    descriptor = text_top(im, "RITUALES DE DESCANSO", descriptor_font,
                          LEFT, 115, CREAM, "descriptor")
    if descriptor[0] != brand[0] or descriptor[2] > brand[2]:
        raise ValueError("descriptor must share the logo's left edge and remain narrower")
    cm._BOXES.append({"role": "brand-lockup", "box": [*brand[:2], brand[2], descriptor[3]],
                      "label": "descriptor aligned left and narrower than wordmark"})
    return brand, descriptor


def draw_window(im, revision):
    d = ImageDraw.Draw(im)
    left, top, right, bottom = WINDOW
    # Clear glass, sky, a lit sun, and a strong mullion make the scene read as a window.
    d.rectangle(WINDOW, fill=BG_ART)
    d.rectangle((left + 12, top + 12, right - 12, bottom - 12), fill=BG_LIGHT)
    sky = Image.new("RGBA", FRAME, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sky)
    if revision in {"R0", "R1", "R2"}:
        glow = Image.new("RGBA", FRAME, (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse((520, 670, 820, 970), fill=(*ACCENT, 80))
        glow = glow.filter(ImageFilter.GaussianBlur(44))
        im.paste(Image.alpha_composite(im.convert("RGBA"), glow).convert("RGB"))
        sd = ImageDraw.Draw(sky)
        sd.ellipse((590, 720, 770, 900), fill=(*CREAM, 235))
    else:
        sd.ellipse((460, 620, 790, 950), fill=(*ACCENT, 48))
        sd.ellipse((516, 676, 734, 894), fill=(*ACCENT, 96))
        sd.ellipse((556, 716, 694, 854), fill=(*CREAM, 230))
        # Light rays sit behind the muntins and blind, not on the blind itself.
        sd.polygon([(602, 842), (648, 842), (852, 1010), (360, 1010)], fill=(*ACCENT, 36))
    im.paste(Image.alpha_composite(im.convert("RGBA"), sky).convert("RGB"))
    d = ImageDraw.Draw(im)
    d.rectangle(WINDOW, outline=CREAM, width=13)
    d.line((539, top + 2, 539, bottom - 2), fill=CREAM, width=9)
    d.line((left + 2, 566, right - 2, 566), fill=CREAM, width=9)
    d.line((left + 2, bottom - 2, right - 2, bottom - 2), fill=ACCENT, width=7)
    # A narrow spill gives the daylight direction without crossing the copy block.
    if revision in {"R0", "R1", "R2"}:
        spill = Image.new("RGBA", FRAME, (0, 0, 0, 0))
        ImageDraw.Draw(spill).polygon([(660, 914), (714, 914), (960, 1000), (530, 1000)],
                                      fill=(*ACCENT, 30))
        spill = spill.filter(ImageFilter.GaussianBlur(22))
        im.paste(Image.alpha_composite(im.convert("RGBA"), spill).convert("RGB"))
    else:
        spill = Image.new("RGBA", FRAME, (0, 0, 0, 0))
        ImageDraw.Draw(spill).polygon([(604, 914), (686, 914), (1000, 1048), (350, 1048)],
                                      fill=(*ACCENT, 34))
        im.paste(Image.alpha_composite(im.convert("RGBA"), spill).convert("RGB"))
    cm._BOXES.append({"role": "window-light", "text": "", "box": [left, top, right, 1050],
                      "label": "framed sky, sun and light spill behind descending blind"})


def draw_blind_backdrop(im, rail_top, role, revision):
    d = ImageDraw.Draw(im)
    left, _, right, _ = WINDOW
    # Roller housing and side guides are part of the window scene, not a floating card.
    d.rounded_rectangle((left - 21, BLIND_TOP - 43, right + 21, BLIND_TOP + 39),
                        radius=22, fill=ACCENT)
    d.line((left + 23, BLIND_TOP - 18, right - 23, BLIND_TOP - 18),
           fill=CREAM, width=4)
    d.ellipse((left - 10, BLIND_TOP - 29, left + 20, BLIND_TOP + 26), fill=BG_ART)
    d.ellipse((right - 20, BLIND_TOP - 29, right + 10, BLIND_TOP + 26), fill=BG_ART)

    fabric = (left + 17, BLIND_TOP, right - 17, rail_top)
    d.rectangle(fabric, fill=CREAM)
    # A single broad fold gives the fabric depth without adding a secondary texture study.
    d.polygon([(fabric[0], fabric[1]), (fabric[0] + 30, fabric[1]),
               (fabric[0] + 12, fabric[3]), (fabric[0], fabric[3])], fill=(230, 222, 201))
    d.polygon([(fabric[2] - 28, fabric[1]), (fabric[2], fabric[1]),
               (fabric[2], fabric[3]), (fabric[2] - 10, fabric[3])], fill=(230, 222, 201))

    if revision in {"R1", "R2"}:
        # One low-contrast diagonal fold, kept in the clear right edge of the fabric.
        fold = Image.new("RGBA", FRAME, (0, 0, 0, 0))
        if revision == "R1":
            points, alpha, blur = (
                [(right - 64, fabric[1] + 10), (right - 43, fabric[1] + 10),
                 (right - 57, fabric[3] - 10), (right - 78, fabric[3] - 10)], 30, 8
            )
        else:
            points, alpha, blur = (
                [(right - 68, fabric[1] + 18), (right - 50, fabric[1] + 18),
                 (right - 94, fabric[3] - 18), (right - 112, fabric[3] - 18)], 22, 6
            )
        ImageDraw.Draw(fold).polygon(points, fill=(32, 51, 49, alpha))
        fold = fold.filter(ImageFilter.GaussianBlur(blur))
        mask = Image.new("L", FRAME, 0)
        ImageDraw.Draw(mask).rectangle(fabric, fill=255)
        fold.putalpha(Image.composite(fold.getchannel("A"), Image.new("L", FRAME, 0), mask))
        im.paste(Image.alpha_composite(im.convert("RGBA"), fold).convert("RGB"))

    # The sun softly comes through the right half of the cover fabric, balancing its short title.
    if revision in {"R0", "R1", "R2"} and role == "cover":
        light = Image.new("RGBA", FRAME, (0, 0, 0, 0))
        ImageDraw.Draw(light).ellipse((480, fabric[1] + 4, 1000, fabric[3] + 150),
                                      fill=(*ACCENT, 155))
        light = light.filter(ImageFilter.GaussianBlur(46))
        mask = Image.new("L", FRAME, 0)
        ImageDraw.Draw(mask).rectangle(fabric, fill=192)
        light.putalpha(Image.composite(light.getchannel("A"), Image.new("L", FRAME, 0), mask))
        im.paste(Image.alpha_composite(im.convert("RGBA"), light).convert("RGB"))

    # Pull cord stays clear of the frame and title area.
    cord_x = right - 35
    d.line((cord_x, BLIND_TOP + 16, cord_x, rail_top + 84), fill=ACCENT, width=6)
    d.arc((cord_x - 22, rail_top + 57, cord_x + 22, rail_top + 103),
          start=0, end=180, fill=ACCENT, width=6)
    return fabric, cord_x


def headline_rail_top(lines, top, revision):
    size = HEADLINE_SIZE[revision]
    pitch = HEADLINE_PITCH[revision]
    font = cm.font("DMSerifDisplay-Regular", size)
    ink_bottom = max(top + index * pitch + font.getbbox(line)[3] - font.getbbox(line)[1]
                     for index, line in enumerate(lines))
    return ink_bottom - OCCLUSION_DEPTH[revision]


def draw_headline(im, lines, top, revision):
    font = cm.font("DMSerifDisplay-Regular", HEADLINE_SIZE[revision])
    boxes = []
    for index, line in enumerate(lines):
        box = text_top(im, line, font, LEFT, top + index * HEADLINE_PITCH[revision],
                       BG, "headline")
        boxes.append(box)
    group = [min(b[0] for b in boxes), min(b[1] for b in boxes),
             max(b[2] for b in boxes), max(b[3] for b in boxes)]
    return group, boxes


def draw_rail(im, rail_top):
    d = ImageDraw.Draw(im)
    left, _, right, _ = WINDOW
    # The foreground weighted rail crosses the last headline line and visibly removes ink.
    d.rectangle((left + 7, rail_top, right - 7, rail_top + 38), fill=BG)
    d.rectangle((left + 7, rail_top, right - 7, rail_top + 7), fill=ACCENT)
    d.line((left + 16, rail_top + 30, right - 16, rail_top + 30),
           fill=BG_ART, width=4)
    return [left + 7, rail_top, right - 7, rail_top + 38]


def draw_cta(im, label, top):
    font = cm.font("Outfit-Bold", 25)
    text_box = text_top(im, label, font, LEFT, top, ACCENT, "cta", tracking=0.035)
    x = text_box[2] + 24
    y = (text_box[1] + text_box[3]) // 2
    d = ImageDraw.Draw(im)
    d.line((x, y, x + 28, y), fill=ACCENT, width=3)
    d.line((x + 18, y - 8, x + 28, y, x + 18, y + 8), fill=ACCENT, width=3)
    cm._BOXES.append({"role": "navigation-arrow", "text": "", "box": [x, y - 8, x + 29, y + 9],
                      "label": "CTA forward cue"})
    return text_box


def draw_slide(spec, revision="R0"):
    im = cm.new(*FRAME, BG)
    brand, descriptor = add_brand(im)
    draw_window(im, revision)
    # Position the blind edge against actual headline ink so the overlap is deliberate.
    lines = HEADLINES[revision][spec["id"]]
    headline_top = HEADLINE_TOPS[revision][spec["id"]]
    rail_top = headline_rail_top(lines, headline_top, revision)
    fabric, cord_x = draw_blind_backdrop(im, rail_top, spec["role"], revision)
    headline, line_boxes = draw_headline(im, lines, headline_top, revision)
    rail_box = draw_rail(im, rail_top)

    support_font = cm.font("Outfit-Regular", 28)
    support_boxes = [text_top(im, line, support_font, LEFT, 973 + index * 40,
                              CREAM, "subline") for index, line in enumerate(spec["support"])]
    support = [min(b[0] for b in support_boxes), min(b[1] for b in support_boxes),
                max(b[2] for b in support_boxes), max(b[3] for b in support_boxes)]
    cta = draw_cta(im, spec["cta"], 1124)
    if support[3] + 44 > cta[1]:
        raise ValueError(f"support and CTA are too close on {spec['id']}: {support}, {cta}")

    path = OUT / f"slide-{spec['id']}-{revision}.png"
    cm.save(im, str(path))
    sidecar = Path(str(path) + ".boxes.json")
    metadata = json.loads(sidecar.read_text(encoding="utf-8"))
    metadata["study"] = {
        "step": 6, "revision": revision, "slide_role": spec["role"],
        "frame_px": list(FRAME), "direction": "artefact-in-scene",
        "style_card": "text-in-scene", "inventory_item": "last strip of light held by a roller blind",
        "headline_size_px": HEADLINE_SIZE[revision], "headline_pitch_px": HEADLINE_PITCH[revision],
        "headline_top_px": headline_top,
        "headline_ink_box_px": headline, "headline_line_boxes_px": line_boxes,
        "headline_color": "#203331", "fabric_color": "#f5efde",
        "fabric_box_px": list(fabric), "rail_box_px": rail_box,
        "rail_top_y_px": rail_top, "occlusion_depth_px": OCCLUSION_DEPTH[revision],
        "illustration_source": "drawn in code; no third-party pixels",
        "image_text_variable": "foreground rail masks only the lower edge of the final headline line",
        "headline_object_relation": {
            "words": lines[-1], "surface_or_gesture": "headline sits on the blind fabric as it descends",
            "layer_order": "headline on fabric; weighted rail in front",
            "covered_ink_px": OCCLUSION_DEPTH[revision],
            "covered_ink_fraction": round(OCCLUSION_DEPTH[revision] / max(1, line_boxes[-1][3] - line_boxes[-1][1]), 3),
            "feed_check_width_px": 360,
        },
        "fabric_cue": "single soft diagonal fold shade" if revision in {"R1", "R2"} else "side hems only",
        "shared_left_edge_px": LEFT, "cord_x_px": cord_x,
        "brand_wordmark_ink_box_px": brand, "descriptor_ink_box_px": descriptor,
        "support_box_px": support, "cta_ink_box_px": cta,
        "tokens": {"background": "#203331", "headline": "#203331",
                   "fabric": "#f5efde", "accent": "#d9c893"},
        "copy": {"headline": lines, "support": spec["support"], "cta": spec["cta"]},
    }
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": path, "role": spec["role"], "headline": headline,
            "support": support, "cta": cta, "rail_y": rail_top}


def make_feed_sheet(slides, revision):
    thumb_w, thumb_h = 360, 450
    pad, gap, header = 22, 18, 44
    sheet = Image.new("RGB", (pad * 2 + thumb_w * 3 + gap * 2,
                               pad * 2 + header + thumb_h), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(str(FONT_DIR / "Outfit-Bold.ttf"), 19)
    draw.text((pad, pad + 8), f"PASO 6 · {revision} · FEED", fill=CREAM, font=label_font)
    y = pad + header
    for index, slide in enumerate(slides):
        image = Image.open(slide["path"]).convert("RGB").resize(
            (thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(image, (pad + index * (thumb_w + gap), y))
    sheet_path = OUT / f"{revision}-feed-3up.png"
    sheet.save(sheet_path)
    return sheet_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", choices=tuple(OCCLUSION_DEPTH), default="R0")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    slides = [draw_slide(spec, args.revision) for spec in SLIDES]
    sheet = make_feed_sheet(slides, args.revision)
    for item in slides:
        print(f"{item['role']}: {item['path']} headline={item['headline']} support={item['support']} CTA={item['cta']} rail={item['rail_y']}")
    print(sheet)


if __name__ == "__main__":
    main()
