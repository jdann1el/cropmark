"""Render the typographic Step 2 transfer study with the bundled Pillow engine."""
from pathlib import Path
import json
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm

OUT = Path(__file__).resolve().parent / "renders/step2"
FONT_DIR = ROOT / "skills/cropmark/fonts"
BG = (32, 51, 49)          # #203331, night forest
CREAM = (245, 239, 222)     # #f5efde
ACCENT = (217, 200, 147)    # #d9c893
GHOST = (113, 132, 122)     # #71847a, muted but feed-visible
GHOST_ALPHA = 0.36           # ornamental word; not part of the reading copy
LEFT = 187
# ImageDraw.rectangle includes its final pixel: 1047 yields a 32 px right safe margin.
GHOST_VIEW = (790, 70, 1047, 1280)

SLIDES = [
    {
        "id": "01",
        "role": "cover",
        "title_size": 124,
        "title_pitch": 132,
        "title_lines": [
            [("Baja", False)],
            [("el ", False), ("día.", True)],
        ],
        "column_width": 450,
        "subline": ["Una pausa suave al final", "de la tarde."],
        "subline_top": None,
        "cta": "SIGUE LEYENDO",
        "ghost": "PAUSA",
    },
    {
        "id": "02",
        "role": "practical_step",
        "title_size": 72,
        "title_pitch": 82,
        "title_lines": [
            [("Prueba una", False)],
            [("rutina sencilla", False)],
            [("para darle sitio", False)],
            [("al ", False), ("descanso.", True)],
        ],
        "column_width": 490,
        "subline": ["Deja una cosa lista para mañana;", "después, apaga lo que te distrae."],
        "subline_top": None,
        "cta": "PRUEBA ESTA NOCHE",
        "ghost": "RITUAL",
    },
    {
        "id": "03",
        "role": "close",
        "title_size": 112,
        "title_pitch": 120,
        "title_lines": [
            [("Suelta", False)],
            [("por ", False), ("hoy.", True)],
        ],
        "column_width": 450,
        "subline": ["Elige un gesto sencillo", "para marcar el cierre."],
        "subline_top": None,
        "cta": "GUARDA ESTA PAUSA",
        "ghost": "CALMA",
    },
]


def union(boxes):
    boxes = [b for b in boxes if b]
    return [min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes)] if boxes else None


def text_top(im, text, font, x, top, color, role, tracking=0):
    return cm.text(im, (x, top - font.getbbox(text)[1]), text, font,
                   fill=color, tracking=tracking, role=role)


def centered_top(im, text, font, cx, top, color, role, tracking=0):
    return cm.text(im, (cx, top - font.getbbox(text)[1]), text, font,
                   anchor="ma", tracking=tracking, fill=color, role=role)


