#!/usr/bin/env python3
"""Measure carousel typography from Cropmark boxes metadata or annotated PNG regions.

Metadata mode uses each recorded text box and its font file. PNG mode requires a
small region map because pixels alone cannot identify text groups or logos. See
--help for the JSON region-map format and limitations.
"""
import argparse
import json
import re
import statistics
from collections import Counter
from pathlib import Path

from PIL import Image, ImageColor, ImageFont

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FONTS = ROOT / "skills/cropmark/fonts"


def rect(box):
    """Return an xyxy rectangle from renderer metadata."""
    if not isinstance(box, (list, tuple)) or len(box) != 4:
        raise ValueError(f"expected four rectangle numbers, got {box!r}")
    x, y, a, b = (float(v) for v in box)
    return [x, y, a, b]


def union(boxes):
    boxes = [b for b in boxes if b]
    if not boxes:
        return None
    return [min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes)]


def px_box(b):
    return [round(v, 2) for v in b] if b else None


def pct_box(b, size):
    if not b:
        return None
    w, h = size
    return [round(100 * b[0] / w, 3), round(100 * b[1] / h, 3),
            round(100 * (b[2] - b[0]) / w, 3), round(100 * (b[3] - b[1]) / h, 3)]


def font_metrics(path, family, size, fonts_dir):
    candidates = []
    if path:
        candidates.append(Path(path).expanduser())
        candidates.append(Path.cwd() / path)
    if family:
        stem = re.sub(r"^[\"']|[\"']$", "", family.split(",")[0].strip())
        candidates.extend([fonts_dir / f"{stem}.ttf", fonts_dir / f"{stem}.otf"])
    for candidate in candidates:
        try:
            font = ImageFont.truetype(str(candidate), max(1, round(float(size))))
            cap = font.getbbox("H")[3] - font.getbbox("H")[1]
            xheight = font.getbbox("x")[3] - font.getbbox("x")[1]
            return round(cap, 2), round(xheight, 2)
        except (OSError, TypeError, ValueError):
            continue
    return None, None


def line_metrics_from_font(text, box, font_path, family, size, stroke, fonts_dir):
    lines = text.splitlines()
    if len(lines) < 2:
        return None, []
    candidates = [Path(font_path)] if font_path else []
    if family:
        stem = re.sub(r"^[\"']|[\"']$", "", family.split(",")[0].strip())
        candidates += [fonts_dir / f"{stem}.ttf", fonts_dir / f"{stem}.otf"]
    font = None
    for candidate in candidates:
        try:
            font = ImageFont.truetype(str(candidate), max(1, round(float(size))))
            break
        except (OSError, TypeError, ValueError):
            pass
    if font is None:
        return None, None
    bounds = [font.getbbox(line or " ", stroke_width=max(0, round(float(stroke)))) for line in lines]
    line_union_h = max(b[3] for b in bounds) - min(b[1] for b in bounds)
    advance = ((box[3] - box[1]) - line_union_h) / (len(lines) - 1)
    gaps = [round(advance + bounds[i + 1][1] - bounds[i][3], 2)
            for i in range(len(bounds) - 1)]
    return round(advance, 2), gaps


def line_metrics_from_boxes(boxes):
    """Cluster same-line fragments, then report ink gap and top-to-top pitch."""
    clusters = []
    for box in sorted(boxes, key=lambda b: (b[1], b[0])):
        match = next((line for line in clusters
                      if min(line[3], box[3]) > max(line[1], box[1])), None)
        if match is None:
            clusters.append(box[:])
        else:
            match[:] = union([match, box])
    clusters.sort(key=lambda b: (b[1], b[0]))
    gaps = [round(next_[1] - prev[3], 2) for prev, next_ in zip(clusters, clusters[1:])]
    pitches = [round(next_[1] - prev[1], 2) for prev, next_ in zip(clusters, clusters[1:])]
    return pitches, gaps, clusters


def margins(box, size):
    if not box:
        return None
    w, h = size
    return {"left_px": round(box[0], 2), "top_px": round(box[1], 2),
            "right_px": round(w - box[2], 2), "bottom_px": round(h - box[3], 2),
            "left_pct": round(100 * box[0] / w, 3), "top_pct": round(100 * box[1] / h, 3),
            "right_pct": round(100 * (w - box[2]) / w, 3),
            "bottom_pct": round(100 * (h - box[3]) / h, 3)}


