#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

REPO = Path(__file__).resolve().parents[6]
S9 = REPO / 'evals/art-direction/diagnostic-2026-10-22/renders/step9'
OUT = Path(__file__).resolve().parent
SIZE = (1280, 720)
FONT = REPO / 'skills/cropmark/fonts/BricolageGrotesque-Bold.ttf'
INK = (247, 243, 232)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def fitted(path):
    return ImageOps.fit(Image.open(path).convert('RGB'), SIZE,
                        method=Image.Resampling.LANCZOS, centering=(.5, .5))


def component(mask, predicate):
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask.astype(np.uint8), 8)
    parts=[]
    for x,y,w,h,area in stats[1:]:
        if predicate(x,y,w,h,area):
            parts.append({'box':[int(x),int(y),int(x+w),int(y+h)],'width':int(w),'height':int(h),'area_px':int(area),'fill_ratio':round(float(area/(w*h)),4)})
    if not parts:
        raise RuntimeError('measurement glyph component not found')
    return max(parts,key=lambda p:(p['height'],p['area_px']))


def measure_raster_a():
    a=np.array(Image.open(S9/'thumbnail/A.png').convert('RGB'))
    crop=a[490:650,40:1040].astype(np.int16)
    r,g,b=crop[:,:,0],crop[:,:,1],crop[:,:,2]
    # A's known one-line raster overlay uses warm cream and cyan; this local mask
    # isolates the P in Portfolio, then drops small background highlights by CC size.
    m=(((r>210)&(g>205)&(b>195)&((r-b)<65)) | ((b>135)&(g>70)&((b-r)>35)&((b-g)>-35)))
    p=component(m,lambda x,y,w,h,area: x+40>=400 and x+40<=500 and y+490>=500 and y+490<=550 and h>=100 and area>=2000)
    p['box']=[p['box'][0]+40,p['box'][1]+490,p['box'][2]+40,p['box'][3]+490]
    p['method']='visible P glyph component segmented from A raster cream/cyan ink in supplied approximate copy region'
    return p


def measure_delta(final_path, base_path, p_predicate):
    fin=np.array(Image.open(final_path).convert('RGB')).astype(np.int16)
    base=np.array(base_path.convert('RGB')).astype(np.int16)
    delta=np.max(np.abs(fin-base),axis=2)>30
    return component(delta,p_predicate)


