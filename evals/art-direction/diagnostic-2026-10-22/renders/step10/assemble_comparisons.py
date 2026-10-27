#!/usr/bin/env python3
"""Build Paso 10 comparisons from the final PNGs without altering them."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

S10 = Path(__file__).resolve().parent
S9 = S10.parent / "step9"
S8 = S10.parent / "step8"


def open_rgb(path: Path, size: tuple[int, int]) -> Image.Image:
    im = Image.open(path).convert("RGB")
    if im.size != size:
        raise ValueError(f"{path}: expected {size}, got {im.size}")
    return im


def row(paths: list[Path], size: tuple[int, int]) -> Image.Image:
    panels = [open_rgb(path, size) for path in paths]
    out = Image.new("RGB", (size[0] * len(panels), size[1]), "white")
    for i, panel in enumerate(panels):
        out.paste(panel, (i * size[0], 0))
    return out


def save_thumb(width: int, name: str) -> None:
    height = 203 if width == 360 else 95
    paths = [S9 / "thumbnail/A.png", S9 / "thumbnail/B-R1.png", S10 / "thumbnail/C.png"]
    panels = [open_rgb(p, (1280, 720)).resize((width, height), Image.Resampling.LANCZOS)
              for p in paths]
    out = Image.new("RGB", (width * 3, height), "white")
    for i, panel in enumerate(panels):
        out.paste(panel, (i * width, 0))
    out.save(S10 / name)


def main() -> None:
    thumb_paths = [S9 / "thumbnail/A.png", S9 / "thumbnail/B-R1.png", S10 / "thumbnail/C.png"]
    row(thumb_paths, (1280, 720)).save(S10 / "thumb-ABC.png")
    save_thumb(360, "thumb-ABC-360.png")
    save_thumb(168, "thumb-ABC-168.png")

    flyer_paths = [S9 / "flyer/A.png", S10 / "flyer/C.png"]
    row(flyer_paths, (1080, 1350)).save(S10 / "flyer-AC.png")
    flyer_360 = [open_rgb(p, (1080, 1350)).resize((360, 450), Image.Resampling.LANCZOS)
                 for p in flyer_paths]
    out = Image.new("RGB", (720, 450), "white")
    out.paste(flyer_360[0], (0, 0))
    out.paste(flyer_360[1], (360, 0))
    out.save(S10 / "flyer-AC-360.png")

    b2 = [S8 / f"B2/final-{i}.png" for i in range(1, 4)]
    b4 = [S10 / f"carousel/B4-{i}.png" for i in range(1, 4)]
    b2_row = row(b2, (1080, 1350))
    b4_row = row(b4, (1080, 1350))
    carousel = Image.new("RGB", (3240, 2700), "white")
    carousel.paste(b2_row, (0, 0))
    carousel.paste(b4_row, (0, 1350))
    carousel.save(S10 / "carousel-B2B4-feed.png")
    carousel_360 = Image.new("RGB", (1080, 900), "white")
    for row_index, paths in enumerate((b2, b4)):
        for i, path in enumerate(paths):
            panel = open_rgb(path, (1080, 1350)).resize((360, 450), Image.Resampling.LANCZOS)
            carousel_360.paste(panel, (i * 360, row_index * 450))
    carousel_360.save(S10 / "carousel-B2B4-feed-360.png")

    manifest = {
        "imagegen_calls_for_paso10": 0,
        "thumbnail_order": ["Paso 9 A", "Paso 9 B-R1", "Paso 10 C"],
        "flyer_order": ["Paso 9 A", "Paso 10 C"],
        "carousel_rows": ["B2", "B4"],
        "outputs": {
            "thumb-ABC.png": [3840, 720],
            "thumb-ABC-360.png": [1080, 203],
            "thumb-ABC-168.png": [504, 95],
            "flyer-AC.png": [2160, 1350],
            "flyer-AC-360.png": [720, 450],
            "carousel-B2B4-feed.png": [3240, 2700],
            "carousel-B2B4-feed-360.png": [1080, 900],
        },
    }
    (S10 / "comparison-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
