#!/usr/bin/env python3
"""Compose the skill condition (B) over generated photo bases and build A/B feed sheet.

Inputs: A/slide-1.png..slide-3.png (complete direct generations),
        B/base-1.png..base-3.png (text-free generated image bases).
Optional object-over-type masks: B/occlusion_masks.json. Each polygon is a list
of normalized [x,y] points. The renderer copies only source-image pixels inside
the polygon back over the type; inspect and tune masks against each actual image.
No vector object illustration is added.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[4] / "skills" / "cropmark" / "engines" / "pillow"))
import cm  # noqa: E402

W, H = 1080, 1350
FEED_W, FEED_H = 360, 450
LEFT, RIGHT = 112, 968
HEAD_Y, HEAD_SIZE, LEADING = 350, 92, 1.06
COPY = [
    {"headline":"La forma\ntoma cuerpo.", "headline_y":210, "support":"Una pieza empieza con un gesto.", "cta":"EXPLORA EL TALLER"},
    {"headline":"Del giro\nnace el borde.", "headline_y":390, "support":"El torno acompaña cada movimiento.", "cta":"SIGUE EL PROCESO"},
    {"headline":"Cada huella\ndeja memoria.", "headline_y":350, "support":"Un rastro queda en la superficie.", "cta":"MIRA LAS PIEZAS"},
]
MASKS_PATH = ROOT / "B" / "occlusion_masks.json"


def fitted(path: Path) -> Image.Image:
    return ImageOps.fit(Image.open(path).convert("RGB"), (W, H), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def get_masks(slide: int):
    if not MASKS_PATH.exists():
        return []
    data = json.loads(MASKS_PATH.read_text(encoding="utf-8"))
    return data.get(str(slide), [])


def make_occlusion_mask(size, spec):
    mask = Image.new("L", size, 0)
    points = [(round(float(x) * W), round(float(y) * H)) for x, y in spec["polygon"]]
    ImageDraw.Draw(mask).polygon(points, fill=255)
    return mask


def compose_b(source_path: Path, slide: int, spec: dict) -> tuple[Image.Image, dict]:
    source = fitted(source_path)
    im = source.copy()
    cm.reset()
    # Dark, quiet background was requested; retain a soft shadow for actual photo variation.
    title_font = cm.font("DMSerifDisplay-Regular", HEAD_SIZE)
    label_font = cm.font("Outfit-Bold", 30)
    body_font = cm.font("Outfit-Regular", 35)
    cta_font = cm.font("Outfit-Bold", 30)
    ink = (250, 244, 231)
    dark_ink = (29, 38, 36)
    headline_y = spec.get("headline_y", HEAD_Y)

    cm.text(im, (LEFT, 104), "TALLER BARRO", label_font, ink, stroke=2,
            stroke_fill=dark_ink, role="brand")
    cm.text(im, (LEFT, 148), "CERÁMICA", label_font, ink, stroke=2,
            stroke_fill=dark_ink, role="descriptor")
    headline_box = cm.text(im, (LEFT, headline_y), spec["headline"], title_font, ink,
                           leading=LEADING, shadow=(0, 4, 10, .65), role="headline")
    cm.text(im, (LEFT, 987), spec["support"], body_font, dark_ink,
            shadow=(0, 3, 8, .55), role="support")
    cm.text(im, (LEFT, 1178), spec["cta"], cta_font, dark_ink, tracking=.035,
            shadow=(0, 3, 8, .55), role="cta")

    # Put selected pixels from the same generated photograph above type. Configure masks
    # only after looking at the image; no guessed universal mask is applied by default.
    total_ink, covered_ink = 0, 0
    if MASKS_PATH.exists():
        union = Image.new("L", (W, H), 0)
        for obj in get_masks(slide):
            mask = make_occlusion_mask((W, H), obj)
            union = ImageChops.lighter(union, mask)
        # Pixel-measure the union against the headline's actual glyphs once.
        glyphs = Image.new("L", (W, H), 0)
        gd = ImageDraw.Draw(glyphs)
        for line_i, line in enumerate(spec["headline"].split("\n")):
            gd.text((LEFT, headline_y + line_i * title_font.size * LEADING), line, font=title_font, fill=255, anchor="la")
        total_ink = sum(1 for p in glyphs.getdata() if p > 0)
        covered_ink = sum(1 for a, b in zip(glyphs.getdata(), union.getdata()) if a > 0 and b > 0)
        im.paste(source, (0, 0), union)
    fraction = (covered_ink / total_ink) if total_ink else 0.0
    # The fraction is written for review; keep it small and inspect the full phrase at 360px.
    if fraction > 0.12:
        print(f"WARNING: slide {slide} covers {fraction:.1%} of headline ink; reduce the mask.", file=sys.stderr)
    out = ROOT / "B" / f"slide-{slide}.png"
    cm.save(im, str(out), boxes_dir=str(ROOT / "B" / "boxes"))
    return im, {"slide": slide, "headline": spec["headline"].replace("\n", " / "),
                "occluded_ink_fraction": round(fraction, 4),
                "mask_count": len(get_masks(slide)), "source": source_path.name,
                "output": out.name, "headline_box": [int(v) for v in headline_box]}


def main():
    finals_a, finals_b, log = [], [], []
    for slide, spec in enumerate(COPY, start=1):
        a_src = ROOT / "A" / f"slide-{slide}.png"
        b_src = ROOT / "B" / f"base-{slide}.png"
        if not a_src.exists() or not b_src.exists():
            raise SystemExit(f"Missing input: {a_src if not a_src.exists() else b_src}")
        a = fitted(a_src)
        a_out = ROOT / "A" / f"final-{slide}.png"
        a.save(a_out)
        finals_a.append(a)
        b, entry = compose_b(b_src, slide, spec)
        finals_b.append(b)
        log.append(entry)

    gap, label_h = 16, 28
    sheet = Image.new("RGB", (3 * FEED_W + 4 * gap, 2 * (FEED_H + label_h) + 3 * gap), (238, 234, 224))
    d = ImageDraw.Draw(sheet)
    for row, (label, images) in enumerate((("A · directo", finals_a), ("B · Cropmark", finals_b))):
        y = gap + row * (FEED_H + label_h + gap)
        d.text((gap, y), label, fill=(28, 35, 33))
        y += label_h
        for col, im in enumerate(images):
            thumb = im.resize((FEED_W, FEED_H), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (gap + col * (FEED_W + gap), y))
    sheet.save(ROOT / "AB-feed.png")
    (ROOT / "B" / "occlusion-log.json").write_text(json.dumps(log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {ROOT / 'AB-feed.png'}")

if __name__ == "__main__":
    main()