def neighboring_gaps(groups):
    """Report gaps between neighboring boxes in top-to-bottom, left-to-right order."""
    ordered = sorted((g for g in groups if g.get("box_px")),
                     key=lambda g: (g["box_px"][1], g["box_px"][0]))
    out = []
    for first, second in zip(ordered, ordered[1:]):
        a, b = first["box_px"], second["box_px"]
        y_overlap = min(a[3], b[3]) - max(a[1], b[1])
        x_overlap = min(a[2], b[2]) - max(a[0], b[0])
        if y_overlap > 0:
            gap = b[0] - a[2] if b[0] >= a[0] else a[0] - b[2]
            axis = "horizontal"
        else:
            gap = b[1] - a[3]
            axis = "vertical"
        out.append({"from": first["name"], "to": second["name"], "axis": axis,
                    "gap_px": round(gap, 2), "overlap_on_other_axis_px": round(max(0, y_overlap if axis == "horizontal" else x_overlap), 2)})
    return out


def from_metadata(path, data, fonts_dir):
    size = tuple(data.get("size", (0, 0)))
    boxes = data.get("boxes", [])
    by_role, logos = {}, []
    for item in boxes:
        b = rect(item["box"])
        role = str(item.get("role", "text"))
        if re.search(r"logo|brand|signature", role, re.I):
            logos.append(b)
        if not item.get("text"):
            continue
        cap, xh = font_metrics(item.get("font_path"), item.get("fontFamily"),
                               item.get("size"), fonts_dir)
        pitch, gaps = line_metrics_from_font(str(item["text"]), b, item.get("font_path"),
                                             item.get("fontFamily"), item.get("size", 0),
                                             item.get("stroke_width", item.get("strokeWidth", 0)), fonts_dir)
        rec = by_role.setdefault(role, {"name": role, "boxes": [], "caps": [], "xheights": [],
                                        "pitches": [], "gaps": [], "colors": [], "multiline": []})
        rec["boxes"].append(b)
        if cap is not None: rec["caps"].append(cap)
        if xh is not None: rec["xheights"].append(xh)
        if item.get("fill") and isinstance(item["fill"], (list, tuple)):
            rec["colors"].append(list(item["fill"][:3]))
        if len(str(item["text"]).splitlines()) > 1:
            rec["multiline"].append((pitch, gaps))
    groups = []
    for rec in by_role.values():
        b = union(rec["boxes"])
        pitches, gaps, lines = line_metrics_from_boxes(rec["boxes"])
        if not pitches and rec["multiline"]:
            pitches, gaps = rec["multiline"][0]
        groups.append({"name": rec["name"], "box": b,
                       "cap_height_px": round(statistics.median(rec["caps"]), 2) if rec["caps"] else None,
                       "x_height_px": round(statistics.median(rec["xheights"]), 2) if rec["xheights"] else None,
                       "line_pitch_px": pitches, "line_gap_px": gaps,
                       "line_boxes_px": [px_box(line) for line in lines],
                       "ink_rgb": Counter(map(tuple, rec["colors"])).most_common(1)[0][0] if rec["colors"] else None})
    content_boxes = [g["box"] for g in groups if not re.search(r"logo|brand|signature|background", g["name"], re.I)]
    all_text = union(content_boxes)
    for g in groups:
        g["box_px"] = px_box(g.pop("box"))
        g["box_pct"] = pct_box(g["box_px"], size)
    headline = next((g for g in groups if g["name"].lower() == "headline"), None)
    rule = next((g for g in groups if g["name"].lower() == "rule"), None)
    return {
        "slide": path.name, "frame_px": list(size), "source": "renderer .boxes.json",
        "text_block_px": px_box(all_text), "text_block_pct_xywh": pct_box(all_text, size),
        "margins": margins(all_text, size), "groups": groups,
        "inter_group_gaps": neighboring_gaps(groups),
        "logo_bbox_px": px_box(union(logos)), "logo_bbox_pct_xywh": pct_box(union(logos), size),
        "rule_to_headline_width_pct": round(100 * (rule["box_px"][2] - rule["box_px"][0]) /
                                               (headline["box_px"][2] - headline["box_px"][0]), 2)
                                      if rule and headline and headline["box_px"][2] > headline["box_px"][0] else None,
        "measurement_note": "Recorded boxes are renderer bounds, not guaranteed exact raster ink bounds. Cap/x-height use the resolved font file at metadata size."
    }


