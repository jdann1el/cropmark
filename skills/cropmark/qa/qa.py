#!/usr/bin/env python3
"""Cropmark technical QA. Exit 0: tested checks passed; 1: rejected; 2: invalid input.
Use --strict for delivery. Visual/content review is always required.
Filenames do not exempt references: validate reference inputs separately.
"""
import argparse
import json
import math
from pathlib import Path
import sys
from PIL import Image, ImageColor, ImageStat

SPEC = {'thumb': ((1280, 720), 320, 40), 'post': ((1080, 1350), 360, 64),
        'carousel': ((1080, 1350), 360, 64), 'story': ((1080, 1920), 360, 64),
        'reel': ((1080, 1920), 360, 64)}

def lum(c):
    def ch(v):
        v /= 255
        return v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4
    return .2126 * ch(c[0]) + .7152 * ch(c[1]) + .0722 * ch(c[2])

def contrast(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + .05) / (lb + .05)

def parse_color(c):
    """RGBA bytes. Lists use byte alpha; CSS rgba uses normalized alpha."""
    if isinstance(c, (list, tuple)) and len(c) in (3, 4):
        values = tuple(float(v) for v in c)
        if not all(math.isfinite(v) and 0 <= v <= 255 for v in values):
            raise ValueError('color channels must be finite bytes')
        return values if len(values) == 4 else values + (255,)
    if isinstance(c, str):
        if c == 'transparent': return (0, 0, 0, 0)
        if c.startswith('rgba(') and c.endswith(')'):
            values = [float(v.strip()) for v in c[5:-1].split(',')]
            if len(values) != 4 or not all(math.isfinite(v) for v in values):
                raise ValueError('invalid rgba color')
            if any(not 0 <= v <= 255 for v in values[:3]) or not 0 <= values[3] <= 1:
                raise ValueError('rgba channel out of range')
            return tuple(values[:3]) + (values[3] * 255,)
        try:
            values = ImageColor.getrgb(c)
            return values if len(values) == 4 else values + (255,)
        except (ValueError, TypeError): pass
    raise ValueError(f'unsupported color {c!r}')

def composite(fg, bg):
    alpha = fg[3] / 255
    return tuple(fg[i] * alpha + bg[i] * (1-alpha) for i in range(3))

def finite_numbers(values, length):
    return (isinstance(values, (list, tuple)) and len(values) == length
            and all(isinstance(v, (int, float)) and not isinstance(v, bool)
                    and math.isfinite(v) for v in values))

