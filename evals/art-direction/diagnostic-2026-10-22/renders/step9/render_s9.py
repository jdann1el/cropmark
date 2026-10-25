#!/usr/bin/env python3
"""Reproducible Paso 9 compositing with editable Cropmark text layers.

Run from anywhere with the repository's Pillow dependency installed:
    python render_s9.py
All generated bases remain untouched. B overlays are controlled by this file.
"""
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

FONT_DIR = REPO / "skills/cropmark/fonts"
LIGHT = (247, 243, 232)
DARK = (38, 34, 29)
TARGET_SMALL = 4.5
TARGET_LARGE = 3.0


def lin(v: int) -> float:
    v = v / 255
    return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4


def lum(rgb) -> float:
    return .2126 * lin(rgb[0]) + .7152 * lin(rgb[1]) + .0722 * lin(rgb[2])


def ratio(a, b) -> float:
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + .05) / (lo + .05)


def pct(values, p):
    values = sorted(values)
    return values[max(0, math.floor((len(values) - 1) * p))]


def fit(src: Path, size):
    return ImageOps.fit(Image.open(src).convert("RGB"), size,
                        method=Image.Resampling.LANCZOS, centering=(.5, .5))


def font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def group_mask(size, text, xy, f, leading=1.08):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    x, y = xy
    for i, line in enumerate(text.split("\n")):
        d.text((x, y + i * f.size * leading), line, font=f, fill=255)
    return mask.point(lambda p: 255 if p >= 250 else 0)


def metrics(base, mask, ink, threshold):
    pixels = [rgb for rgb, a in zip(base.convert("RGB").getdata(), mask.getdata()) if a >= 250]
    if not pixels:
        raise ValueError("empty glyph core")
    lums = [lum(p) for p in pixels]
    ratios = [ratio(ink, p) for p in pixels]
    return {
        "glyph_core_pixels": len(pixels),
        "background_srgb_linear_luminance_p05": round(pct(lums, .05), 5),
        "background_srgb_linear_luminance_median": round(pct(lums, .50), 5),
        "contrast_p05": round(pct(ratios, .05), 3),
        "contrast_median": round(pct(ratios, .50), 3),
        "under_target_percent": round(100 * sum(r < threshold for r in ratios) / len(ratios), 3),
        "target": threshold,
    }


def choose(base, text, xy, f, leading, threshold, preferred=None):
    mask = group_mask(base.size, text, xy, f, leading)
    candidates = {"light": metrics(base, mask, LIGHT, threshold),
                  "dark": metrics(base, mask, DARK, threshold)}
    if preferred:
        name = preferred
    else:
        name = max(candidates, key=lambda k: candidates[k]["contrast_p05"])
    return (LIGHT if name == "light" else DARK), candidates[name], candidates, mask


def visible_cap(f):
    box = f.getbbox("H")
    return box[3] - box[1]


def render_group(im, role, text, xy, font_name, size, leading=1.08,
                 threshold=TARGET_SMALL, underline=False, preferred=None):
    f = font(font_name, size)
    ink, selected_metrics, candidates, mask = choose(im, text, xy, f, leading,
                                                      threshold, preferred)
    cm.text(im, xy, text, f, ink, leading=leading, role=role)
    if underline:
        box = mask.getbbox()
        if box:
            y = box[3] + 8
            ImageDraw.Draw(im).line((box[0], y, box[2], y), fill=ink, width=3)
    return {
        "role": role, "text": text.replace("\n", " "), "editable_text": text,
        "position": list(xy), "font_file": font_name, "font_size": size,
        "visible_cap_height_px_master": visible_cap(f),
        "visible_cap_height_px_at_360": round(visible_cap(f) * 360 / 1080, 2),
        "ink_srgb": list(ink), "contrast": selected_metrics,
        "candidate_contrast": candidates,
        "effects": {"shadow": False, "stroke": False, "text_panel": False},
        "underline": underline,
    }


def crop_sidecar(src, size):
    im = Image.open(src)
    target_ratio = size[0] / size[1]
    source_ratio = im.width / im.height
    if source_ratio > target_ratio:
        cw = round(im.height * target_ratio)
        x0 = (im.width - cw) // 2
        box = [x0, 0, x0 + cw, im.height]
    else:
        ch = round(im.width / target_ratio)
        y0 = (im.height - ch) // 2
        box = [0, y0, im.width, y0 + ch]
    return {"source": str(src.relative_to(ROOT)), "source_size": list(im.size),
            "crop_box": box, "output_size": list(size),
            "operation": "center crop to target aspect ratio then Lanczos resize"}


def save_a(src, out, size, context):
    im = fit(src, size)
    im.save(out)
    (Path(str(out) + ".sidecar.json")).write_text(json.dumps({
        "condition": "A direct imagegen raster final; content not retouched",
        "copy_editability": "embedded raster lettering; original font unknown",
        "context": context, **crop_sidecar(src, size),
        "source_sha256": sha(src), "output_sha256": sha(out),
    }, ensure_ascii=False, indent=2) + "\n")


