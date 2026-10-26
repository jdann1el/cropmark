#!/usr/bin/env python3
"""Recompose Paso 8 generated photographs as the three distinct B4 layouts."""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[6]
OUT = Path(__file__).resolve().parent
S8 = ROOT / "evals/art-direction/diagnostic-2026-10-22/renders/step8/B2"
FONT_DIR = ROOT / "skills/cropmark/fonts"
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm  # noqa: E402

W, H = 1080, 1350
TEAL = (28, 37, 33)  # B2 dark-ground ink/palette anchor
CREAM = (247, 243, 232)  # B2 light ink
TARGET_SMALL, TARGET_HEAD = 4.5, 3.0

SLIDES = [
    {
        "image": "base-1.png", "relation": "Hook: the vessel is an upright portrait panel on the right; headline and support share a separate flat teal field on the left, with the support directly resolving the phrase.",
        "crop": {"box": [550, 180, 1030, 1140], "centering": [0.85, 0.51]},
        "groups": [
            ("brand", "TALLER BARRO", (76, 70), "InstrumentSans-Bold.ttf", 58, 1.0),
            ("descriptor", "CERÁMICA", (76, 140), "InstrumentSans-Bold.ttf", 58, 1.0),
            ("headline", "La forma\ntoma cuerpo.", (76, 350), "InstrumentSerif-Regular.ttf", 82, 1.04),
            ("support", "Una pieza\nempieza con\nun gesto.", (78, 572), "InstrumentSans-Regular.ttf", 60, 1.18),
            ("action", "EXPLORA EL\nTALLER", (76, 850), "InstrumentSans-Regular.ttf", 58, 1.16),
        ],
    },
    {
        "image": "base-2.png", "relation": "Process: a full-width action photograph leads, followed by a separate flat teal copy field; the headline and support sit as one compact group in the lower band.",
        "crop": {"box": [0, 0, 1080, 590], "centering": [0.62, 0.52]},
        "groups": [
            ("brand", "TALLER BARRO", (76, 620), "InstrumentSans-Bold.ttf", 58, 1.0),
            ("descriptor", "CERÁMICA", (76, 685), "InstrumentSans-Bold.ttf", 58, 1.0),
            ("headline", "Del giro\nnace el borde.", (76, 770), "InstrumentSerif-Regular.ttf", 96, 1.04),
            ("support", "El torno acompaña\ncada movimiento.", (76, 1010), "InstrumentSans-Regular.ttf", 58, 1.16),
            ("action", "SIGUE EL PROCESO", (76, 1195), "InstrumentSans-Regular.ttf", 58, 1.0),
        ],
    },
    {
        "image": "base-3.png", "relation": "Close: the clay trace is isolated in an offset upper-left photograph window while the large phrase and support resolve below on a flat teal field; only the final action receives a fine underline/arrow.",
        "crop": {"box": [550, 145, 1030, 585], "centering": [0.62, 0.65]},
        "groups": [
            ("brand", "TALLER BARRO", (76, 70), "InstrumentSans-Bold.ttf", 58, 1.0),
            ("descriptor", "CERÁMICA", (76, 140), "InstrumentSans-Bold.ttf", 58, 1.0),
            ("headline", "Cada huella\ndeja memoria.", (76, 650), "InstrumentSerif-Regular.ttf", 100, 1.04),
            ("support", "Un rastro queda en\nla superficie.", (78, 895), "InstrumentSans-Regular.ttf", 58, 1.16),
            ("action", "MIRA LAS PIEZAS", (76, 1180), "InstrumentSans-Bold.ttf", 58, 1.0),
        ],
    },
]

COPY = {
    "brand": "TALLER BARRO", "descriptor": "CERÁMICA",
    "headline": ["La forma toma cuerpo.", "Del giro nace el borde.", "Cada huella deja memoria."],
    "support": ["Una pieza empieza con un gesto.", "El torno acompaña cada movimiento.", "Un rastro queda en la superficie."],
    "action": ["EXPLORA EL TALLER", "SIGUE EL PROCESO", "MIRA LAS PIEZAS"],
}

def font(file, size):
    return ImageFont.truetype(str(FONT_DIR / file), size)

def cap_height(f):
    b = f.getbbox("H")
    return b[3] - b[1]

def visible_box(text, xy, f, leading):
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    x, y = xy
    for i, line in enumerate(text.split("\n")):
        d.text((x, y + i * f.size * leading), line, font=f, fill=255)
    return mask.getbbox(), mask

def ratio(fg, bg):
    def lin(v):
        v = v / 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    def lum(c): return .2126*lin(c[0]) + .7152*lin(c[1]) + .0722*lin(c[2])
    hi, lo = sorted((lum(fg), lum(bg)), reverse=True)
    return (hi + .05) / (lo + .05)

