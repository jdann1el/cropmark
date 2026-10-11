#!/usr/bin/env python3
"""cropmark QA (MIT). Usage: python qa.py <format> [--out DIR] [--boxes DIR] file1 [file2 ...]
Files whose name contains '_original' or '_before' are reported but never fail (intentional bad references).
format: thumb | post | carousel | story
Checks dimensions, text boxes from <file>.boxes.json (inside canvas, margins, thumbnail
bottom-right badge zone, min size, WCAG-ish contrast vs local background) and writes
feed-size previews + a contact sheet to ./qa_out/. Exit code 1 if any FAIL."""
import json, os, sys
from PIL import Image, ImageDraw, ImageStat
SPEC = {'thumb': ((1280, 720), 320, 40), 'post': ((1080, 1350), 360, 64), 'carousel': ((1080, 1350), 360, 64), 'story': ((1080, 1920), 360, 64)}

def lum(c):
    def ch(v):
        v /= 255; return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(c[0]) + 0.7152 * ch(c[1]) + 0.0722 * ch(c[2])

def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True); return (la + 0.05) / (lb + 0.05)

def parse_color(c):
    if isinstance(c, list): return tuple(c[:3])
    if isinstance(c, str) and c.startswith('rgb'): return tuple(int(float(x)) for x in c[c.index('(') + 1:c.index(')')].split(',')[:3])
    return (255, 255, 255)

def check(fmt, path):
    (W, H), feed, margin = SPEC[fmt]; out = []
    im = Image.open(path).convert('RGB')
    out.append(('OK' if im.size == (W, H) else 'FAIL', f'size {im.size} (want {W}x{H})'))
    bj = path + '.boxes.json'
    if BOXES and not os.path.exists(bj): bj = os.path.join(BOXES, os.path.basename(path) + '.boxes.json')
    if not os.path.exists(bj) and os.path.exists(path.rsplit('.', 1)[0] + '.png.boxes.json'): bj = path.rsplit('.', 1)[0] + '.png.boxes.json'
    if not os.path.exists(bj):
        out.append(('WARN', 'no .boxes.json: text checks skipped (render with the cropmark engines)'))
    else:
        data = json.load(open(bj)); sx = im.width / data['size'][0]
        for b in data['boxes']:
            x0, y0, x1, y1 = [v * sx for v in b['box']]; t = b['text'].replace('\n', ' ')[:30]
            if b.get('role') == 'bleed': continue
            if x0 < 0 or y0 < 0 or x1 > W or y1 > H: out.append(('FAIL', f'"{t}" leaves the canvas {b["box"]}'))
            elif min(x0, y0, W - x1, H - y1) < margin * 0.5 and b.get('role') != 'bleed': out.append(('WARN', f'"{t}" closer than {margin//2}px to an edge'))
            if fmt == 'thumb' and x1 > W * 0.80 and y1 > H * 0.83: out.append(('FAIL', f'"{t}" in the bottom-right duration-badge zone'))
            size = b.get('size', 99) * sx
            if fmt != 'thumb' and size < 18: out.append(('WARN', f'"{t}" font {size:.0f}px < 18px'))
            if fmt == 'thumb' and size < 34: out.append(('WARN', f'"{t}" font {size:.0f}px may vanish at 320px'))
            if b.get('role') == 'shape' or not b.get('text', '').strip():
                if fmt == 'thumb' and x1 > W * 0.80 and y1 > H * 0.83 and b.get('role') == 'shape': out.append(('WARN', f'shape {b["box"]} touches the duration-badge zone'))
                continue
            fg = parse_color(b.get('fill', b.get('color')))
            if x1 - x0 > 2 and y1 - y0 > 2:
                if b.get('bg'): bg = parse_color(b['bg'])
                else:  # sample a ring just outside the text box = what the letters sit on
                    pad = max(6, int((y1 - y0) * 0.15)); ring = []
                    for (a, c, d, e) in ((x0 - pad, y0 - pad, x1 + pad, y0), (x0 - pad, y1, x1 + pad, y1 + pad), (x0 - pad, y0, x0, y1), (x1, y0, x1 + pad, y1)):
                        a, c, d, e = max(0, int(a)), max(0, int(c)), min(W, int(d)), min(H, int(e))
                        if d - a > 1 and e - c > 1: ring.append(im.crop((a, c, d, e)).resize((8, 8)))
                    if not ring: continue
                    strip = Image.new('RGB', (8 * len(ring), 8)); [strip.paste(r, (8 * i, 0)) for i, r in enumerate(ring)]
                    bg = tuple(int(v) for v in ImageStat.Stat(strip).median)
                cr = contrast(fg, bg)
                lvl = 'OK' if cr >= 4.5 else 'WARN' if cr >= 3 else 'FAIL'
                if size >= 60 and cr >= 3: lvl = 'OK'
                if lvl != 'OK' or os.environ.get('QA_VERBOSE'): out.append((lvl, f'"{t}" contrast {cr:.1f}:1'))
    if fmt == 'thumb' and os.path.exists(bj):
        words = sum(len(b['text'].split()) for b in json.load(open(bj))['boxes'] if b.get('role') not in ('card', 'shape', 'brand'))
        if words > 4: out.append(('WARN', f'{words} headline words on a thumbnail (target ≤4; in-scene cards counted apart)'))
    if any(k in os.path.basename(path) for k in ('_original', '_before')):
        out = [('INFO' if l == 'FAIL' else l, m) for l, m in out]
    os.makedirs(OUT, exist_ok=True)
    pv = im.resize((feed, int(feed * im.height / im.width)), Image.LANCZOS)
    pv.save(os.path.join(OUT, 'feed_' + os.path.basename(path).rsplit('.', 1)[0] + '.png'))
    return out, pv

OUT, BOXES = 'qa_out', None

def main():
    global OUT, BOXES
    args = sys.argv[1:]; fmt = args.pop(0)
    while args and args[0].startswith('--'):
        k = args.pop(0); v = args.pop(0)
        if k == '--out': OUT = v
        elif k == '--boxes': BOXES = v
    files = args; fail = False; prevs = []
    for f in files:
        res, pv = check(fmt, f); prevs.append(pv)
        print(f'== {f}'); [print(f'  {l:4} {m}') for l, m in res]; fail |= any(l == 'FAIL' for l, _ in res)
    if prevs:
        g = 8; w = max(p.width for p in prevs); h = max(p.height for p in prevs); cols = min(len(prevs), 5)
        rows = (len(prevs) + cols - 1) // cols; S = Image.new('RGB', (cols * (w + g) + g, rows * (h + g) + g), (40, 40, 40))
        for i, p in enumerate(prevs): S.paste(p, (g + (i % cols) * (w + g), g + (i // cols) * (h + g)))
        S.save(os.path.join(OUT, 'contact_sheet.png')); print(f'previews -> {OUT}/ (open contact_sheet.png and LOOK at it)')
    sys.exit(1 if fail else 0)

if __name__ == '__main__': main()