def sha(path):
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def svg_overlay(name, size, groups):
    # SVG text remains an editable duplicate of the canonical Python overlay.
    # PNG typography comes from Cropmark/Pillow; the bundled fonts are named explicitly.
    chunks = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{size[0]}" height="{size[1]}" viewBox="0 0 {size[0]} {size[1]}">']
    for g in groups:
        x, y = g["position"]
        family = g["font_file"].replace(".ttf", "")
        chunks.append(f'<g id="{g["role"]}" aria-label="{g["text"]}" fill="rgb({g["ink_srgb"][0]},{g["ink_srgb"][1]},{g["ink_srgb"][2]})" font-family="{family}" font-size="{g["font_size"]}">')
        for i, line in enumerate(g["editable_text"].split("\n")):
            chunks.append(f'<text x="{x}" y="{y + i * g["font_size"] * 1.08:.2f}">{line.replace("&", "&amp;").replace("<", "&lt;")}</text>')
        if g.get("underline"):
            chunks.append(f'<line x1="{x}" y1="{y + g["font_size"] + 8}" x2="{x + 400}" y2="{y + g["font_size"] + 8}" stroke="rgb({g["ink_srgb"][0]},{g["ink_srgb"][1]},{g["ink_srgb"][2]})" stroke-width="3"/>')
        chunks.append("</g>")
    chunks.append("</svg>")
    (ROOT / name).write_text("\n".join(chunks) + "\n")


def render_b3():
    outdir = ROOT / "B3"
    configs = [
        {
            "positions": {"brand": ((70, 60), 60), "descriptor": ((70, 128), 60),
                          "headline": ((70, 260), 132), "support": ((70, 1010), 58),
                          "cta": ((70, 1216), 58)}, "headline_relation": "rim echo above vessel; type is a broad rising silhouette across the quiet wall",
            "headline": "La forma\ntoma cuerpo.", "support": "Una pieza empieza\ncon un gesto.", "cta": "EXPLORA EL TALLER",
        },
        {
            "positions": {"brand": ((70, 60), 60), "descriptor": ((70, 128), 60),
                          "headline": ((70, 425), 116), "support": ((70, 225), 58),
                          "cta": ((70, 1210), 58)}, "headline_relation": "wheel arc answers a compact lower-left headline; headline scale and position shift from cover",
            "headline": "Del giro\nnace el borde.", "support": "El torno acompaña\ncada movimiento.", "cta": "SIGUE EL PROCESO",
        },
        {
            "positions": {"brand": ((70, 80), 60), "descriptor": ((70, 148), 60),
                          "headline": ((70, 575), 124), "support": ((70, 235), 58),
                          "cta": ((70, 1195), 58)}, "headline_relation": "headline sits beside the thumbprint trace as a material echo; mid-left placement differs from slides 1 and 2",
            "headline": "Cada huella\ndeja memoria.", "support": "Un rastro queda en\nla superficie.", "cta": "MIRA LAS PIEZAS",
        },
    ]
    reports = []
    for i, c in enumerate(configs, 1):
        cm.reset()
        base_path = outdir / f"base-{i}.png"
        base = fit(base_path, (1080, 1350))
        im = base.copy()
        groups = []
        for role, text in (("brand", "TALLER BARRO"), ("descriptor", "CERÁMICA"),
                           ("headline", c["headline"]), ("support", c["support"]), ("cta", c["cta"])):
            pos, size = c["positions"][role]
            if role == "headline":
                fam, threshold, lead = "InstrumentSerif-Regular.ttf", TARGET_LARGE, 1.02
            elif role in ("brand", "descriptor", "cta"):
                fam, threshold, lead = "InstrumentSans-Bold.ttf", TARGET_SMALL, 1.05
            else:
                fam, threshold, lead = "InstrumentSans-Regular.ttf", TARGET_SMALL, 1.12
            # White ink stays on the broad, sunlit clay/wall field; choose by actual crop metrics.
            g = render_group(im, role, text, pos, fam, size, lead, threshold,
                             underline=(i == 3 and role == "cta"))
            groups.append(g)
        out = outdir / f"final-{i}.png"
        cm.save(im, str(out))
        # The last Cropmark sidecar is a fresh record per final and contains exact group boxes.
        boxes = json.loads(Path(str(out) + ".boxes.json").read_text())
        boxes.update({"text_free": False, "condition": "B3 Cropmark editable overlay",
                      "source_base": f"base-{i}.png", "crop": crop_sidecar(base_path, (1080, 1350)),
                      "headline_image_relation": c["headline_relation"], "groups": groups})
        Path(str(out) + ".boxes.json").write_text(json.dumps(boxes, ensure_ascii=False, indent=2) + "\n")
        svg_overlay(f"B3/final-{i}.svg", (1080, 1350), groups)
        reports.append({"slide": i, "final": f"B3/final-{i}.png", "groups": groups,
                        "headline_image_relation": c["headline_relation"],
                        "base_sha256": sha(base_path), "final_sha256": sha(out)})
    return reports