def check(fmt, path, *, boxes=None, strict=False):
    (W, H), feed, margin = SPEC[fmt]
    path = Path(path)
    im = Image.open(path).convert('RGB')
    result = [('OK' if im.size == (W,H) else 'FAIL', f'size {im.size} (want {W}x{H})')]
    bj = Path(str(path)+'.boxes.json')
    if not bj.exists() and boxes: bj = Path(boxes)/(path.name+'.boxes.json')
    if not bj.exists():
        alt = path.with_suffix('.png.boxes.json')
        if alt.exists(): bj = alt
    if not bj.exists(): result.append(('FAIL','no .boxes.json: text validation incomplete'))
    else:
        data = json.loads(bj.read_text())
        if not isinstance(data,dict) or not finite_numbers(data.get('size'),2) or min(data['size']) <= 0:
            raise ValueError(f'{bj.name}: positive finite coordinate size required')
        if not isinstance(data.get('boxes'),list): raise ValueError('metadata boxes must be a list')
        sx,sy = im.width/data['size'][0],im.height/data['size'][1]
        if abs(sx-sy) > 1e-6: raise ValueError('metadata aspect ratio differs from image')
        has_text=any(isinstance(b,dict) and isinstance(b.get('text',''),str)
                     and b.get('role','text') not in ('shape','bleed') and b.get('text','').strip()
                     for b in data['boxes'])
        if strict and not has_text and data.get('text_free') is not True:
            result.append(('FAIL','no text boxes require explicit text_free: true'))
        for b in data['boxes']:
            if not isinstance(b,dict) or not finite_numbers(b.get('box'),4):
                raise ValueError('each metadata box requires four finite coordinates')
            x0,y0,x1,y1 = [v*sx for v in b['box']]
            if x1 < x0 or y1 < y0: raise ValueError('box coordinates are reversed')
            text = b.get('text','')
            if not isinstance(text,str): raise ValueError('metadata text must be a string')
            t,role=text.replace('\n',' ')[:40],b.get('role','text')
            if role == 'bleed': continue
            if x0 < 0 or y0 < 0 or x1 > im.width or y1 > im.height:
                result.append(('FAIL',f'"{t}" leaves the canvas'))
            elif min(x0,y0,im.width-x1,im.height-y1) < margin/2:
                result.append(('FAIL' if strict and text.strip() else 'WARN',f'"{t}" too close to an edge'))
            is_text=role != 'shape' and bool(text.strip())
            if fmt == 'thumb' and x1 > W*.80 and y1 > H*.83:
                result.append(('FAIL' if is_text else 'WARN',f'"{t}" in bottom-right duration-badge zone'))
            if not is_text: continue
            if fmt == 'story' and (y0 < 270 or y1 > H-380):
                result.append(('FAIL',f'"{t}" in story safe zone overlay'))
            if fmt == 'reel' and (y0 < 270 or y1 > H*.65 or x1 > W-120):
                result.append(('FAIL',f'"{t}" in reel safe zone overlay'))
            size=b.get('size')
            if not isinstance(size,(int,float)) or not math.isfinite(size) or size <= 0:
                raise ValueError('text metadata requires positive finite font size')
            size *= sx
            if size < (34 if fmt == 'thumb' else 18):
                result.append(('WARN',f'"{t}" font {size:.0f}px may vanish at feed size'))
            if strict and not (b.get('font_path') or b.get('font_effective') or b.get('effectiveFonts')):
                result.append(('FAIL',f'"{t}" effective font not recorded'))
            fg=parse_color(b.get('fill',b.get('color')))
            opacity=b.get('opacity',1)
            if not isinstance(opacity,(int,float)) or not math.isfinite(opacity) or not 0 <= opacity <= 1:
                raise ValueError('text opacity must be finite and in [0,1]')
            fg=fg[:3]+(fg[3]*opacity,)
            if b.get('bg') is not None:
                declared_bg=parse_color(b['bg'])
                if declared_bg[3] < 255 and b.get('bg_backdrop') is None:
                    raise ValueError('translucent background needs its opaque bg_backdrop; cannot assume white')
                backdrop=parse_color(b.get('bg_backdrop',(255,255,255)))
                if backdrop[3] < 255: raise ValueError('bg_backdrop must be opaque')
                bg=composite(declared_bg,backdrop)
            else:
                pad=max(6,int((y1-y0)*.15));rings=[]
                for a,c,d,e in ((x0-pad,y0-pad,x1+pad,y0),(x0-pad,y1,x1+pad,y1+pad),
                                (x0-pad,y0,x0,y1),(x1,y0,x1+pad,y1)):
                    rect=(max(0,int(a)),max(0,int(c)),min(im.width,int(d)),min(im.height,int(e)))
                    if rect[2]>rect[0] and rect[3]>rect[1]: rings.append(im.crop(rect).resize((8,8)))
                if not rings:
                    result.append(('FAIL' if strict else 'WARN',f'"{t}" contrast not measurable'));continue
                strip=Image.new('RGB',(8*len(rings),8))
                for i,ring in enumerate(rings): strip.paste(ring,(8*i,0))
                bg=tuple(ImageStat.Stat(strip).median)
                result.append(('INFO',f'"{t}" contrast uses surrounding-background estimate; inspect photo/gradient visually'))
            cr=contrast(composite(fg,bg),bg)
            minimum=3 if size >= 60 else 4.5
            stroke=b.get('stroke_width',b.get('strokeWidth',0))
            if not isinstance(stroke,(int,float)) or not math.isfinite(stroke) or stroke < 0:
                raise ValueError('stroke width must be finite and nonnegative')
            stroke *= sx
            if cr < minimum and stroke >= max(1,size*.015) and b.get('stroke_fill') is not None:
                outline=parse_color(b['stroke_fill'])
                outline=outline[:3]+(outline[3]*opacity,)
                visible_outline=composite(outline,bg)
                outline_cr=contrast(visible_outline,bg)
                fill_outline_cr=contrast(composite(fg,visible_outline),visible_outline)
                if outline_cr >= minimum and fill_outline_cr >= 3:
                    result.append(('OK',f'"{t}" stroke contrast {outline_cr:.1f}:1; verify outline legibility at feed'))
                    continue
            result.append(('OK' if cr >= minimum else 'FAIL',f'"{t}" contrast {cr:.1f}:1'))
    preview=im.resize((feed,round(feed*im.height/im.width)),Image.Resampling.LANCZOS)
    return result,preview

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('format',choices=SPEC)
    parser.add_argument('--out',default='qa_out')
    parser.add_argument('--boxes')
    parser.add_argument('--strict',action='store_true',help='require complete metadata for delivery')
    parser.add_argument('--expected-count',type=int)
    parser.add_argument('files',nargs='+')
    args=parser.parse_args()
    if args.expected_count is not None and args.expected_count < 1: parser.error('expected-count must be positive')
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    report,previews,invalid,failed=[],[],False,False
    if args.expected_count is not None and len(args.files) != args.expected_count:
        failed=True;print(f'FAIL sequence: {len(args.files)} files, expected {args.expected_count}')
    for i,path in enumerate(args.files):
        try:
            findings,preview=check(args.format,path,boxes=args.boxes,strict=args.strict)
            preview.save(out/f'{i+1:02d}-feed-{Path(path).stem}.png');previews.append(preview)
            failed |= any(level == 'FAIL' for level,_ in findings)
        except (OSError,ValueError,TypeError,KeyError) as exc:
            findings=[('ERROR',str(exc))];invalid=True
        print(f'== {path}')
        for level,message in findings: print(f'  {level:5} {message}')
        report.append({'file':path,'findings':[{'level':l,'message':m} for l,m in findings]})
    if previews:
        gap,cols=8,min(len(previews),5)
        w,h=max(p.width for p in previews),max(p.height for p in previews)
        sheet=Image.new('RGB',(cols*(w+gap)+gap,math.ceil(len(previews)/cols)*(h+gap)+gap),(40,40,40))
        for i,pv in enumerate(previews): sheet.paste(pv,(gap+i%cols*(w+gap),gap+i//cols*(h+gap)))
        sheet.save(out/'contact_sheet.png')
    code=2 if invalid else 1 if failed else 0
    (out/'qa-report.json').write_text(json.dumps({'exit_code':code,'strict':args.strict,
        'expected_count':args.expected_count,'actual_count':len(args.files),
        'scope':'technical metadata checks; visual, semantic and fidelity review required','files':report},ensure_ascii=False,indent=2))
    return code

if __name__ == '__main__':sys.exit(main())
