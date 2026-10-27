"""cropmark Pillow helpers (MIT). Photo + few words: thumbnails, simple posts.
Every text/card call records its box so qa/qa.py can check safe zones and contrast:
save(img, path) writes path + '.boxes.json'."""
import json, math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance, ImageOps, ImageChops

FONTS = os.path.join(os.path.dirname(__file__), '..', '..', 'fonts')
_BOXES = []

def font(name, size, weight=None):
    """Bundled font by file stem ('Anton-Regular'); weight= sets the wght axis of variable fonts (e.g. Caveat-Variable)."""
    p = name if os.path.isabs(name) else os.path.join(FONTS, name if name.endswith('.ttf') else name + '.ttf')
    f = ImageFont.truetype(p, size)
    if weight is not None:
        try:
            axes=f.get_variation_axes()
            weights=[i for i,a in enumerate(axes) if a['name'].lower() in (b'weight','weight')]
            if not weights: raise ValueError('font has no weight axis')
            idx=weights[0]
            if not axes[idx]['minimum'] <= weight <= axes[idx]['maximum']: raise ValueError('weight outside font axis range')
            values=[a['default'] for a in axes];values[idx]=weight
            f.set_variation_by_axes(values)
        except OSError as exc: raise ValueError('requested weight requires a variable weight font') from exc
    return f

def reset():
    """Start a new piece: clears recorded QA boxes (call once per output)."""
    _BOXES.clear()

def new(w, h, color=(0, 0, 0)):
    reset(); return Image.new('RGB', (w, h), color)

def cover(src, w, h, focus=(0.5, 0.5), zoom=1.0):
    """Load + crop-to-fill around a focus point (0-1); zoom>1 crops tighter. Does NOT clear QA boxes."""
    im = Image.open(src).convert('RGB') if isinstance(src, str) else src.convert('RGB')
    s = max(w / im.width, h / im.height) * zoom; im = im.resize((math.ceil(im.width * s), math.ceil(im.height * s)), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1])
    return im.crop((x, y, x + w, y + h))

def grade(im, contrast=1.1, saturation=1.15, brightness=1.0, warmth=0):
    im = ImageEnhance.Contrast(im).enhance(contrast); im = ImageEnhance.Color(im).enhance(saturation)
    im = ImageEnhance.Brightness(im).enhance(brightness)
    if warmth:
        r, g, b = im.split(); r = r.point(lambda v: min(255, v + warmth)); b = b.point(lambda v: max(0, v - warmth)); im = Image.merge('RGB', (r, g, b))
    return im

def shade(im, side='left', strength=0.6, reach=0.55, color=(0, 0, 0)):
    """Soft local gradient to calm a text zone (side: left/right/top/bottom)."""
    w, h = im.size; m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    n = int((w if side in ('left', 'right') else h) * reach)
    for i in range(n):
        a = int(255 * strength * (1 - i / n) ** 1.6)
        if side == 'left': d.line([(i, 0), (i, h)], fill=a)
        elif side == 'right': d.line([(w - 1 - i, 0), (w - 1 - i, h)], fill=a)
        elif side == 'top': d.line([(0, i), (w, i)], fill=a)
        else: d.line([(0, h - 1 - i), (w, h - 1 - i)], fill=a)
    return Image.composite(Image.new('RGB', (w, h), color), im, m)

def vignette(im, strength=0.45):
    w, h = im.size; m = Image.new('L', (w, h), 0); d = ImageDraw.Draw(m)
    d.ellipse((-w * .15, -h * .15, w * 1.15, h * 1.15), fill=255); m = m.filter(ImageFilter.GaussianBlur(min(w, h) / 6))
    dark = ImageEnhance.Brightness(im).enhance(1 - strength); return Image.composite(im, dark, m)

def _line_w(f, s, tracking):
    return f.getlength(s) + tracking * f.size * max(0, len(s) - 1)

def _check_glyphs(f, s):
    """Reject the font's missing-glyph shape instead of silently drawing tofu."""
    missing = f.getmask('\U0010ffff')
    signature = (missing.size, bytes(missing))
    absent = []
    for c in set(s):
        if c.isspace(): continue
        mask = f.getmask(c)
        if (mask.size, bytes(mask)) == signature: absent.append(f'U+{ord(c):04X}')
    if absent: raise ValueError('Font lacks glyphs: ' + ', '.join(sorted(absent)))