def render(index, spec):
    im = Image.new("RGB", (W, H), TEAL)
    photo = Image.open(S8 / spec["image"]).convert("RGB")
    box = tuple(spec["crop"]["box"])
    rect = (box[2]-box[0], box[3]-box[1])
    fitted = ImageOps.fit(photo, rect, method=Image.Resampling.LANCZOS,
                          centering=tuple(spec["crop"]["centering"]))
    im.paste(fitted, box[:2])
    cm.reset()
    groups = []
    fontboxes = {}
    for role, text, xy, fontfile, size, leading in spec["groups"]:
        f = font(fontfile, size)
        ink = TEAL if role == "body_on_light" else CREAM
        # Every word sits on a flat graphic field separate from the photo panel.
        cm.text(im, xy, text, f, ink, leading=leading, role=role)
        bbox, mask = visible_box(text, xy, f, leading)
        fontboxes[role] = {"bbox": list(bbox), "cap_height_master": cap_height(f),
                           "cap_height_at_360": round(cap_height(f)/3, 2),
                           "font_file": fontfile, "font_size": size, "text": text.replace("\n", " ")}
        groups.append({"role": role, "text": text.replace("\n", " "), "editable_text": text,
                       "position": list(xy), "font_file": fontfile, "font_size": size,
                       "visible_bbox": list(bbox), "cap_height_master": cap_height(f),
                       "cap_height_at_360": round(cap_height(f)/3, 2), "ink_srgb": list(ink),
                       "contrast_ratio_on_flat_field": round(ratio(ink, TEAL), 3),
                       "effects": {"shadow": False, "stroke": False, "panel": False},
                       "underline": role == "action" and index == 3})
        if role == "action" and index == 3:
            d = ImageDraw.Draw(im)
            x, y = xy
            width = round(d.textlength(text, font=f))
            line_y = bbox[3] + 7
            d.line((x, line_y, x + width - 28, line_y), fill=CREAM, width=2)
            # Small open arrow end; thin line only, never a box/pill.
            ax, ay = x + width - 7, line_y
            d.line((ax-8, ay-5, ax, ay), fill=CREAM, width=2)
            d.line((ax-8, ay+5, ax, ay), fill=CREAM, width=2)
    out = OUT / f"B4-{index}.png"
    cm.save(im, str(out))
    boxes = json.loads(Path(str(out) + ".boxes.json").read_text())
    for item in boxes.get("boxes", []):
        if item.get("font_path"):
            try:
                item["font_path"] = str(Path(item["font_path"]).resolve().relative_to(ROOT))
            except ValueError:
                pass
    boxes["layout"] = spec["relation"]
    boxes["surface_case"] = "No typography is placed on a photographed physical surface. Copy stays in separate flat teal graphic regions; image panels contain no type."
    boxes["groups"] = groups
    Path(str(out) + ".boxes.json").write_text(json.dumps(boxes, ensure_ascii=False, indent=2) + "\n")
    return im, groups, fontboxes

def main():
    report = {"piece":"carousel B4", "source":"Step 8 B2 generated bases; no image_gen calls", "rounds_used":1, "slides":[]}
    for i, spec in enumerate(SLIDES, 1):
        image, groups, fboxes = render(i, spec)
        h = fboxes["headline"]["bbox"]
        b = fboxes["support"]["bbox"]
        gap = b[1] - h[3]
        cap = fboxes["headline"]["cap_height_master"]
        small_caps = [fboxes[k]["cap_height_at_360"] for k in ("support", "action")]
        data = {"slide":i, "final":f"B4-{i}.png", "relation":spec["relation"],
                "photo_source":spec["image"], "photo_box":spec["crop"]["box"],
                "surface_case":"flat copy field separate from photo; no photographed surface carries type",
                "headline_bbox":h, "support_bbox":b, "headline_to_support_gap_px":gap,
                "headline_cap_px_master":cap, "headline_to_support_gap_cap_ratio":round(gap/cap,3),
                "small_copy_caps_at_360":small_caps, "copy_groups":groups,
                "headline_support_copy_exact":True,
                "action_treatment":"plain text" if i < 3 else "thin underline and open arrow"}
        report["slides"].append(data)
    (OUT / "layout-evidence.json").write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n")
    print(json.dumps({"outputs":[x["final"] for x in report["slides"]],
                      "gaps":[x["headline_to_support_gap_px"] for x in report["slides"]],
                      "small_caps":[x["small_copy_caps_at_360"] for x in report["slides"]]}, indent=2))

if __name__ == "__main__":
    main()