def parse_color(value):
    if isinstance(value, str):
        return ImageColor.getrgb(value)[:3]
    if isinstance(value, (tuple, list)) and len(value) >= 3:
        return tuple(int(v) for v in value[:3])
    return None


def ink_bbox(image, region, threshold, with_color=False):
    spec = {"box": region} if isinstance(region, (list, tuple)) else region
    x, y, w, h = (int(round(v)) for v in spec["box"])
    x0, y0, x1, y1 = max(0, x), max(0, y), min(image.width, x + w), min(image.height, y + h)
    rgb = image.convert("RGBA")
    if x0 >= x1 or y0 >= y1:
        return (None, None) if with_color else None
    bg = parse_color(spec.get("background"))
    if bg is None:
        edge = []
        for xx in range(x0, x1):
            edge.extend([rgb.getpixel((xx, y0))[:3], rgb.getpixel((xx, y1 - 1))[:3]])
        for yy in range(y0 + 1, y1 - 1):
            edge.extend([rgb.getpixel((x0, yy))[:3], rgb.getpixel((x1 - 1, yy))[:3]])
        bg = tuple(round(statistics.median(px[c] for px in edge)) for c in range(3)) if edge else (255, 255, 255)
    ink = []
    colors = Counter()
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            r, g, b, a = rgb.getpixel((xx, yy))
            if a > 8 and max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2])) >= threshold:
                ink.append((xx, yy))
                colors[(r, g, b)] += 1
    if not ink:
        return (None, None) if with_color else None
    box = [min(p[0] for p in ink), min(p[1] for p in ink),
           max(p[0] for p in ink) + 1, max(p[1] for p in ink) + 1]
    color = colors.most_common(1)[0][0]
    return (box, color) if with_color else box


def from_png(path, regions, threshold, fonts_dir):
    image = Image.open(path).convert("RGBA")
    size = tuple(regions.get("frame", image.size))
    groups, logos = [], []
    for item in regions.get("groups", []):
        measured_lines = [ink_bbox(image, line, threshold, with_color=True) for line in item.get("lines", [])]
        lines = [box for box, color in measured_lines if box]
        line_colors = [color for box, color in measured_lines if box and color]
        single = ink_bbox(image, item["box"], threshold, with_color=True) if item.get("box") else (None, None)
        b = union(lines) if lines else single[0]
        color = Counter(line_colors).most_common(1)[0][0] if line_colors else single[1]
        cap, xh = font_metrics(item.get("font"), None, item.get("font_size"), fonts_dir)
        gaps = [round(lines[i + 1][1] - lines[i][3], 2) for i in range(len(lines) - 1)] if lines else None
        pitches = [round(lines[i + 1][1] - lines[i][1], 2) for i in range(len(lines) - 1)] if lines else None
        baseline_boxes = [ink_bbox(image, region, threshold) for region in item.get("baselines", [])]
        baseline_boxes = [box for box in baseline_boxes if box]
        baseline_y = [box[3] for box in baseline_boxes]
        if len(baseline_y) >= 2:
            pitches = [round(baseline_y[i + 1] - baseline_y[i], 2) for i in range(len(baseline_y) - 1)]
        groups.append({"name": item["name"], "box": b, "cap_height_px": cap,
                       "x_height_px": xh, "line_pitch_px": pitches,
                       "line_gap_px": gaps, "line_boxes_px": [px_box(line) for line in lines],
                       "baseline_y_px": baseline_y if baseline_y else None,
                       "ink_rgb": color,
                       "include_in_block": item.get("include_in_block", True)})
    if regions.get("logo"):
        logo, logo_color = ink_bbox(image, regions["logo"], threshold, with_color=True)
        if logo:
            logos.append(logo)
    else:
        logo_color = None
    content_boxes = [g["box"] for g in groups if g.get("include_in_block", True)
                     and not re.search(r"logo|brand|signature|background", g["name"], re.I)]
    all_text = union(content_boxes)
    for g in groups:
        g["box_px"] = px_box(g.pop("box"))
        g["box_pct"] = pct_box(g["box_px"], size)
        g.pop("include_in_block", None)
    cap_region = ink_bbox(image, regions["cap_height"], threshold) if regions.get("cap_height") else None
    x_region = ink_bbox(image, regions["x_height"], threshold) if regions.get("x_height") else None
    word = next((g for g in groups if re.search(r"background", g["name"], re.I)), None)
    alpha = None
    if word and word.get("ink_rgb") and regions.get("canvas_background"):
        bg = parse_color(regions["canvas_background"])
        fg = word["ink_rgb"]
        denom = sum((255 - c) ** 2 for c in bg)
        alpha = round(100 * sum((f - b) * (255 - b) for f, b in zip(fg, bg)) / denom, 2) if denom else None
    return {
        "slide": path.name, "frame_px": list(size), "source": "PNG ink segmentation in annotated regions",
        "text_block_px": px_box(all_text), "text_block_pct_xywh": pct_box(all_text, size),
        "margins": margins(all_text, size), "groups": groups,
        "inter_group_gaps": neighboring_gaps([g for g in groups if not re.search(r"background", g["name"], re.I)]),
        "logo_bbox_px": px_box(union(logos)), "logo_bbox_pct_xywh": pct_box(union(logos), size),
        "logo_ink_rgb": logo_color,
        "rule_to_headline_width_pct": _rule_ratio(groups),
        "cap_sample_px": (cap_region[3] - cap_region[1]) if cap_region else None,
        "x_height_sample_px": (x_region[3] - x_region[1]) if x_region else None,
        "background_word_apparent_opacity_over_white_pct": alpha,
        "measurement_note": f"PNG ink masks use max-channel RGB distance >= {threshold} from explicit or ROI-edge median background; annotate each text line tightly."
    }