def text(im, xy, s, f, fill=(255, 255, 255), anchor='la', tracking=0.0, leading=1.0, stroke=0, stroke_fill=(0, 0, 0),
         shadow=None, align='left', role='text'):
    """Multi-line text ('\n'). tracking in em. shadow=(dx,dy,blur,alpha). Returns bbox."""
    _check_glyphs(f, s)
    lines = s.split('\n'); lh = f.size * leading
    widths = [_line_w(f, l, tracking) for l in lines]; W = max(widths); H = lh * (len(lines) - 1) + f.size
    x, y = xy
    if anchor[0] == 'm': x -= W / 2
    elif anchor[0] == 'r': x -= W
    if anchor[1] == 'm': y -= H / 2
    elif anchor[1] == 'b': y -= H
    positions = []
    for i, l in enumerate(lines):
        lx = x + (W-widths[i])/2 if align == 'center' else x+W-widths[i] if align == 'right' else x
        ly = y+i*lh
        if tracking:
            positions.extend((lx+f.getlength(l[:k])+tracking*f.size*k,ly,c) for k,c in enumerate(l))
        elif l: positions.append((lx,ly,l))
    def draw_on(d, col, off=(0, 0), st=stroke):
        for px,py,part in positions:
            sf = col if d.mode == 'L' else stroke_fill
            d.text((px+off[0],py+off[1]),part,font=f,fill=col,stroke_width=st,stroke_fill=sf)
    if shadow:
        dx, dy, blur, alpha = shadow; layer = Image.new('L', im.size, 0); draw_on(ImageDraw.Draw(layer), 255, (dx, dy), stroke)
        layer = layer.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: int(v * alpha))
        im.paste(Image.new('RGB', im.size, (0, 0, 0)), (0, 0), layer)
    ink_layer=Image.new('RGBA',im.size,(0,0,0,0))
    draw_on(ImageDraw.Draw(ink_layer),fill)
    composed=Image.alpha_composite(im.convert('RGBA'),ink_layer)
    im.paste(composed.convert(im.mode))
    d = ImageDraw.Draw(im)
    ink = [d.textbbox((px,py),part,font=f,stroke_width=stroke) for px,py,part in positions]
    box = ([math.floor(min(b[0] for b in ink)), math.floor(min(b[1] for b in ink)),
            math.ceil(max(b[2] for b in ink)), math.ceil(max(b[3] for b in ink))] if ink else [int(x),int(y),int(x),int(y)])
    _BOXES.append({'role': role, 'text': s, 'box': box, 'fill': list(fill) if isinstance(fill, tuple) else fill,
                   'size': f.size, 'font_path': str(f.path), 'stroke_width': stroke,
                   'stroke_fill': list(stroke_fill) if isinstance(stroke_fill,tuple) else stroke_fill})
    return box

def fit(s, fontname, max_w, start=200, min_size=20, tracking=0.0, stroke=0):
    """Returns a FONT OBJECT (not a size) at the largest size where the widest line fits max_w."""
    if not (math.isfinite(max_w) and max_w > 0 and start >= min_size > 0):
        raise ValueError('fit requires positive width and start >= min_size > 0')
    size = int(start)
    while size >= min_size:
        f = font(fontname, size)
        _check_glyphs(f,s)
        def ink_width(line):
            if not line: return 0
            if tracking:
                boxes=[f.getbbox(c,stroke_width=stroke) for c in line]
                pos=[f.getlength(line[:k])+tracking*f.size*k for k in range(len(line))]
                return max(p+b[2] for p,b in zip(pos,boxes))-min(p+b[0] for p,b in zip(pos,boxes))
            b=f.getbbox(line,stroke_width=stroke)
            return max(_line_w(f,line,tracking),b[2]-b[0])
        if max(ink_width(l) for l in s.split('\n')) <= max_w: return f
        size -= 1
    raise ValueError(f'Text cannot fit width {max_w} at minimum size {min_size}')

