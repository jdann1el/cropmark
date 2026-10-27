#!/usr/bin/env python3
"""Draw the Taller Barro skill sanity check using original code-drawn forms."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm

OUT = Path(__file__).resolve().parent / "renders/step6b"
FONT_DIR = ROOT / "skills/cropmark/fonts"
FRAME = (1080, 1350)
BG = (41, 57, 52)
BG_HI = (56, 75, 68)
CLAY = (227, 199, 158)
CLAY_SHADE = (197, 161, 120)
CLAY_DARK = (155, 107, 79)
TERRA = (198, 112, 79)
INK = (40, 58, 52)
CREAM = (244, 233, 211)
LEFT = 140
HEADLINE_SIZE = 90
HEADLINE_TOP = 500
HEADLINE_PITCH = 108
OCCLUSION_PX = {"R0": 8, "R1": 5, "R2": 5}
TOKENS = {"background": "#293934", "clay": "#e3c79e", "ink": "#283a34",
          "terra": "#c6704f", "headline_size_px": HEADLINE_SIZE}

SLIDES = [
    {"id": "cover", "role": "cover", "headline": ["La forma", "toma cuerpo."],
     "support": ["Una pieza empieza con un gesto."], "cta": "EXPLORA EL TALLER"},
    {"id": "process", "role": "process", "headline": ["Del giro", "nace el borde."],
     "support": ["El torno acompaña cada movimiento."], "cta": "SIGUE EL PROCESO"},
    {"id": "close", "role": "close", "headline": ["Cada huella", "deja memoria."],
     "support": ["Un rastro queda en la superficie."], "cta": "MIRA LAS PIEZAS"},
]


def text_top(im, text, font, x, top, color, role, tracking=0):
    return cm.text(im, (x, top - font.getbbox(text)[1]), text, font,
                   fill=color, tracking=tracking, role=role)


def brand(im):
    wordmark = text_top(im, "TALLER BARRO", cm.font("Outfit-Bold", 42),
                        LEFT, 58, CREAM, "logo")
    descriptor = text_top(im, "CERÁMICA", cm.font("Outfit-Bold", 30),
                          LEFT, 112, CREAM, "descriptor")
    if descriptor[0] != wordmark[0] or descriptor[2] > wordmark[2]:
        raise ValueError("descriptor must share the wordmark edge and remain narrower")
    cm._BOXES.append({"role": "brand-lockup", "text": "",
                      "box": [wordmark[0], wordmark[1], wordmark[2], descriptor[3]]})


def draw_vessel(im):
    d = ImageDraw.Draw(im)
    # One shallow shadow and one broad glaze/fold shade give the clay a tactile cue.
    shadow = Image.new("RGBA", FRAME, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse((188, 886, 902, 1014), fill=(5, 12, 10, 105))
    shadow = shadow.filter(ImageFilter.GaussianBlur(28))
    im.paste(Image.alpha_composite(im.convert("RGBA"), shadow).convert("RGB"))
    d = ImageDraw.Draw(im)
    body = [(360, 303), (720, 303), (800, 382), (900, 416), (980, 488),
            (1015, 603), (1020, 754), (950, 860), (830, 941), (694, 976),
            (386, 976), (250, 941), (130, 860), (60, 754), (65, 603),
            (100, 488), (180, 416), (280, 382)]
    d.polygon(body, fill=CLAY)
    # Single soft side fold, deliberately quiet behind the words.
    d.polygon([(790, 395), (827, 412), (885, 546), (908, 738),
               (867, 853), (832, 874), (864, 744), (840, 560)], fill=CLAY_SHADE)
    # Turned mouth and foot establish the vessel's volume.
    d.ellipse((334, 268, 746, 368), fill=CLAY_SHADE)
    d.ellipse((354, 278, 726, 347), fill=CLAY)
    d.arc((297, 924, 785, 1000), start=5, end=175, fill=CLAY_DARK, width=13)
    d.arc((339, 930, 742, 988), start=5, end=175, fill=(238, 214, 178), width=6)
    cm._BOXES.append({"role": "shape", "text": "vessel body", "box": [60, 268, 1020, 1000]})
    return body


def draw_wheel(im):
    d = ImageDraw.Draw(im)
    d.ellipse((38, 330, 1042, 992), fill=(35, 49, 45))
    d.ellipse((50, 342, 1030, 976), fill=CLAY_SHADE)
    d.ellipse((62, 352, 1018, 956), fill=CLAY)
    # A spiral-like coil rises on the right, leaving a clean field for type.
    pts = [(804, 815), (887, 785), (937, 714), (939, 636), (903, 572),
           (846, 538), (790, 544), (754, 582)]
    d.line(pts, fill=CLAY_DARK, width=23, joint="curve")
    d.line([(x - 2, y - 6) for x, y in pts], fill=(235, 211, 174), width=5, joint="curve")
    d.ellipse((777, 568, 817, 608), fill=CLAY_DARK)
    d.ellipse((784, 572, 802, 592), fill=(235, 211, 174))
    cm._BOXES.append({"role": "shape", "text": "turning wheel and clay coil",
                      "box": [38, 330, 1042, 992]})


def draw_slab(im):
    d = ImageDraw.Draw(im)
    slab = [(77, 340), (964, 350), (1015, 424), (992, 900),
            (920, 958), (155, 938), (70, 886)]
    d.polygon(slab, fill=CLAY)
    d.line([(111, 357), (928, 366)], fill=(242, 221, 188), width=9)
    d.line([(155, 938), (920, 958)], fill=CLAY_SHADE, width=7)
    # A broad dimple, not a texture pattern.
    d.ellipse((764, 567, 994, 804), fill=CLAY_SHADE)
    d.ellipse((794, 591, 963, 771), fill=CLAY)
    d.ellipse((836, 620, 919, 709), fill=CLAY_SHADE)
    d.arc((790, 588, 966, 770), 205, 338, fill=(245, 220, 183), width=8)
    cm._BOXES.append({"role": "shape", "text": "clay slab with thumb impression",
                      "box": [70, 340, 1015, 958]})


def headline(im, spec, revision, surface="vessel"):
    d = ImageDraw.Draw(im)
    font = cm.font("DMSerifDisplay-Regular", HEADLINE_SIZE)
    boxes = []
    for i, line in enumerate(spec["headline"]):
        box = text_top(im, line, font, LEFT, HEADLINE_TOP + i * HEADLINE_PITCH,
                       INK, "headline")
        boxes.append(box)
    lower = boxes[-1][3]
    rail_top = lower - OCCLUSION_PX[revision]
    coil_center = rail_top + 7.5  # 15 px stroke; top edge matches the intended covered ink.

    # The forming coil is physically in front of the marked clay; it crosses
    # only the bottom of the last line. The full copy remains visible at 360 px.
    if spec["id"] == "cover":
        pts = [(156, coil_center), (330, coil_center - 4), (535, coil_center),
               (735, coil_center - 3), (896, coil_center + 2)]
        d.line(pts, fill=CLAY_DARK, width=15, joint="curve")
        d.line([(x, y - 5) for x, y in pts], fill=(244, 221, 185), width=4, joint="curve")
    elif spec["id"] == "process":
        pts = [(198, coil_center + 2), (365, coil_center - 3), (535, coil_center + 1),
               (695, coil_center - 3), (861, coil_center + 3)]
        d.line(pts, fill=CLAY_DARK, width=15, joint="curve")
        d.line([(x, y - 5) for x, y in pts], fill=(244, 221, 185), width=4, joint="curve")
    if spec["id"] in {"cover", "process"}:
        cm._BOXES.append({"role": "shape", "text": "foreground clay coil crossing lower headline edge",
                          "box": [150, rail_top - 2, 900, rail_top + 12]})
    return boxes, rail_top


def draw_slide(spec, revision="R0"):
    im = cm.new(*FRAME, BG)
    brand(im)
    if spec["id"] == "cover":
        draw_vessel(im)
    elif spec["id"] == "process":
        draw_wheel(im)
    else:
        draw_slab(im)
    boxes, rail_top = headline(im, spec, revision)

    support_font = cm.font("Outfit-Regular", 30)
    support_boxes = [text_top(im, line, support_font, LEFT, 1030 + i * 38,
                              CREAM, "subline") for i, line in enumerate(spec["support"])]
    support_union = [min(b[0] for b in support_boxes), min(b[1] for b in support_boxes),
                     max(b[2] for b in support_boxes), max(b[3] for b in support_boxes)]
    cta = text_top(im, spec["cta"], cm.font("Outfit-Bold", 27), LEFT, 1156,
                   (236, 190, 136), "cta", tracking=0.0)
    # Small clay mark gives the CTA an anchor without widening the copy.
    d = ImageDraw.Draw(im)
    d.line((LEFT, 1204, LEFT + 46, 1204), fill=TERRA, width=5)
    cm._BOXES.append({"role": "shape", "text": "CTA underline", "box": [LEFT, 1201, LEFT + 46, 1207]})
    if support_union[3] + 36 > cta[1]:
        raise ValueError(f"support and CTA collide on {spec['id']}: {support_union}, {cta}")

    path = OUT / f"slide-{spec['id']}-{revision}.png"
    cm.save(im, str(path))
    sidecar = Path(str(path) + ".boxes.json")
    metadata = json.loads(sidecar.read_text(encoding="utf-8"))
    metadata["study"] = {
        "step": "6b", "revision": revision, "slide_role": spec["role"],
        "frame_px": list(FRAME), "direction": "artefact-in-scene",
        "style_card": "text-in-scene", "inventory_items": ["coiled clay ribbon", "vessel lip", "potter's wheel", "thumbprint"],
        "headline_size_px": HEADLINE_SIZE, "headline_pitch_px": HEADLINE_PITCH,
        "headline_top_px": HEADLINE_TOP, "headline_line_boxes_px": boxes,
        "surface_or_gesture": ("headline pressed on visible clay; forming coil crosses lower ink"
                                if spec["id"] in {"cover", "process"}
                                else "headline pressed on clay slab beside a thumb impression"),
        "layer_order": ("clay form, headline on clay, foreground coil"
                        if spec["id"] in {"cover", "process"}
                        else "clay slab, headline on surface, impression beside the copy"),
        "covered_ink_px": OCCLUSION_PX[revision] if spec["id"] in {"cover", "process"} else 0,
        "covered_ink_fraction": round(OCCLUSION_PX[revision] / max(1, boxes[-1][3] - boxes[-1][1]), 3) if spec["id"] in {"cover", "process"} else 0,
        "feed_check_width_px": 360, "object_carries_headline": True,
        "shared_left_edge_px": LEFT, "tokens": TOKENS,
        "support_box_px": support_union, "cta_box_px": cta,
        "illustration_source": "shapes and type drawn in code; bundled OFL fonts; no third-party pixels",
        "copy": {"headline": spec["headline"], "support": spec["support"], "cta": spec["cta"]},
    }
    sidecar.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"path": path, "id": spec["id"], "headline": boxes, "support": support_union, "cta": cta,
            "coil_y": rail_top}


def draw_sketch(which):
    im = cm.new(*FRAME, BG)
    brand(im)
    if which == "A":
        draw_vessel(im)
        spec = SLIDES[0]
        font = cm.font("DMSerifDisplay-Regular", 90)
        for i, line in enumerate(spec["headline"]):
            text_top(im, line, font, LEFT, HEADLINE_TOP + i * HEADLINE_PITCH, INK, "headline")
        lower = font.getbbox(spec["headline"][-1])[3] - font.getbbox(spec["headline"][-1])[1] + HEADLINE_TOP + HEADLINE_PITCH
        y = lower - 8
        ImageDraw.Draw(im).line([(156, y + 5), (330, y + 1), (535, y + 5), (735, y + 2), (896, y + 7)],
                                fill=CLAY_DARK, width=15, joint="curve")
        label = "A · VASIJA / TITULAR EN LA ARCILLA"
    else:
        draw_wheel(im)
        font = cm.font("DMSerifDisplay-Regular", 82)
        text_top(im, "Del giro", font, LEFT, 494, INK, "headline")
        text_top(im, "nace el borde.", font, LEFT, 598, INK, "headline")
        d = ImageDraw.Draw(im)
        d.arc((170, 485, 879, 900), 5, 167, fill=CLAY_DARK, width=18)
        label = "B · TORNO / TEXTO ALREDEDOR DEL GIRO"
    font_label = cm.font("Outfit-Bold", 23)
    text_top(im, label, font_label, LEFT, 1270, CREAM, "caption")
    path = OUT / f"sketch-{which}.png"
    cm.save(im, str(path))
    return path


def feed_sheet(items, name, title, thumb_w=360):
    thumb_h = round(thumb_w * FRAME[1] / FRAME[0])
    pad, gap, header = 20, 16, 48
    sheet = Image.new("RGB", (pad * 2 + thumb_w * len(items) + gap * (len(items) - 1),
                               pad * 2 + header + thumb_h), BG)
    d = ImageDraw.Draw(sheet)
    d.text((pad, pad + 8), title, fill=CREAM,
           font=ImageFont.truetype(str(FONT_DIR / "Outfit-Bold.ttf"), 19))
    y = pad + header
    for i, item in enumerate(items):
        path = item["path"] if isinstance(item, dict) else item
        thumb = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        sheet.paste(thumb, (pad + i * (thumb_w + gap), y))
    out = OUT / name
    sheet.save(out)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--stage", choices=("sketches", "representative", "final"), required=True)
    p.add_argument("--revision", choices=tuple(OCCLUSION_PX), default="R0")
    args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.stage == "sketches":
        paths = [draw_sketch("A"), draw_sketch("B")]
        print(feed_sheet(paths, "sketches-feed-2up.png", "STEP 6B · SKETCHES · FEED"))
    elif args.stage == "representative":
        items = [draw_slide(spec, args.revision) for spec in SLIDES[:2]]
        print(feed_sheet(items, f"{args.revision}-representative-feed-2up.png",
                         f"STEP 6B · {args.revision} · COVER + PROCESS"))
        for item in items:
            print(item["path"])
    else:
        items = [draw_slide(spec, args.revision) for spec in SLIDES]
        print(feed_sheet(items, f"{args.revision}-feed-3up.png", f"STEP 6B · {args.revision} · FEED"))
        for item in items:
            print(item["path"])


if __name__ == "__main__":
    main()
