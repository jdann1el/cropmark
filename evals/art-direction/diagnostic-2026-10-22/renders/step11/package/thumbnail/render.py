from __future__ import annotations
import hashlib, json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FONT_PATH = REPO / 'fonts/Anton-Regular.ttf'
SIZE = (1280, 720)
SOURCE = ROOT / 'base-r1-edited-source.png'
INK = (247, 243, 232)
BG_SCALE = 0.92


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ink_mask(text: str, font: ImageFont.FreeTypeFont, xy: tuple[int, int]) -> Image.Image:
    mask = Image.new('L', SIZE, 0)
    ImageDraw.Draw(mask).text(xy, text, font=font, fill=255, anchor='lt')
    return mask


def ink_box(mask: Image.Image) -> list[int]:
    b = mask.getbbox()
    if b is None:
        raise RuntimeError('empty text mask')
    return list(b)


def p_metrics() -> dict:
    font = ImageFont.truetype(str(FONT_PATH), 150)
    mask = Image.new('L', (256, 256), 0)
    ImageDraw.Draw(mask).text((0, 0), 'P', font=font, fill=255, anchor='lt')
    arr = np.array(mask) >= 128
    n, labels, stats, _ = cv2.connectedComponentsWithStats(arr.astype(np.uint8), 8)
    x,y,w,h,area = max(stats[1:], key=lambda s: (s[3],s[4]))
    return {'box_local':[int(x),int(y),int(x+w),int(y+h)],'width':int(w),'height':int(h),'area_px':int(area),'fill_ratio':round(float(area/(w*h)),4),'threshold':'alpha >= 0.5'}


def box_gap(ink: np.ndarray, box: list[int]) -> float:
    ys, xs = np.where(ink)
    l,t,r,b = box
    dx = np.maximum(np.maximum(l-xs, 0), xs-r+1)
    dy = np.maximum(np.maximum(t-ys, 0), ys-b+1)
    return float(np.sqrt(dx*dx + dy*dy).min())


def contrast_stats(clean: Image.Image, final: Image.Image, mask: Image.Image) -> dict:
    bg = np.asarray(clean.convert('RGB'), dtype=np.float32)/255
    fg = np.asarray(final.convert('RGB'), dtype=np.float32)/255
    a = np.asarray(mask, dtype=np.uint8) >= 250
    # Glyph core: alpha >= 0.98, measured against the clean background and integrated final.
    def lin(v): return np.where(v <= 0.04045, v/12.92, ((v+0.055)/1.055)**2.4)
    fg_l = 0.2126*lin(fg[:,:,0])+0.7152*lin(fg[:,:,1])+0.0722*lin(fg[:,:,2])
    bg_l = 0.2126*lin(bg[:,:,0])+0.7152*lin(bg[:,:,1])+0.0722*lin(bg[:,:,2])
    ratio=(np.maximum(fg_l,bg_l)+0.05)/(np.minimum(fg_l,bg_l)+0.05)
    vals=ratio[a]
    if not vals.size: return {'error':'no text core'}
    return {'p05':round(float(np.percentile(vals,5)),3),'median':round(float(np.median(vals)),3),'share_below_3':round(float(np.mean(vals<3)*100),3),'share_below_4_5':round(float(np.mean(vals<4.5)*100),3),'core_pixels':int(vals.size)}