def render_single(src, output, size, context, overlay=None):
    base = fit(src, size)
    im = base.copy()
    groups = []
    cm.reset()
    for item in overlay or []:
        role, text, xy, font_name, fs, leading, threshold, underline, preferred = item
        f = font(font_name, fs)
        ink, m, candidates, _ = choose(base, text, xy, f, leading, threshold, preferred)
        mask = group_mask(base.size, text, xy, f, leading)
        cm.text(im, xy, text, f, ink, leading=leading, role=role)
        if underline:
            box = mask.getbbox()
            if box:
                y = box[3] + 8
                ImageDraw.Draw(im).line((box[0], y, box[2], y), fill=ink, width=3)
        groups.append({
            "role": role, "text": text.replace("\n", " "), "editable_text": text,
            "position": list(xy), "font_file": font_name, "font_size": fs,
            "visible_cap_height_px_master": visible_cap(f),
            "visible_cap_height_px_at_360": round(visible_cap(f) * 360 / 1080, 2),
            "ink_srgb": list(ink), "contrast": m, "candidate_contrast": candidates,
            "effects": {"shadow": False, "stroke": False, "text_panel": False},
            "underline": underline,
        })
    out = ROOT / output
    cm.save(im, str(out))
    side = {"condition": "B Cropmark editable overlay", "context": context,
            "source_base": str(src.relative_to(ROOT)), "crop": crop_sidecar(src, size),
            "groups": groups, "output_sha256": sha(out)}
    Path(str(out) + ".sidecar.json").write_text(json.dumps(side, ensure_ascii=False, indent=2) + "\n")
    svg_overlay(output.replace(".png", ".svg"), size, groups)
    return side


def render_singles():
    thumb = ROOT / "thumbnail"
    flyer = ROOT / "flyer"
    save_a(thumb / "A-source.png", thumb / "A.png", (1280, 720), "3 AIs. 1 Portfolio.")
    save_a(flyer / "A-source.png", flyer / "A.png", (1080, 1350), "Noche de vinilos · Sala Taller · 14 nov · 21:00")
    # Cropmark's strict CLI metadata cannot edit A's embedded lettering. These
    # estimated copy regions are provenance only; font_effective states that the
    # source font is unknown and all strings remain raster content.
    (thumb / "A.png.boxes.json").write_text(json.dumps({
        "size": [1280, 720], "text_free": False,
        "condition": "A direct imagegen raster; embedded lettering, unknown font; approximate copy region",
        "boxes": [{"role": "raster_copy", "text": "3 AIs. 1 Portfolio.", "box": [54, 504, 1010, 642],
                   "size": 126, "font_effective": "embedded raster lettering; font unknown",
                   "fill": [247, 243, 232]}]}, ensure_ascii=False, indent=2) + "\n")
    (flyer / "A.png.boxes.json").write_text(json.dumps({
        "size": [1080, 1350], "text_free": False,
        "condition": "A direct imagegen raster; embedded lettering, unknown font; approximate copy regions",
        "boxes": [
            {"role": "raster_copy", "text": "Noche de vinilos", "box": [84, 304, 710, 436],
             "size": 103, "font_effective": "embedded raster lettering; font unknown", "fill": [27, 19, 14]},
            {"role": "raster_copy", "text": "Sala Taller · 14 nov · 21:00", "box": [121, 439, 710, 509],
             "size": 45, "font_effective": "embedded raster lettering; font unknown", "fill": [27, 19, 14]},
        ]}, ensure_ascii=False, indent=2) + "\n")
    render_single(thumb / "B-base-source.png", "thumbnail/B.png", (1280, 720),
                  "3 AIs. 1 Portfolio.", [
                      ("headline", "3 AIs. 1 Portfolio.", (66, 553), "BricolageGrotesque-Bold.ttf", 92, 1.0, TARGET_LARGE, False, None)
                  ])
    render_single(flyer / "B-base-source.png", "flyer/B.png", (1080, 1350),
                  "Noche de vinilos · Sala Taller · 14 nov · 21:00", [
                      ("event", "Noche de vinilos", (84, 278), "InstrumentSerif-Regular.ttf", 76, 1.0, TARGET_LARGE, False, "dark"),
                      ("venue_date", "Sala Taller · 14 nov\n· 21:00", (86, 438), "InstrumentSans-Bold.ttf", 56, 1.12, TARGET_SMALL, False, "dark"),
                  ])


def main():
    b3 = render_b3()
    render_singles()
    (ROOT / "rounds/R0").mkdir(parents=True, exist_ok=True)
    report = {
        "round": "R0", "correction_rounds_used": 0,
        "method": "Source bases center-cropped/resized to master dimensions; Cropmark/Pillow text groups; no shadow, stroke, or added panel.",
        "B3": b3,
        "font_license": "Bundled fonts are from skills/cropmark/fonts; licenses listed in fonts/OFL-LICENSES.txt.",
        "comparatives": "Not generated by T3; T3b owns contact sheets and previews.",
    }
    (ROOT / "rounds/R0/render-log.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"B3": [x["final"] for x in b3], "singles": ["thumbnail/A.png", "thumbnail/B.png", "flyer/A.png", "flyer/B.png"]}, indent=2))


if __name__ == "__main__":
    main()