def _rule_ratio(groups):
    headline = next((g for g in groups if g["name"].lower() == "headline"), None)
    rule = next((g for g in groups if g["name"].lower() == "rule"), None)
    if not headline or not rule or not headline.get("box_px"):
        return None
    width = headline["box_px"][2] - headline["box_px"][0]
    return round(100 * (rule["box_px"][2] - rule["box_px"][0]) / width, 2) if width else None


def main():
    parser = argparse.ArgumentParser(description=__doc__, epilog="""PNG region JSON example:
  {"frame":[1080,1350],"groups":[{"name":"title","lines":[{"box":[100,100,800,120],"background":"#ffffff"},{"box":[100,230,800,120],"background":"#ffffff"}],"font":"Anton-Regular.ttf","font_size":84}],"logo":{"box":[80,1260,150,40],"background":"#ffffff"},"cap_height":{"box":[101,101,38,70],"background":"#ffffff"},"x_height":{"box":[147,101,30,55],"background":"#ffffff"}}
Each region box is [x,y,width,height]. For photo/paper backgrounds set a per-region
background colour or use tightly cropped uniform-background ROIs. Cap/x PNG samples
must isolate one uppercase/lowercase glyph. Inter-group gaps compare consecutive
groups in reading order. Metadata gaps are estimates for text boxes, not ink masks.""")
    parser.add_argument("inputs", nargs="+", type=Path, help="PNG or corresponding .boxes.json files")
    parser.add_argument("--regions", type=Path, help="PNG ROI annotation JSON (single slide or slides keyed by filename)")
    parser.add_argument("--ink", action="store_true", help="force pixel ink measurement even when boxes metadata exists")
    parser.add_argument("--threshold", type=int, default=48, help="RGB distance threshold for PNG ink segmentation")
    parser.add_argument("--fonts-dir", type=Path, default=DEFAULT_FONTS)
    args = parser.parse_args()
    outputs = []
    region_data = json.loads(args.regions.read_text()) if args.regions else None
    for source in args.inputs:
        if source.name.endswith(".boxes.json"):
            meta_path = source
            image_path = Path(str(source)[:-len(".boxes.json")])
        else:
            image_path = source
            meta_path = Path(str(source) + ".boxes.json")
        if meta_path.is_file() and not args.ink:
            outputs.append(from_metadata(image_path, json.loads(meta_path.read_text()), args.fonts_dir))
        elif region_data:
            per_slide = region_data.get("slides", {}).get(source.name, region_data)
            outputs.append(from_png(source, per_slide, args.threshold, args.fonts_dir))
        else:
            parser.error(f"no metadata for {source}; supply --regions for PNG ink measurement")
    print(json.dumps({"slides": outputs}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
