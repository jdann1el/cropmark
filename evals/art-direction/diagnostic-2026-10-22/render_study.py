from pathlib import Path
import sys
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "skills/cropmark/engines/pillow"))
import cm

OUT = Path(__file__).resolve().parent / "out"
BG = (173, 179, 89)
WHITE = (255, 255, 255)
PALE = (225, 225, 163)
BG_WORD = (184, 189, 106)


def top_text(im, text, font, x, top, color, role):
    return cm.text(im, (x, top - font.getbbox(text)[1]), text, font,
                   fill=color, role=role)


def centered_top(im, text, font, cx, top, color, role, tracking=0):
    return cm.text(im, (cx, top - font.getbbox(text)[1]), text, font,
                   fill=color, anchor="ma", tracking=tracking, role=role)


def add_vertical_background_word(im, size=360):
    text = "glicemia"
    font = cm.font("DMSerifDisplay-Regular", size)
    bb = font.getbbox(text)
    layer = Image.new("RGBA", (bb[2] - bb[0], bb[3] - bb[1]), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((-bb[0], -bb[1]), text, font=font, fill=BG_WORD + (255,))
    rotated = layer.rotate(-90, expand=True, resample=Image.Resampling.BICUBIC)
    left, top = 787, 0
    visible = rotated.crop((0, 0, min(rotated.width, 1080 - left), min(rotated.height, 1350 - top)))
    ink = visible.getchannel("A").getbbox()
    im.paste(rotated, (left, top), rotated)
    if ink:
        cm._BOXES.append({"role": "background-word", "text": text,
                          "box": [left + ink[0], top + ink[1], left + ink[2], top + ink[3]],
                          "fill": list(BG_WORD), "size": size, "font_path": str(font.path)})


def render(path, headline_size, brand, subline_size=45):
    im = cm.new(1080, 1350, BG)
    add_vertical_background_word(im)

    centered_top(im, brand, cm.font("Outfit-Regular", 24), 316, 304,
                 WHITE, "logo", tracking=0.17)
    centered_top(im, "NUTRICIONISTA", cm.font("Outfit-Regular", 12), 316, 336,
                 WHITE, "logo", tracking=0.36)

    regular = cm.font("DMSerifDisplay-Regular", headline_size)
    italic = cm.font("DMSerifDisplay-Italic", headline_size)
    ascent = regular.getmetrics()[0]
    cm.text(im, (189, 526 - ascent), "Você", regular, fill=WHITE, role="headline")
    cm.text(im, (189, 633 - ascent), "sabe qual", regular, fill=WHITE, role="headline")
    prefix = "é a "
    cm.text(im, (189, 739 - ascent), prefix, regular, fill=WHITE, role="headline")
    cm.text(im, (189 + regular.getlength(prefix), 739 - italic.getmetrics()[0]),
            "pior", italic, fill=WHITE, role="headline")
    cm.text(im, (188, 844 - ascent), "glicemia?", regular, fill=WHITE, role="headline")

    ImageDraw.Draw(im).line((187, 912, 631, 912), fill=WHITE, width=3)
    cm._BOXES.append({"role": "rule", "text": "", "box": [187, 911, 632, 914],
                      "fill": list(WHITE), "size": 3})
    top_text(im, "Não é a de 400...", cm.font("Outfit-Regular", subline_size),
             198, 945, WHITE, "subline")

    ImageDraw.Draw(im).rounded_rectangle((187, 1070, 457, 1124), radius=28,
                                         fill=BG, outline=PALE, width=3)
    cm._BOXES.append({"role": "pill-shape", "text": "", "box": [187, 1070, 458, 1125],
                      "fill": list(BG), "outline": list(PALE), "stroke_width": 3})
    centered_top(im, "LEIA A LEGENDA", cm.font("Outfit-Regular", 24), 322.5,
                 1088, PALE, "cta")
    cm.save(im, str(path))


OUT.mkdir(parents=True, exist_ok=True)
renders = [
    ("R0-initial-104.png", 104, "ESPAÇO NUTRIÇÃO"),
    ("R1-headline-106.png", 106, "ESPAÇO NUTRIÇÃO"),
    ("R2-neutral-wordmark.png", 106, "VIDA LEVE SAUDE"),
    ("R3-subline-47-final.png", 106, "VIDA LEVE SAUDE", 47),
]
for item in renders:
    filename, size, brand, *extra = item
    render(OUT / filename, size, brand, *(extra or [45]))
source = Path("/workspace/cropmark-refs/07-design-social-media-nutricionista/07-02.png")
cm.compare_sheet([(str(source), str(OUT / renders[-1][0]), "Final R3")],
                 str(OUT / "reference-vs-final.jpg"),
                 label=("Reference", "Reconstruction"), w=640)
for item in renders:
    print(OUT / item[0])
print(OUT / "reference-vs-final.jpg")