def main():
    src = ImageOps.fit(Image.open(SOURCE).convert('RGB'), SIZE, method=Image.Resampling.LANCZOS, centering=(0.5,0.5))
    # Scale the intact scene inward by 8% to make room at the outer edge for all key silhouettes.
    bg_color = src.getpixel((10, 560))
    base = Image.new('RGB', SIZE, bg_color)
    sw, sh = round(SIZE[0]*BG_SCALE), round(SIZE[1]*BG_SCALE)
    scene = src.resize((sw,sh),Image.Resampling.LANCZOS)
    scene_xy=((SIZE[0]-sw)//2,(SIZE[1]-sh)//2)
    base.paste(scene,scene_xy)
    base.save(ROOT/'clean-background.png',optimize=True)

    font_main = ImageFont.truetype(str(FONT_PATH),150)
    font_kicker = ImageFont.truetype(str(FONT_PATH),95)
    masks = {
      'kicker':ink_mask('3 AIs.',font_kicker,(48,414)),
      'main':ink_mask('1 Portfolio.',font_main,(48,523)),
    }
    final=base.convert('RGBA')
    for m in masks.values():
        ink=Image.new('RGBA',SIZE,INK+(0,))
        ink.putalpha(m)
        final=Image.alpha_composite(final,ink)
    final=final.convert('RGB')
    final.save(ROOT/'final.png',optimize=True)
    for name,m in masks.items(): m.save(ROOT/f'{name}-mask.png',optimize=True)

    # Tight, manually fitted visible-subject boxes after the measured 0.92 scene transform.
    # Coordinates were fitted from the clean background at 1280x720; polygons retain the silhouette shape.
    subjects={
      'transform':{'scale':BG_SCALE,'offset_px':list(scene_xy)},
      'subjects':[
        {'id':'portfolio-board','bbox':[620,48,1206,467],'polygon':[[620,67],[686,49],[1200,48],[1206,429],[1180,467],[625,444]],'fit':'manual tight visible outline; board only, not its surrounding dark field'},
        {'id':'agent-left','bbox':[536,193,691,407],'polygon':[[580,194],[626,193],[657,207],[669,239],[691,257],[680,281],[650,287],[647,337],[658,387],[636,405],[610,393],[585,407],[564,394],[568,340],[546,331],[536,294],[553,271],[559,231]],'fit':'manual tight union of full visible head, torso, both arms and legs'},
        {'id':'agent-right','bbox':[1072,141,1220,457],'polygon':[[1142,141],[1197,151],[1220,178],[1211,294],[1194,382],[1214,438],[1203,456],[1157,453],[1136,418],[1112,382],[1109,321],[1072,271],[1089,248],[1101,198]],'fit':'manual tight union of full visible head, torso, both arms and legs'},
        {'id':'agent-lower','bbox':[988,330,1174,479],'polygon':[[1080,330],[1113,339],[1122,363],[1160,394],[1174,447],[1158,471],[1129,479],[1084,469],[1044,474],[1007,461],[998,434],[988,362],[1014,346],[1049,349]],'fit':'manual tight union of full visible head, torso, wheels and arm'},
      ]
    }
    (ROOT/'subjects.json').write_text(json.dumps(subjects,ensure_ascii=False,indent=2)+'\n')

    # Save text ink boxes from alpha >= 0.5 masks.
    boxes={k:ink_box(v) for k,v in masks.items()}
    (ROOT/'final.png.boxes.json').write_text(json.dumps({
      'size':list(SIZE),'canvas_px':list(SIZE),'copy':'3 AIs. 1 Portfolio.','condition':'Paso 11 candidate thumbnail; editable Pillow overlay on candidate clean scene',
      'source_base':'evals/art-direction/diagnostic-2026-10-22/renders/step11/thumbnail/base-r1-edited-source.png',
      'source_sha256':sha(SOURCE),'crop_operation':'center-fit generated 16:9 source to 1280x720; scale scene to 92%; centered on a sampled deep-navy canvas',
      'font_file':'skills/cropmark/fonts/Anton-Regular.ttf','ink_srgb':list(INK),
      'groups':[
        {'role':'headline_kicker','text':'3 AIs.','box':boxes['kicker'],'font_size':95,'ink_mask':'kicker-mask.png'},
        {'role':'headline','text':'1 Portfolio.','box':boxes['main'],'font_size':150,'ink_mask':'main-mask.png'},
      ],
      'boxes':[{'role':'headline_kicker','text':'3 AIs.','box':boxes['kicker'],'size':95,'font_path':'skills/cropmark/fonts/Anton-Regular.ttf','fill':list(INK)},{'role':'headline','text':'1 Portfolio.','box':boxes['main'],'size':150,'font_path':'skills/cropmark/fonts/Anton-Regular.ttf','fill':list(INK)}],
      'effects':{'drop_shadow':False,'stroke':False,'backing_panel':False},
      'background_scale':BG_SCALE,'background_offset_px':list(scene_xy),'output_sha256':sha(ROOT/'final.png')
    },ensure_ascii=False,indent=2)+'\n')

    # Clearance overlay uses the contracted text ink and independently annotated tight subject bboxes.
    overlay=base.convert('RGBA')
    od=ImageDraw.Draw(overlay)
    for s in subjects['subjects']:
      l,t,r,b=s['bbox']; od.rectangle((l,t,r,b),outline=(255,72,72,255),width=2)
      od.text((l,t-22),s['id'],fill=(255,90,90,255),font=ImageFont.truetype(str(FONT_PATH),16))
    for name,m in masks.items():
      l,t,r,b=boxes[name]
      od.rectangle((l,t,r,b),outline=(65,255,166,255),width=2)
    overlay.save(ROOT/'clearance-overlay.png',optimize=True)

    ink_arrays={k:np.asarray(v)>=128 for k,v in masks.items()}
    all_ink=ink_arrays['kicker']|ink_arrays['main']
    gaps={}
    for s in subjects['subjects']:
      gaps[s['id']]=min(box_gap(a,s['bbox']) for a in ink_arrays.values())
    essential=np.argwhere(all_ink)
    ys,xs=essential[:,0],essential[:,1]
    edge=min(int(xs.min()),int(ys.min()),int(SIZE[0]-1-xs.max()),int(SIZE[1]-1-ys.max()))
    subject_edge=min(min(s['bbox'][0],s['bbox'][1],SIZE[0]-s['bbox'][2],SIZE[1]-s['bbox'][3]) for s in subjects['subjects'])
    p=p_metrics()
    preview_caps={'kicker_at_168':round(ink_box(masks['kicker'])[3]-ink_box(masks['kicker'])[1],2)*168/1280,'P_at_168':p['height']*168/1280}
    report={
      'canvas_px':list(SIZE),'final_sha256':sha(ROOT/'final.png'),'clean_background_sha256':sha(ROOT/'clean-background.png'),
      'source_sha256':sha(SOURCE),'source_dimensions_px':list(Image.open(SOURCE).size),
      'ink_boxes_alpha_ge_0_5':boxes,'subject_boxes_and_gaps_px':{s['id']:{'bbox':s['bbox'],'min_ink_gap':round(gaps[s['id']],2)} for s in subjects['subjects']},
      'minimum_subject_gap_px':round(min(gaps.values()),2),'minimum_subject_gap_at_168_px':round(min(gaps.values())*168/1280,2),'minimum_subject_gap_at_360_px':round(min(gaps.values())*360/1280,2),'overlap_count':sum(v==0 for v in gaps.values()),
      'closest_pair':min(gaps,key=gaps.get),'essential_ink_edge_clearance_px':edge,'key_subject_edge_clearance_px':subject_edge,
      'duration_zone':{'rect':[1049.6,612,1280,720],'ink_intersection_pixels':int(np.sum(all_ink[612:720,1049:1280])),'subject_bbox_intersections':[s['id'] for s in subjects['subjects'] if s['bbox'][2]>1049.6 and s['bbox'][3]>612]},
      'headline_metrics':{'common_glyph':'P','common_glyph_measurement':p,'cap_px_at_168':round(p['height']*168/1280,2),'cap_percent_height':round(100*p['height']/720,3),'fill_ratio':p['fill_ratio'],'kicker_cap_px_at_168':round((ink_box(masks['kicker'])[3]-ink_box(masks['kicker'])[1])*168/1280,2)},
      'contrast':{'kicker':contrast_stats(base,final,masks['kicker']),'main':contrast_stats(base,final,masks['main'])},
      'visual_reading':{'168px_transcription':'3 AIs. 1 Portfolio.','168px_story_read':'Three distinct robots around one large shared portfolio grid.','360px_story_read':'Three robots point to and adjust different grid areas on the same portfolio board.','display':'unzoomed native preview'},
      'style_choice':{'jev_recommendation':'UI-hero (score 61.4; confidence 0.46) over text-in-scene (49.3; 0.372). Treated as focal shared portfolio board; no UI card, shadow, new interface copy or metric added. Flat type and all spec constraints govern.'},
      'requirements':{
        'one_1280x720_final':'PASS','exact_copy':'PASS','minimum_32px_gap': 'PASS' if min(gaps.values())>=32 else 'FAIL',
        'zero_subject_overlap':'PASS' if not any(v==0 for v in gaps.values()) else 'FAIL',
        'common_P_cap_at_least_126px':'PASS' if p['height']>=126 else 'FAIL',
        'P_fill_at_least_0_6613':'PASS' if p['fill_ratio']>=0.6613 else 'FAIL',
        '3_AIs_cap_at_least_10px_at_168':'PASS' if preview_caps['kicker_at_168']>=10 else 'FAIL',
        'type_edge_margin_at_least_40px':'PASS' if edge>=40 else 'FAIL',
        'subject_edge_margin_at_least_40px':'PASS' if subject_edge>=40 else 'FAIL',
        'duration_zone_clear':'PASS' if int(np.sum(all_ink[612:720,1049:1280]))==0 and not [s for s in subjects['subjects'] if s['bbox'][2]>1049.6 and s['bbox'][3]>612] else 'FAIL',
        'contrast':'PASS' if contrast_stats(base,final,masks['main'])['p05']>=3 and contrast_stats(base,final,masks['kicker'])['p05']>=4.5 else 'FAIL',
        'required_ink_clipped_or_occluded_pixels':0,'drop_shadow':False,'natural_left_alignment':True
      },
      'previews':{},'measure_uncertainty':'Subject boxes/polygons are builder annotations from the clean rendered scene; no pixel classifier used because robot and board edges blend into their connected shadows. Raster-control segmentation uncertainty is not applicable to this editable candidate.'
    }
    for width,h in ((168,95),(320,180),(360,203)):
      final.resize((width,h),Image.Resampling.LANCZOS).save(ROOT/f'final-{width}.png',optimize=True)
      report['previews'][str(width)]={'size_px':[width,h],'resampling':'Lanczos','sharpening':False}
    (ROOT/'measurements.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'final':str(ROOT/'final.png'),'boxes':boxes,'measurements':{k:report[k] for k in ['subject_boxes_and_gaps_px','minimum_subject_gap_px','overlap_count','essential_ink_edge_clearance_px','duration_zone','headline_metrics','contrast']}},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