def add_ghost_word(im, word, target_length=1100):
    """Draw a muted, cropped vertical word inside a declared right-side viewport."""
    base = cm.font("DMSerifDisplay-Regular", 100)
    size = round(100 * target_length / base.getlength(word))
    font = cm.font("DMSerifDisplay-Regular", size)
    bb = font.getbbox(word)
    layer = Image.new("RGBA", (bb[2] - bb[0], bb[3] - bb[1]), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((-bb[0], -bb[1]), word, font=font,
                               fill=GHOST + (round(255 * GHOST_ALPHA),))
    rotated = layer.rotate(-90, expand=True, resample=Image.Resampling.BICUBIC)
    x0, y0, x1, y1 = GHOST_VIEW
    x = x0 + (x1 - x0 - rotated.width) // 2
    y = y0 + (y1 - y0 - rotated.height) // 2
    stage = Image.new("RGBA", im.size, (0, 0, 0, 0))
    stage.alpha_composite(rotated, (x, y))
    viewport = Image.new("L", im.size, 0)
    ImageDraw.Draw(viewport).rectangle(GHOST_VIEW, fill=255)
    alpha = Image.new("L", im.size, 0)
    alpha = Image.composite(stage.getchannel("A"), alpha, viewport)
    stage.putalpha(alpha)
    im.paste(stage, (0, 0), stage.getchannel("A"))
    visible = stage.getchannel("A").getbbox()
    cm._BOXES.append({
        "role": "ghost-word", "text": "", "label": word,
        "decorative": True, "box": list(visible),
        "fill": list(GHOST), "size": size,
        "font_path": str(font.path), "opacity": GHOST_ALPHA,
    })
    return size, visible


def draw_rich_line(im, parts, regular, italic, x, ink_top, color):
    # cm.text's Pillow anchor is ascender-based. Convert the requested visible
    # ink top to that anchor using the highest run bbox so mixed italic runs
    # share a baseline and the recorded group gap matches the rendered pixels.
    run_boxes = []
    for content, is_italic in parts:
        font = italic if is_italic else regular
        run_boxes.append((content, font, font.getbbox(content)))
    anchor_y = ink_top - min(box[1] for _, _, box in run_boxes)
    cursor = x
    boxes = []
    for content, font, _ in run_boxes:
        box = cm.text(im, (cursor, anchor_y), content, font, fill=color, role="headline")
        boxes.append(box)
        cursor += font.getlength(content)
    return union(boxes)


def add_pill(im, label, top):
    font = cm.font("Outfit-Regular", 24)
    tracking = 0.045
    text_width = font.getlength(label) + tracking * font.size * max(0, len(label) - 1)
    width = round(text_width + 52)
    height = 58
    box = [LEFT, top, LEFT + width, top + height]
    ImageDraw.Draw(im).rounded_rectangle(box, radius=29, fill=BG, outline=ACCENT, width=3)
    cm._BOXES.append({"role": "shape", "text": "", "box": box,
                      "fill": list(BG), "outline": list(ACCENT), "stroke_width": 3})
    bbox = font.getbbox(label)
    ink_height = bbox[3] - bbox[1]
    text_top = top + (height - ink_height) / 2
    centered_top(im, label, font, LEFT + width / 2, text_top, ACCENT, "cta", tracking)
    return box


def draw_slide(spec, suffix="R0"):
    im = cm.new(1080, 1350, BG)
    ghost_size, ghost_box = add_ghost_word(im, spec["ghost"])

    logo_font = cm.font("Outfit-Regular", 27)
    descriptor_font = cm.font("Outfit-Regular", 18)
    brand = text_top(im, "NOCHE LENTA", logo_font, LEFT, 304, CREAM, "logo", tracking=0.105)
    brand_center = (brand[0] + brand[2]) / 2
    descriptor = centered_top(im, "HÁBITOS DE DESCANSO", descriptor_font,
                              brand_center, 339, CREAM, "descriptor", tracking=0.17)

    regular = cm.font("DMSerifDisplay-Regular", spec["title_size"])
    italic = cm.font("DMSerifDisplay-Italic", spec["title_size"])
    brand_bottom = max(brand[3], descriptor[3])
    headline_top = brand_bottom + 99
    title_boxes = []
    for index, parts in enumerate(spec["title_lines"]):
        ink_top = headline_top + index * spec["title_pitch"]
        title_boxes.append(draw_rich_line(im, parts, regular, italic, LEFT, ink_top, CREAM))
    title_box = union(title_boxes)
    title_width = title_box[2] - title_box[0]
    if title_width > spec["column_width"]:
        raise ValueError(f"{spec['id']} headline {title_width}px exceeds {spec['column_width']}px column")

    rule_y = title_box[3] + 42
    rule_width = round(title_width * 1.02)
    rule_box = [LEFT, rule_y, LEFT + rule_width, rule_y + 3]
    ImageDraw.Draw(im).line((rule_box[0], rule_y + 1, rule_box[2] - 1, rule_y + 1),
                            fill=CREAM, width=3)
    cm._BOXES.append({"role": "rule", "text": "", "box": rule_box,
                      "fill": list(CREAM), "size": 3})

    sub_font = cm.font("Outfit-Regular", 32)
    subline_top = rule_y + 40
    subline_boxes = []
    for index, line in enumerate(spec["subline"]):
        subline_boxes.append(text_top(im, line, sub_font, LEFT,
                                      subline_top + index * 40, CREAM, "subline"))
    subline_box = union(subline_boxes)
    pill_box = add_pill(im, spec["cta"], subline_box[3] + 86)

    path = OUT / f"slide-{spec['id']}-{suffix}.png"
    cm.save(im, str(path))
    metadata = json.loads(Path(str(path) + ".boxes.json").read_text())
    metadata["study"] = {
        "step": 2, "slide_role": spec["role"], "headline_column_width_px": spec["column_width"],
        "headline_ink_width_px": title_width, "rule_to_headline_width_pct": round(100 * rule_width / title_width, 2),
        "ghost_word_size_px": ghost_size, "ghost_word_visible_box_px": ghost_box,
        "ghost_word_target_length_px": 1100,
        "ghost_word_opacity": GHOST_ALPHA,
        "promised_left_inset_px": LEFT, "canvas_bg": "#203331",
    }
    Path(str(path) + ".boxes.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
    return {
        "path": path, "boxes_path": Path(str(path) + ".boxes.json"),
        "brand": brand, "descriptor": descriptor, "headline": title_box,
        "rule": rule_box, "subline": subline_box, "pill": pill_box,
        "ghost": ghost_box, "title_width": title_width, "rule_width": rule_width,
        "headline_top": headline_top, "subline_top": subline_top,
        "pill_top": pill_box[1], "ghost_size": ghost_size,
    }


def make_feed_sheet(slides, output, caption="PASO 2 • REVISIÓN EN FEED"):
    thumb_w, thumb_h = 360, 450
    gap, pad, header = 18, 22, 44
    sheet = Image.new("RGB", (pad * 2 + thumb_w * 3 + gap * 2,
                               pad * 2 + header + thumb_h), BG)
    draw = ImageDraw.Draw(sheet)
    label_font = ImageFont.truetype(str(FONT_DIR / "Outfit-Bold.ttf"), 19)
    draw.text((pad, pad + 8), caption, fill=CREAM, font=label_font)
    y = pad + header
    for index, slide in enumerate(slides):
        im = Image.open(slide["path"]).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        x = pad + index * (thumb_w + gap)
        sheet.paste(im, (x, y))
    sheet.save(output)
    return output


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    suffix = sys.argv[1] if len(sys.argv) > 1 else "R0"
    results = [draw_slide(spec, suffix=suffix) for spec in SLIDES]
    sheet = make_feed_sheet(results, OUT / f"{suffix}-feed-3up.png")
    for result in results:
        print(result["path"])
        print("  headline", result["headline"], "rule", result["rule"],
              "width ratio", round(100 * result["rule_width"] / result["title_width"], 2),
              "subline", result["subline"], "pill", result["pill"], "ghost", result["ghost"])
    print(sheet)


if __name__ == "__main__":
    main()