def main():
    base_path=S9/'thumbnail/B-base-R1-source.png'
    base=fitted(base_path)
    im=base.copy()
    d=ImageDraw.Draw(im)
    small=ImageFont.truetype(str(FONT),126)
    large=ImageFont.truetype(str(FONT),200)
    # The short setup line stays left in the quiet desk zone. The portfolio word
    # carries the stake at A-level visible cap height in the dark lower copy band.
    d.text((54,385),'3 AIs.',font=small,fill=INK,anchor='lt')
    large_text='1 Portfolio.'
    bbox=d.textbbox((54,490),large_text,font=large,anchor='lt',stroke_width=5)
    layer=Image.new('RGBA',(bbox[2]-bbox[0],bbox[3]-bbox[1]),(0,0,0,0))
    ld=ImageDraw.Draw(layer)
    ld.text((0,0),large_text,font=large,fill=INK,anchor='lt',stroke_width=5,stroke_fill=INK)
    # A modest 12% horizontal condensation keeps the dominant word clear of the
    # lower-right robot while preserving the measured cap height and heavy stems.
    layer=layer.resize((round(layer.width*.88),layer.height),Image.Resampling.LANCZOS)
    im.paste(layer.convert('RGB'),(bbox[0],bbox[1]),layer.getchannel('A'))
    out=OUT/'C.png'
    im.save(out,optimize=True)
    # Editable source metadata and a standalone layer description.
    textbox=d.textbbox((54,385),'3 AIs.',font=small,anchor='lt')
    bigbox=d.textbbox((54,490),large_text,font=large,anchor='lt',stroke_width=5)
    bigbox=[54,490,54+round((bigbox[2]-bigbox[0])*.88),490+(bigbox[3]-bigbox[1])]
    (OUT/'C.png.boxes.json').write_text(json.dumps({
      'size':list(SIZE),'text_free':False,'condition':'Paso 10 C; Cropmark/Pillow overlay on generated B-R1 scene base',
      'copy':'3 AIs. 1 Portfolio.','scene_concept':'same real generated B-R1 scene: three agents actively adjust one shared portfolio grid',
      'surface_case':'No plausible surface for this headline; set flat in the dark clean lower-left copy zone, not on the pictured portfolio screen.',
      'source_base':str(base_path.relative_to(REPO)),'source_sha256':sha(base_path),
      'crop_operation':'center crop to 16:9 then Lanczos resize to 1280x720',
      'boxes':[
       {'role':'headline_kicker','text':'3 AIs.','box':list(textbox),'size':126,'font_path':'skills/cropmark/fonts/BricolageGrotesque-Bold.ttf','fill':list(INK)},
       {'role':'headline','text':'1 Portfolio.','box':bigbox,'size':200,'font_path':'skills/cropmark/fonts/BricolageGrotesque-Bold.ttf','fill':list(INK)}
      ],
      'groups':[
       {'role':'headline_kicker','text':'3 AIs.','box':list(textbox),'font_file':'skills/cropmark/fonts/BricolageGrotesque-Bold.ttf','font_size':126,'ink_srgb':list(INK)},
       {'role':'headline','text':'1 Portfolio.','box':bigbox,'font_file':'skills/cropmark/fonts/BricolageGrotesque-Bold.ttf','font_size':200,'ink_srgb':list(INK),'horizontal_scale':0.88,'stroke_width':5}
      ],'effects':{'shadow':False,'stroke':True,'stroke_treatment':'5px same-ink weight reinforcement; no outline contrast','text_panel':False},'output_sha256':sha(out)
    },ensure_ascii=False,indent=2)+'\n')
    for width in (360,168):
        h=round(SIZE[1]*width/SIZE[0])
        im.resize((width,h),Image.Resampling.LANCZOS).save(OUT/f'C-{width}.png',optimize=True)
    # Measure a common capital P glyph directly in each raster output.
    a=measure_raster_a()
    b_path=S9/'thumbnail/B-R1.png'
    b=measure_delta(b_path,fitted(base_path),lambda x,y,w,h,area: 100<=x<=190 and 595<=y<=680 and h>=50 and area>=1000)
    b['method']='visible P glyph component from B-R1 overlay pixel delta against the exact clean source base'
    c=measure_delta(out,base,lambda x,y,w,h,area: 100<=x<=250 and 480<=y<=710 and h>=100 and area>=2000)
    c['method']='visible P glyph component from C overlay pixel delta against the exact clean source base'
    for p in (a,b,c):
        p['cap_percent_frame_height']=round(100*p['height']/SIZE[1],3)
        p['cap_px_at_168']=round(p['height']*168/SIZE[0],2)
    report={'measurement':'same uppercase P glyph; connected-component visible ink bounds; A uses known raster-ink mask in its supplied approximate copy crop, B/C use pixel-difference masks against clean generated bases','frame_px':list(SIZE),'A':a,'B-R1':b,'C':c,'C_minus_A_percent_points':round(c['cap_percent_frame_height']-a['cap_percent_frame_height'],3),'C_minus_B_percent_points':round(c['cap_percent_frame_height']-b['cap_percent_frame_height'],3),'C_weight_metric':'P glyph foreground fill ratio (ink component pixels / glyph bounding box area); C uses a 5px same-ink stroke as integral heavy face weight','font_license':'Bricolage Grotesque is bundled in skills/cropmark/fonts; OFL license present there.','call_count_image_gen':0,'correction_rounds_used':1}
    report['A']['weight_metric']=report['C_weight_metric']; report['B-R1']['weight_metric']=report['C_weight_metric']; report['C']['weight_metric']=report['C_weight_metric']
    (OUT/'measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'final':str(out),'measurements':report},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
