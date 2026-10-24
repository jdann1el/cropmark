#!/usr/bin/env python3
"""Compose and measure the three Step 8 B2 slides without altering A or B."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[4]
sys.path.insert(0, str(REPO / "skills/cropmark/engines/pillow"))
import cm  # noqa: E402

W, H = 1080, 1350
LEFT = 112
LIGHT = (247, 243, 232)
DARK = (28, 37, 33)
FONT_DIR = REPO / "skills/cropmark/fonts"
FINAL_DIR = ROOT / "B2"
ROUND_DIR = ROOT / "rounds/R0"

SLIDES = [
    {
        "headline": "La forma\ntoma cuerpo.",
        "support": "Una pieza empieza\ncon un gesto.",
        "cta": "EXPLORA EL TALLER",
    },
    {
        "headline": "Del giro\nnace el borde.",
        "support": "El torno acompaña\ncada movimiento.",
        "cta": "SIGUE EL PROCESO",
    },
    {
        "headline": "Cada huella\ndeja memoria.",
        "support": "Un rastro queda en\nla superficie.",
        "cta": "MIRA LAS PIEZAS",
    },
]

FONTS = {
    "headline": ("InstrumentSerif-Regular.ttf", 108),
    "brand": ("InstrumentSans-Bold.ttf", 30),
    "descriptor": ("InstrumentSans-Bold.ttf", 27),
    "support": ("InstrumentSans-Regular.ttf", 34),
    "cta": ("InstrumentSans-Bold.ttf", 28),
}
POSITIONS = {
    "brand": (LEFT, 82),
    "descriptor": (LEFT, 126),
    "headline": (LEFT, 220),
    "support": (LEFT, 956),
    "cta": (LEFT, 1128),
}
LEADING = {"headline": 1.04, "support": 1.24}
THRESHOLD = {"brand": 4.5, "descriptor": 4.5, "headline": 3.0, "support": 4.5, "cta": 4.5}


def lin(v: int) -> float:
    v = v / 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def luminance(rgb) -> float:
    return 0.2126 * lin(rgb[0]) + 0.7152 * lin(rgb[1]) + 0.0722 * lin(rgb[2])


def cr(fg, bg) -> float:
    a, b = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def percentile(values, p):
    ordered = sorted(values)
    index = int(math.floor((len(ordered) - 1) * p))
    return ordered[index]


def fitted(path: Path) -> Image.Image:
    return ImageOps.fit(Image.open(path).convert("RGB"), (W, H), method=Image.Resampling.LANCZOS)


def font(role):
    name, size = FONTS[role]
    return ImageFont.truetype(str(FONT_DIR / name), size)


def mask_for(im, role, copy):
    f = font(role)
    x, y = POSITIONS[role]
    leading = LEADING.get(role, 1.0)
    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    for i, line in enumerate(copy.split("\n")):
        d.text((x, y + i * f.size * leading), line, font=f, fill=255)
    return mask.point(lambda v: 255 if v >= 250 else 0)


def sample_metrics(base, mask, ink):
    rgb = base.convert("RGB")
    pixels = [p for p, a in zip(rgb.getdata(), mask.getdata()) if a >= 250]
    if not pixels:
        raise ValueError("empty glyph-core mask")
    ratios = [cr(ink, p) for p in pixels]
    lums = [luminance(p) for p in pixels]
    return {
        "glyph_core_pixels": len(pixels),
        "background_luminance_p05": round(percentile(lums, 0.05), 4),
        "background_luminance_median": round(percentile(lums, 0.50), 4),
        "contrast_p05": round(percentile(ratios, 0.05), 2),
        "contrast_median": round(percentile(ratios, 0.50), 2),
        "under_target_percent": round(100 * sum(r < THRESHOLD[ROLE] for r in ratios) / len(ratios), 2),
    }


def choose_ink(base, role, copy):
    global ROLE
    ROLE = role
    mask = mask_for(base, role, copy)
    candidates = {"light": LIGHT, "dark": DARK}
    stats = {name: sample_metrics(base, mask, color) for name, color in candidates.items()}
    # Choose by the weakest local pixels (P05), then keep the selected role ink stable.
    selected = max(candidates, key=lambda name: stats[name]["contrast_p05"])
    return candidates[selected], {"selected": selected, "candidates": stats, "selected_metrics": stats[selected]}


def draw_text(im, role, copy, ink):
    cm.text(im, POSITIONS[role], copy, font(role), ink,
            leading=LEADING.get(role, 1.0), role=role)


def compose_one(index, spec):
    base_path = FINAL_DIR / f"base-{index}.png"
    base = fitted(base_path)
    im = base.copy()
    cm.reset()
    report = {"slide": index, "base": base_path.name, "size": [W, H], "groups": {}}
    copies = {
        "brand": "TALLER BARRO",
        "descriptor": "CERÁMICA",
        "headline": spec["headline"],
        "support": spec["support"],
        "cta": spec["cta"],
    }
    for role in ("brand", "descriptor", "headline", "support", "cta"):
        ink, measured = choose_ink(base, role, copies[role])
        draw_text(im, role, copies[role], ink)
        report["groups"][role] = {
            "text": copies[role].replace("\n", " "),
            "position": list(POSITIONS[role]),
            "font": FONTS[role][0],
            "font_size": FONTS[role][1],
            "fill": list(ink),
            "effects": {"shadow": False, "outline": False, "plate": False},
            "contrast": measured,
            "target_ratio": THRESHOLD[role],
        }
    out = FINAL_DIR / f"final-{index}.png"
    cm.save(im, str(out))
    report["boxes_file"] = out.name + ".boxes.json"
    return im, report


def write_feed(finals):
    a_dir = ROOT.parent / "step7/A"
    b_dir = ROOT.parent / "step7/B"
    rows = [
        ("A · directo", [Image.open(a_dir / f"final-{i}.png").convert("RGB") for i in range(1, 4)]),
        ("B · Cropmark", [Image.open(b_dir / f"slide-{i}.png").convert("RGB") for i in range(1, 4)]),
        ("B2 · zonas medidas", finals),
    ]
    label_h = 34
    sheet = Image.new("RGB", (W, 3 * (H // 3 + label_h)), (244, 241, 232))
    # Every thumbnail is exactly 360 × 450; rows have a 34 px label band.
    y = 0
    label_font = ImageFont.truetype(str(FONT_DIR / "InstrumentSans-Bold.ttf"), 22)
    for label, images in rows:
        ImageDraw.Draw(sheet).text((18, y + 6), label, font=label_font, fill=(31, 42, 37))
        y += label_h
        for col, image in enumerate(images):
            sheet.paste(image.resize((360, 450), Image.Resampling.LANCZOS), (col * 360, y))
        y += 450
    # The construction above is 3×484 = 1452 high.
    sheet = sheet.crop((0, 0, W, y))
    path = ROOT / "AB2-feed.png"
    sheet.save(path)
    ROUND_DIR.mkdir(parents=True, exist_ok=True)
    sheet.save(ROUND_DIR / "R0-initial-feed-AB2.png")
    return path


def main():
    finals, reports = [], []
    for index, spec in enumerate(SLIDES, start=1):
        image, report = compose_one(index, spec)
        finals.append(image)
        reports.append(report)
    feed = write_feed(finals)
    ROUND_DIR.mkdir(parents=True, exist_ok=True)
    (ROUND_DIR / "contrast-R0.json").write_text(json.dumps(reports, ensure_ascii=False, indent=2) + "\n")
    (ROUND_DIR / "render-log.json").write_text(json.dumps({
        "round": 0,
        "cause": "Initial B2 composition from the three inspected generated bases.",
        "variable": "Measured ink by actual glyph-core pixels; common left edge, headline scale, and quiet-zone placements.",
        "prediction": "Light ink will clear provisional 3:1 on the dark wall and dark ink will clear 4.5:1 on the pale table; all text stays outside object areas.",
        "result": "Rendered three 1080×1350 finals with exact brief wording, no tracking or effects.",
        "before_feed": str(ROUND_DIR / "R0-initial-feed-AB2.png"),
        "after_feed": str(feed),
        "correction_rounds_used": 0,
    }, ensure_ascii=False, indent=2) + "\n")
    print(feed)


if __name__ == "__main__":
    main()