def rounded(im, box, radius=28, fill=(255, 255, 255), shadow=(0, 14, 28, 0.35), outline=None, width=0, role='shape'):
    if shadow:
        dx, dy, blur, a = shadow; m = Image.new('L', im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([box[0] + dx, box[1] + dy, box[2] + dx, box[3] + dy], radius, fill=int(255 * a))
        im.paste(Image.new('RGB', im.size, (0, 0, 0)), (0, 0), m.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(im).rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)
    if role: _BOXES.append({'role': role, 'text': '', 'box': [int(v) for v in box]})

def card(im, xy, s, f, pad=(34, 22), fill=(255, 255, 255), color=(17, 17, 17), radius=28, icon=None, anchor='la'):
    """In-scene card (notification / label). icon=(rgb) draws a coloured dot badge."""
    _check_glyphs(f,s)
    if '\n' in s: raise ValueError('card/pill requires single-line text; use a text layout for multiline copy')
    bb = f.getbbox(s)
    tw,th = bb[2]-bb[0],bb[3]-bb[1]; iw = int(th * 1.1) + 18 if icon else 0
    W = tw + iw + pad[0] * 2; H = th + pad[1] * 2; x, y = xy
    if anchor[0] == 'm': x -= W / 2
    elif anchor[0] == 'r': x -= W
    if anchor[1] == 'm': y -= H / 2
    elif anchor[1] == 'b': y -= H
    rounded(im, [x, y, x + W, y + H], radius, fill, role=None)
    if icon:
        r = th * 0.55; cx = x + pad[0] + r; cy = y + H / 2; ImageDraw.Draw(im).ellipse([cx - r, cy - r, cx + r, cy + r], fill=icon)
    bb = f.getbbox(s)  # exact ink box -> true vertical centring for any font
    ty = y + H / 2 - (bb[1] + bb[3]) / 2
    ink_layer=Image.new('RGBA',im.size,(0,0,0,0))
    ImageDraw.Draw(ink_layer).text((x + pad[0] + iw - bb[0], ty), s, font=f, fill=color)
    im.paste(Image.alpha_composite(im.convert('RGBA'),ink_layer).convert(im.mode))
    _BOXES.append({'role': 'card', 'text': s, 'box': [math.floor(x + pad[0] + iw), math.floor(ty + bb[1]), math.ceil(x + pad[0] + iw + tw), math.ceil(ty + bb[3])],
                   'fill': list(color) if isinstance(color,tuple) else color, 'size': f.size, 'font_path': str(f.path)})
    _BOXES[-1]['bg'] = list(fill) if isinstance(fill,tuple) else fill
    return [math.floor(x),math.floor(y),math.ceil(x+W),math.ceil(y+H)]

def pill(im, xy, s, f, fill=(255, 210, 0), color=(0, 0, 0), pad=(26, 12), anchor='la'):
    return card(im, xy, s, f, pad=pad, fill=fill, color=color, radius=999, anchor=anchor)

def halftone(im, cell=10, angle=45, ink=(0, 0, 0), paper=None, gamma=0.8, max_r=0.62):
    """B/W halftone (RGBA, transparent paper if paper is None). gamma<1 lifts midtones so shadows don't fill solid."""
    g = ImageOps.autocontrast(ImageOps.grayscale(im)).point(lambda v: int(255 * (v / 255) ** gamma)).rotate(angle, expand=1, fillcolor=255); W, H = g.size
    out = Image.new('L', (W, H), 0); d = ImageDraw.Draw(out)
    for yy in range(0, H, cell):
        for xx in range(0, W, cell):
            v = g.getpixel((min(W - 1, xx + cell // 2), min(H - 1, yy + cell // 2))); r = (1 - v / 255) * cell * max_r
            if r > 0.4: d.ellipse([xx + cell / 2 - r, yy + cell / 2 - r, xx + cell / 2 + r, yy + cell / 2 + r], fill=255)
    out = out.rotate(-angle, expand=1); l = (out.width - im.width) // 2; t = (out.height - im.height) // 2
    m = out.crop((l, t, l + im.width, t + im.height))
    rgba = Image.new('RGBA', im.size, paper + (255,) if paper else (0, 0, 0, 0)); rgba.paste(Image.new('RGBA', im.size, ink + (255,)), (0, 0), m); return rgba

def torn_mask(size, jitter=7, seed=1):
    """Torn-paper alpha mask; jitter 5-9 looks like paper, >12 looks spiky."""
    random.seed(seed); w, h = size; pts = []
    for side in range(4):
        n = 18
        for i in range(n):
            t = i / n
            p = [(t * w, 0), (w, t * h), (w - t * w, h), (0, h - t * h)][side]
            pts.append((p[0] + random.uniform(-jitter, jitter) * (side % 2 == 1) + (jitter if side == 3 else -jitter if side == 1 else 0),
                        p[1] + random.uniform(-jitter, jitter) * (side % 2 == 0) + (jitter if side == 0 else -jitter if side == 2 else 0)))
    m = Image.new('L', size, 0); ImageDraw.Draw(m).polygon(pts, fill=255); return m

def key_out(im, bg=None, tol=40, feather=2):
    """Key only matching background connected to the border; not semantic segmentation.

    Enclosed matching detail is preserved. Matching subject detail connected to
    the border is still ambiguous: use a subject mask or retain the photograph.
    """
    if not 0 <= tol <= 255 or feather < 0: raise ValueError('invalid key tolerance/feather')
    out = im.convert('RGBA'); rgb=out.convert('RGB'); bg=bg if bg is not None else rgb.getpixel((0,0))
    diff=ImageChops.difference(rgb,Image.new('RGB',rgb.size,bg))
    r,g,b=diff.split(); largest=ImageChops.lighter(ImageChops.lighter(r,g),b)
    candidates=largest.point(lambda v:255 if v <= tol else 0)
    # Native flood fill marks only background candidates reachable from an edge.
    w,h=candidates.size
    for x in range(w):
        for y in (0,h-1):
            if candidates.getpixel((x,y)) == 255: ImageDraw.floodfill(candidates,(x,y),128)
    for y in range(h):
        for x in (0,w-1):
            if candidates.getpixel((x,y)) == 255: ImageDraw.floodfill(candidates,(x,y),128)
    a=candidates.point(lambda v:0 if v == 128 else 255)
    if feather: a=a.filter(ImageFilter.GaussianBlur(feather))
    out.putalpha(ImageChops.multiply(out.getchannel('A'),a))
    return out

def paste(im, layer, xy, scale=1.0):
    if scale != 1: layer = layer.resize((int(layer.width * scale), int(layer.height * scale)), Image.LANCZOS)
    im.paste(layer, (int(xy[0]), int(xy[1])), layer if layer.mode == 'RGBA' else None); return layer.size

def rotated(im, layer, xy, angle, role='shape'):
    """Paste an RGBA layer (e.g. a sticky note made with new_layer + text) rotated by angle degrees; records its box."""
    r = layer.rotate(angle, expand=True, resample=Image.BICUBIC); im.paste(r, (int(xy[0]), int(xy[1])), r)
    _BOXES.append({'role': role, 'text': '', 'box': [int(xy[0]), int(xy[1]), int(xy[0] + r.width), int(xy[1] + r.height)]}); return r.size

def sticky(im, xy, s, f, angle=-5, paper=(255, 228, 92), ink=(30, 30, 30), pad=40, tape=True):
    """Handwritten sticky note (text-in-scene). Text box is recorded for QA."""
    _check_glyphs(f,s)
    tw = max(_line_w(f, l, 0) for l in s.split('\n')); th = f.size * 1.1 * len(s.split('\n'))
    W, H = int(tw + pad * 2), int(th + pad * 2); L = Image.new('RGBA', (W + 40, H + 40), (0, 0, 0, 0))
    sh = Image.new('L', L.size, 0); ImageDraw.Draw(sh).rectangle([24, 28, W + 16, H + 20], fill=110); L.putalpha(0)
    base = Image.new('RGBA', L.size, (0, 0, 0, 0)); base.paste((0, 0, 0, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(10)))
    d = ImageDraw.Draw(base); d.rectangle([16, 16, W + 16, H + 16], fill=paper + (255,))
    for i, l in enumerate(s.split('\n')): d.text((16 + pad, 16 + pad + i * f.size * 1.1), l, font=f, fill=ink)
    if tape: d.rectangle([W / 2 - 50 + 16, 4, W / 2 + 50 + 16, 34], fill=(240, 240, 230, 190))
    size = rotated(im, base, xy, angle, role=None)
    _BOXES.append({'role': 'card', 'text': s, 'box': [int(xy[0]), int(xy[1]), int(xy[0] + size[0]), int(xy[1] + size[1])], 'fill': list(ink), 'bg': list(paper), 'size': f.size, 'font_path':str(f.path)}); return size

def blur_region(im, box, radius=18):
    """Tease a value (ui-hero): blur only that region."""
    r = im.crop(box).filter(ImageFilter.GaussianBlur(radius)); im.paste(r, box[:2]); return im

def despill(layer, strength=1.0):
    """Remove green fringe from a keyed RGBA cutout (green-screen generations)."""
    r, g, b, a = layer.split()
    lim = ImageChops.lighter(r, b)
    if not 0 <= strength <= 1: raise ValueError('despill strength must be in [0,1]')
    corrected=ImageChops.subtract(g,ImageChops.subtract(g,lim))
    g2=Image.blend(g,corrected,strength)
    return Image.merge('RGBA', (r, g2, b, a))

def clean_cutout(layer, key=None, tol=60, erode=0, feather=0, despill_strength=0):
    """Preserve identity/alpha by default. Key/erosion/feather/despill are explicit.

    These operations do not infer a subject mask and are unsafe as automatic
    cleanup for hair, logos, translucent materials or matching subject colors.
    """
    if not isinstance(erode,int) or erode < 0 or feather < 0 or not 0 <= despill_strength <= 1:
        raise ValueError('invalid cutout cleanup parameters')
    layer = layer.convert('RGBA')
    if key:
        k = key_out(layer.convert('RGB'), key, tol, 0); a = ImageChops.multiply(layer.split()[3], k.split()[3])
    else: a = layer.split()[3]
    if erode: a = a.filter(ImageFilter.MinFilter(erode * 2 + 1))
    if feather: a=a.filter(ImageFilter.GaussianBlur(feather))
    out=despill(layer,despill_strength) if despill_strength else layer.copy()
    out.putalpha(a); return out

def tag(im, xy, s, f, angle=-8, paper=(201, 164, 112), ink=(40, 28, 18), string=True):
    """Kraft hang tag with a hole + string (text-in-scene price/label tag). Box recorded for QA."""
    _check_glyphs(f,s)
    tw = _line_w(f, s, 0); W, H = int(tw + f.size * 1.9), int(f.size * 2.1)
    L = Image.new('RGBA', (W + 30, H + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    pts = [(15 + H * .45, 15), (15 + W, 15), (15 + W, 15 + H), (15 + H * .45, 15 + H), (15, 15 + H / 2)]
    d.polygon(pts, fill=paper + (255,)); r = f.size * .14; cx, cy = 15 + H * .5, 15 + H / 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(0, 0, 0, 0)); d.text((15 + H * .5 + r * 3, 15 + H / 2), s, font=f, fill=ink, anchor='lm')
    size = rotated(im, L, xy, angle, role=None)
    _BOXES.append({'role': 'card', 'text': s, 'box': [int(xy[0]), int(xy[1]), int(xy[0] + size[0]), int(xy[1] + size[1])], 'fill': list(ink), 'bg': list(paper), 'size': f.size, 'font_path':str(f.path)}); return size

def compare_sheet(pairs, out, label=('before', 'after'), w=640):
    """Before/after sheet: pairs = [(before_path, after_path, caption), ...]."""
    ims = []
    for a, b, cap in pairs:
        A = Image.open(a).convert('RGB'); B = Image.open(b).convert('RGB'); h = int(w * A.height / A.width)
        ims.append((A.resize((w, h)), B.resize((w, h)), cap))
    H = sum(x[0].height + 60 for x in ims) + 20; S = Image.new('RGB', (w * 2 + 60, H), (24, 24, 24)); d = ImageDraw.Draw(S); y = 20
    f = font('InstrumentSans-Bold', 26)
    for A, B, cap in ims:
        d.text((20, y), f'{cap}  —  {label[0]}', font=f, fill=(200, 200, 200)); d.text((w + 40, y), f'{cap}  —  {label[1]}', font=f, fill=(255, 255, 255))
        S.paste(A, (20, y + 36)); S.paste(B, (w + 40, y + 36)); y += A.height + 60
    S.save(out, quality=90); return out

def save(im, path, quality=92, boxes_dir=None, *, text_free=False):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    im.save(path, quality=quality) if path.lower().endswith(('.jpg', '.jpeg')) else im.save(path)
    bp = os.path.join(boxes_dir, os.path.basename(path)) if boxes_dir else path
    if boxes_dir: os.makedirs(boxes_dir, exist_ok=True)
    json.dump({'size': im.size, 'boxes': _BOXES, 'text_free':text_free}, open(bp + '.boxes.json', 'w'), ensure_ascii=False, indent=1)
    return path
