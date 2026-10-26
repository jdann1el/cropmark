#!/usr/bin/env python3
"""Composite Paso 10 flyer C2 onto the measured sleeve plane."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[5]
S9 = REPO / "evals/art-direction/diagnostic-2026-10-22/renders/step9"
SOURCE = S9 / "flyer/B-base-source.png"
FONT_DIR = S9 / "fonts"
SIZE = (1080, 1350)
PLANE = (720, 680)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def draw_line(canvas: Image.Image, text: str, x: int, y: int, font: ImageFont.FreeTypeFont):
    d = ImageDraw.Draw(canvas)
    box = d.textbbox((0, 0), text, font=font)
    d.text((x - box[0], y - box[1]), text, font=font, fill=255)


def measure(mask: np.ndarray, H: np.ndarray) -> tuple[list[int], np.ndarray]:
    warped = cv2.warpPerspective(mask, H, SIZE, flags=cv2.INTER_CUBIC,
                                 borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    ys, xs = np.where(warped > 200)
    if not len(xs):
        raise RuntimeError("empty projected glyph mask")
    return [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1], warped


def make_text_masks():
    scale = 3
    canvas = Image.new("L", (PLANE[0] * scale, PLANE[1] * scale), 0)
    ink_groups: dict[str, list[Image.Image]] = {"headline": [], "metadata": []}
    title_font = ImageFont.truetype(str(FONT_DIR / "BricolageGrotesque-Bold.ttf"), 124 * scale)
    meta_font = ImageFont.truetype(str(FONT_DIR / "InstrumentSans-Regular.ttf"), 64 * scale)
    metadata_ratio = 1.0

    # The title is a two-line phrase. Keep every supplied separator attached
    # to following metadata and keep the whole metadata group on one line.
    entries = [
        ("headline", "Noche de", 60, 55, title_font),
        ("headline", "vinilos", 60, 181, title_font),
        ("metadata", "· Sala Taller · 14 nov · 21:00", 40, 460, meta_font),
    ]
    for role, text, x, y, f in entries:
        layer = Image.new("L", canvas.size, 0)
        draw_line(layer, text, (0 if role == "metadata" else x * scale), y * scale, f)
        if role == "metadata":
            glyph_box = layer.getbbox()
            glyphs = layer.crop(glyph_box)
            safe_width = (PLANE[0] - 2 * x) * scale
            metadata_ratio = min(1.0, safe_width / glyphs.width)
            glyphs = glyphs.resize((round(glyphs.width * metadata_ratio), glyphs.height), Image.Resampling.LANCZOS)
            fitted = Image.new("L", canvas.size, 0)
            fitted.paste(glyphs, (x * scale, glyph_box[1]))
            layer = fitted
        canvas = Image.composite(Image.new("L", canvas.size, 255), canvas, layer)
        ink_groups[role].append(layer)

    down = lambda m: np.array(m.resize(PLANE, Image.Resampling.LANCZOS), dtype=np.uint8)
    group_masks = {role: np.maximum.reduce([down(m) for m in layers]) for role, layers in ink_groups.items()}
    total = np.maximum.reduce(list(group_masks.values()))
    return total, group_masks, metadata_ratio


def main():
    image = ImageOps.fit(Image.open(SOURCE).convert("RGB"), SIZE,
                         method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    base = np.asarray(image).astype(np.float32)

    # The four corners come from intersections of long Canny/Hough edge fits
    # around the sleeve. Coordinates below are in the untouched source photo.
    # They were scaled with the same center-fit used for the rendered final.
    source_corners = np.array([
        [31.01, 144.36], [743.96, 128.16], [774.29, 787.36], [62.05, 840.07]
    ], dtype=np.float32)
    source_w, source_h = Image.open(SOURCE).size
    scale_x, scale_y = SIZE[0] / source_w, SIZE[1] / source_h
    dst = source_corners * np.array([scale_x, scale_y], dtype=np.float32)
    rect = np.array([[0, 0], [PLANE[0] - 1, 0],
                     [PLANE[0] - 1, PLANE[1] - 1], [0, PLANE[1] - 1]], dtype=np.float32)
    H = cv2.getPerspectiveTransform(rect, dst)
    inverse = cv2.getPerspectiveTransform(dst, rect)

    total_mask, masks, metadata_ratio = make_text_masks()
    projected = cv2.warpPerspective(total_mask, H, SIZE, flags=cv2.INTER_CUBIC,
                                    borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    masks_out = {role: cv2.warpPerspective(mask, H, SIZE, flags=cv2.INTER_CUBIC,
                                           borderMode=cv2.BORDER_CONSTANT, borderValue=0)
                 for role, mask in masks.items()}

    # Print uses substrate light and grain: the original sleeve pixel is locally
    # darkened under ink, with a small grain-linked modulation and no cast shadow.
    coverage = np.clip(projected.astype(np.float32) / 255.0, 0, 1)
    gray = np.mean(base, axis=2)
    local = np.clip((gray - 100.0) / 170.0, 0, 1)
    ink_rgb = base * np.array([0.255, 0.202, 0.184], dtype=np.float32)
    grain = (local - 0.72) * 0.08
    alpha = coverage * np.clip(0.82 + grain, 0.74, 0.88)
    out = base * (1.0 - alpha[:, :, None]) + ink_rgb * alpha[:, :, None]
    out = np.clip(out, 0, 255).astype(np.uint8)

    out_path = ROOT / "C.png"
    Image.fromarray(out, "RGB").save(out_path)
    Image.fromarray(out).resize((360, 450), Image.Resampling.LANCZOS).save(ROOT / "C-360.png")

    boxes = []
    for role, mask in masks_out.items():
        box, _ = measure(mask, np.eye(3, dtype=np.float32))
        rendered_size = 124 if role == "headline" else 64
        boxes.append({
            "role": role,
            "text": "Noche de vinilos" if role == "headline" else "· Sala Taller · 14 nov · 21:00",
            "box": box,
            "size": rendered_size,
            "font_effective": "BricolageGrotesque-Bold.ttf" if role == "headline" else "InstrumentSans-Regular.ttf",
            "fill": [59, 44, 36],
            "method": "glyph mask projected with sleeve homography",
        })
    (Path(str(out_path) + ".boxes.json")).write_text(json.dumps({
        "size": list(SIZE), "text_free": False, "condition": "C2: editable text projected onto sleeve plane",
        "copy": "Noche de vinilos · Sala Taller · 14 nov · 21:00", "boxes": boxes,
    }, ensure_ascii=False, indent=2) + "\n")
    evidence = {
        "baseline": "Step 9 flyer A; John's preference is perspective-warped printed lettering.",
        "correction_rounds_used": 1,
        "source_asset": str(SOURCE.relative_to(REPO)), "source_sha256": sha(SOURCE),
        "source_size_px": [source_w, source_h], "final_size_px": list(SIZE),
        "surface": "blank matte cream sleeve; type is on its photographed plane",
        "corner_measurement": "long Canny/Hough edge fits intersected; source pixel coordinates",
        "corners_source_px": source_corners.tolist(), "corners_final_px": dst.tolist(),
        "rectified_plane_px": list(PLANE), "safe_inset_ratio": 0.05,
        "homography_rectified_to_final": H.tolist(),
        "inverse_homography_final_to_rectified": inverse.tolist(),
        "corner_roundtrip_residual_px": float(np.max(np.linalg.norm(
            cv2.perspectiveTransform(dst.reshape(-1, 1, 2), inverse).reshape(-1, 2) - rect, axis=1))),
        "integration": "multiply-style warm dark brown print; local sleeve luminance and grain modulate ink alpha; no shadow/stroke/panel; the separator before Sala Taller is attached to the metadata line, with no isolated divider dot",
        "headline": {"editable_text": "Noche de\\nvinilos", "font": "BricolageGrotesque-Bold.ttf", "font_px_rectified": 124,
                     "cap_px_rectified": 82, "cap_px_feed360_approx": 27.33},
        "metadata": {"editable_text": "· Sala Taller · 14 nov · 21:00", "font": "InstrumentSans-Regular.ttf", "font_px_rectified": 64,
                     "cap_px_rectified": 46, "cap_px_feed360_approx": 15.33,
                     "horizontal_compression": metadata_ratio},
        "title_metadata_cap_ratio": 82 / 46,
        "candidate_claim": "visual appearance requires judge review; geometric projection metrics are recorded, not a universal validated rule",
        "output_sha256": sha(out_path),
    }
    (ROOT / "surface-evidence.json").write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(out_path), "sha256": evidence["output_sha256"],
                      "corner_roundtrip_residual_px": evidence["corner_roundtrip_residual_px"]}, indent=2))


if __name__ == "__main__":
    main()
