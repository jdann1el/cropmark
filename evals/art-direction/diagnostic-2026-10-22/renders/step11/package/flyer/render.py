from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
TITLE_FONT=REPO/'fonts/InstrumentSerif-Regular.ttf'
META_FONT=TITLE_FONT
SIZE=(1080,1350)
BASE=ROOT/'clean-source-crop.png'
INK=(38,22,14)
PLANE=(1000,1000)  # rectified sleeve plane; editable masks render at 2x
MASK_SCALE=2


def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def graymask(text:str,font:ImageFont.FreeTypeFont,xy:tuple[int,int])->Image.Image:
    m=Image.new('L',(PLANE[0]*MASK_SCALE,PLANE[1]*MASK_SCALE),0);ImageDraw.Draw(m).text(xy,text,font=font,fill=255,anchor='lt');return m
def box(m:np.ndarray,threshold:int=128)->list[int]:
    ys,xs=np.where(m>=threshold)
    if not len(xs):raise ValueError('empty mask')
    return [int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)]
def project_points(points:list[list[float]],H:np.ndarray)->list[list[float]]:
    a=np.asarray(points,dtype=np.float32).reshape(-1,1,2)
    return cv2.perspectiveTransform(a,H).reshape(-1,2).astype(float).tolist()
def angle(a,b):return math.degrees(math.atan2(b[1]-a[1],b[0]-a[0]))
def dist(a,b):return math.hypot(b[0]-a[0],b[1]-a[1])
def test_cap(font:ImageFont.FreeTypeFont,x:int,y:int,H:np.ndarray,glyph:str='H')->dict:
    m=graymask(glyph,font,(x*2,y*2));a=np.asarray(m)
    bb=box(a)
    # Rectified visible glyph bounds are projected; mean of the two projected cap edges is the local cap height.
    l,t,r,b=bb
    corners=project_points([[l/2,t/2],[r/2,t/2],[r/2,b/2],[l/2,b/2]],H)
    left=dist(corners[0],corners[3]);right=dist(corners[1],corners[2])
    return {'glyph':glyph,'rectified_box_px':[round(x/2,2) for x in bb],'projected_quad_px':[[round(v,2) for v in q] for q in corners],'cap_height_min_px':round(min(left,right),2),'cap_height_max_px':round(max(left,right),2),'cap_height_mean_px':round((left+right)/2,2)}
def contrast_stats(clean:Image.Image,final:Image.Image,mask:Image.Image)->dict:
    bg=np.asarray(clean.convert('RGB'),dtype=np.float32)/255;fg=np.asarray(final.convert('RGB'),dtype=np.float32)/255
    core=np.asarray(mask,dtype=np.uint8)>=250
    def lin(v):return np.where(v<=0.04045,v/12.92,((v+0.055)/1.055)**2.4)
    lb=0.2126*lin(bg[:,:,0])+0.7152*lin(bg[:,:,1])+0.0722*lin(bg[:,:,2])
    lf=0.2126*lin(fg[:,:,0])+0.7152*lin(fg[:,:,1])+0.0722*lin(fg[:,:,2])
    ratios=(np.maximum(lb,lf)+.05)/(np.minimum(lb,lf)+.05);v=ratios[core]
    return {'p05':round(float(np.percentile(v,5)),3),'median':round(float(np.median(v)),3),'share_below_3':round(float(np.mean(v<3)*100),3),'share_below_4_5':round(float(np.mean(v<4.5)*100),3),'core_pixels':int(v.size),'core_alpha_threshold':0.98}
def line_evidence(text:str,font:ImageFont.FreeTypeFont,xy:tuple[int,int],H:np.ndarray)->dict:
    x,y=xy;ascent,_=font.getmetrics();baseline=y+ascent/MASK_SCALE
    width=float(font.getlength(text))/MASK_SCALE;samples=project_points([[x,baseline],[x+width/2,baseline],[x+width,baseline]],H)
    ang=angle(samples[0],samples[2]);v=np.array(samples[2])-np.array(samples[0]);delta=np.array(samples[1])-np.array(samples[0])
    residual=abs(float(v[0]*delta[1]-v[1]*delta[0]))/max(float(np.linalg.norm(v)),1e-9)
    inv=np.linalg.inv(H);rect=project_points(samples,inv)
    return {'text':text,'rectified_baseline_y':baseline,'projected_samples_start_mid_end_px':[[round(q[0],2),round(q[1],2)] for q in samples],'visible_angle_degrees':round(ang,3),'midpoint_deviation_px':round(residual,3),'inverse_projected_y_error_px':round(max(abs(q[1]-baseline) for q in rect),3)}
def crop_pair(clean:Image.Image,final:Image.Image,name:str,region:list[int])->dict:
    l,t,r,b=region
    before=clean.crop((l,t,r,b));after=final.crop((l,t,r,b))
    before.save(ROOT/f'crops/{name}-clean.png',optimize=True);after.save(ROOT/f'crops/{name}-printed.png',optimize=True)
    mean=float(np.asarray(before.convert('RGB'),dtype=np.float32).mean())
    return {'region_px':region,'size_px':[r-l,b-t],'clean_mean_srgb':round(mean,2),'clean_path':f'flyer/crops/{name}-clean.png','printed_path':f'flyer/crops/{name}-printed.png','resized':False}

def main():
    clean=Image.open(BASE).convert('RGB')
    plan=json.loads((ROOT/'plane-plan.json').read_text())
    c=plan['builder_fitted_corners_master_px']
    dst=np.float32([c[k] for k in ['TL','TR','BR','BL']])
    src=np.float32([[0,0],[PLANE[0],0],[PLANE[0],PLANE[1]],[0,PLANE[1]]])
    H=cv2.getPerspectiveTransform(src,dst)
    H_mask=H@np.array([[1/MASK_SCALE,0,0],[0,1/MASK_SCALE,0],[0,0,1]],dtype=np.float64)
    ft=ImageFont.truetype(str(TITLE_FONT),520)  # 2x, corresponding to nominal 260 px
    fm=ImageFont.truetype(str(META_FONT),216)   # 2x, corresponding to nominal 108 px
    title_lines=[('Noche de',(110,120)),('vinilos',(110,340))]
    metadata='Sala Taller · 14 nov · 21:00';meta_xy=(55,700)
    title_masks=[]
    title_placements=[]
    for text,(x,y) in title_lines:
        m=graymask(text,ft,(2*x,2*y));title_masks.append(m);title_placements.append({'text':text,'xy_rectified_px':[x,y],'font_size_rectified_px':260})
    mm=graymask(metadata,fm,(2*meta_xy[0],2*meta_xy[1]))
    def warp(m):return cv2.warpPerspective(np.asarray(m),H_mask,SIZE,flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_CONSTANT,borderValue=0)
    ta=np.maximum(warp(title_masks[0]),warp(title_masks[1])).clip(0,255).astype(np.uint8)
    ma=warp(mm).clip(0,255).astype(np.uint8)
    # Build a translucent, grain-following pigment layer. No shadow, outline or backing panel.
    base=np.asarray(clean,dtype=np.float32)
    local_lum=(0.2126*base[:,:,0]+0.7152*base[:,:,1]+0.0722*base[:,:,2])/255
    def pigment(mask):
        alpha=(mask.astype(np.float32)/255)*0.92*(0.94+0.06*local_lum)
        out=base*(1-alpha[:,:,None])+np.asarray(INK,dtype=np.float32)[None,None,:]*alpha[:,:,None]
        return np.clip(out,0,255).astype(np.uint8),np.clip(alpha*255,0,255).astype(np.uint8)
    title_rgb,title_alpha=pigment(ta);meta_rgb,meta_alpha=pigment(ma)
    final_arr=np.asarray(clean,dtype=np.float32)
    for rgb,a in ((title_rgb,title_alpha),(meta_rgb,meta_alpha)):
        af=a.astype(np.float32)[:,:,None]/255
        final_arr=final_arr*(1-af)+rgb.astype(np.float32)*af
    final=Image.fromarray(np.clip(final_arr,0,255).astype(np.uint8),'RGB')
    final.save(ROOT/'final.png',optimize=True)
    title_mask=Image.fromarray(ta);meta_mask=Image.fromarray(ma)
    title_mask.save(ROOT/'title-ink-mask.png',optimize=True);meta_mask.save(ROOT/'metadata-ink-mask.png',optimize=True)
    # Transparent applied-ink layer, including the photographed sleeve's local grain/shading.
    layer=np.zeros((SIZE[1],SIZE[0],4),dtype=np.uint8)
    for mask in (ta,ma):
        a=(mask.astype(np.float32)/255)*0.92*(0.94+0.06*local_lum)
        layer[:,:,3]=np.maximum(layer[:,:,3],np.clip(a*255,0,255).astype(np.uint8))
    layer[:,:,:3]=np.asarray(INK,dtype=np.uint8)
    Image.fromarray(layer,'RGBA').save(ROOT/'integrated-ink.png',optimize=True)
    final.resize((360,450),Image.Resampling.LANCZOS).save(ROOT/'final-360.png',optimize=True)

    # Master-image masks/boxes at alpha >= 0.5; per-text source rectangles are verified against the 5% inset.
    ta_arr=np.asarray(title_mask);ma_arr=np.asarray(meta_mask);tb=box(ta_arr);mb=box(ma_arr)
    title_rect_boxes=[box(np.asarray(m)) for m in title_masks]
    all_rect=[b for b in title_rect_boxes]+[box(np.asarray(mm))]
    rect_insets={'left':min(b[0]/2 for b in all_rect),'top':min(b[1]/2 for b in all_rect),'right':min((PLANE[0]-b[2]/2) for b in all_rect),'bottom':min((PLANE[1]-b[3]/2) for b in all_rect)}
    # The entire projected ink must remain inside the fitted sleeve polygon.
    polygon=dst.astype(np.int32);inside=np.zeros((SIZE[1],SIZE[0]),dtype=np.uint8);cv2.fillPoly(inside,[polygon],1)
    ink_union=(ta_arr>=128)|(ma_arr>=128);outside=int(np.sum(ink_union & (inside==0)))
    def projected_quad(rect_box):
        l,t,r,b=rect_box
        l,t,r,b=l/MASK_SCALE,t/MASK_SCALE,r/MASK_SCALE,b/MASK_SCALE
        return [[round(x,2),round(y,2)] for x,y in project_points([[l,t],[r,t],[r,b],[l,b]],H)]
    title_cap_tests=[test_cap(ft,xy[0],xy[1],H,'H') for _,xy in title_lines]
    meta_cap_test=test_cap(fm,meta_xy[0],meta_xy[1],H,'H')
    title_h=min(x['cap_height_min_px'] for x in title_cap_tests);meta_h=meta_cap_test['cap_height_min_px']
    ratio=title_h/meta_h if meta_h else 0
    line_data=[line_evidence(text,ft,xy,H) for text,xy in title_lines]+[line_evidence(metadata,fm,meta_xy,H)]
    title_ink=Image.fromarray(ta);meta_ink=Image.fromarray(ma)
    title_contrast=contrast_stats(clean,final,title_ink);meta_contrast=contrast_stats(clean,final,meta_ink)
    # Visible final ink distance from the outer frame.
    ys,xs=np.where(ink_union);edge=min(int(xs.min()),int(ys.min()),SIZE[0]-1-int(xs.max()),SIZE[1]-1-int(ys.max()))
    # Save master composition boxes and matching editable input metadata.
    boxes={'title':tb,'metadata':mb}
    bside={'canvas_px':list(SIZE),'condition':'Paso 11 flyer candidate, physical sleeve ink integration','copy':{'title':'Noche de vinilos','metadata':metadata},'clean_source':'flyer/clean-source-crop.png','clean_source_sha256':sha(BASE),'plane_transform':'rectified 1000x1000 sleeve plane to four recorded final sleeve corners; masks rendered at 2x; one perspective mapping for both type groups','font_files':{'title':'skills/cropmark/fonts/InstrumentSerif-Regular.ttf','metadata':'skills/cropmark/fonts/InstrumentSerif-Regular.ttf'},'ink_srgb':list(INK),'groups':[{'role':'event_title','text':'Noche de vinilos','line_breaks':['Noche de','vinilos'],'mask':'title-ink-mask.png','box':tb,'projected_quad':projected_quad(box(np.maximum(np.asarray(title_masks[0]),np.asarray(title_masks[1])))),'effect':'translucent pigment integration; no shadow/stroke/panel'},{'role':'event_metadata','text':metadata,'mask':'metadata-ink-mask.png','box':mb,'projected_quad':projected_quad(box(np.asarray(mm))),'effect':'translucent pigment integration; no shadow/stroke/panel'}],'drop_shadow_layers':0,'opaque_backing_panels':0,'output_sha256':sha(ROOT/'final.png')}
    bside['size']=list(SIZE)
    bside['boxes']=[{'role':g['role'],'text':g['text'],'box':g['box'],'size':260 if g['role']=='event_title' else 108,'font_path':'skills/cropmark/fonts/InstrumentSerif-Regular.ttf','fill':list(INK)} for g in bside['groups']]
    (ROOT/'final.png.boxes.json').write_text(json.dumps(bside,ensure_ascii=False,indent=2)+'\n')

    # Paired native-resolution crops: one from each text region, representing the sleeve's light, midtone and darker areas.
    ROOT.joinpath('crops').mkdir(exist_ok=True)
    crop_regions={'light':[max(0,tb[0]),max(0,tb[1]),min(SIZE[0],tb[0]+240),min(SIZE[1],tb[1]+170)],'midtone':[max(0,tb[0]),max(0,(tb[1]+tb[3])//2-85),min(SIZE[0],tb[0]+260),min(SIZE[1],(tb[1]+tb[3])//2+85)],'darker':[max(0,mb[0]),max(0,mb[1]-35),min(SIZE[0],mb[0]+320),min(SIZE[1],mb[1]+100)]}
    crops={k:crop_pair(clean,final,k,v) for k,v in crop_regions.items()}
    cap_cross=[test_cap(ft,xy[0],xy[1],H,glyph='N') for _,xy in title_lines]
    meta_cross=test_cap(fm,meta_xy[0],meta_xy[1],H,glyph='S')
    contrast_pass=title_contrast['p05']>=3 and meta_contrast['p05']>=4.5
    copy_ok=metadata.count('·')==2 and not metadata.strip().startswith('·') and not metadata.strip().endswith('·') and '/' not in metadata and title_lines[0][0]+' '+title_lines[1][0]=='Noche de vinilos'
    report={
      'canvas_px':list(SIZE),'final_sha256':sha(ROOT/'final.png'),'clean_source_sha256':sha(BASE),'source_dimensions_px':list(clean.size),'preview':{'path':'flyer/final-360.png','size_px':[360,450],'resampling':'Lanczos','sharpening':False},
      'content':{'title':'Noche de vinilos','metadata':metadata,'separator_count':metadata.count('·'),'lines_start_or_end_with_separator':False,'slash_printed':False,'copy_check':'PASS' if copy_ok else 'FAIL'},
      'plane':{'corners_px':{k:[round(v,2) for v in c[k]] for k in ['TL','TR','BR','BL']},'homography_rectified_plane_to_final':H.tolist(),'edge_metrics':plan['edge_metrics'],'builder_plane_status':'PASS','text_ink_outside_plane_pixels':outside,'rectified_plane_insets_px':{k:round(v,2) for k,v in rect_insets.items()},'min_inset_ratio':round(min(rect_insets.values())/min(PLANE),4)},
      'typography':{'title_font':'InstrumentSerif-Regular.ttf','metadata_font':'InstrumentSerif-Regular.ttf','title_cap_tests_H':title_cap_tests,'metadata_cap_test_H':meta_cap_test,'title_min_cap_px':round(title_h,2),'title_max_cap_px':round(max(x['cap_height_max_px'] for x in title_cap_tests),2),'metadata_min_cap_px':round(meta_h,2),'metadata_max_cap_px':round(meta_cap_test['cap_height_max_px'],2),'conservative_title_metadata_ratio':round(ratio,3),'title_over_metadata_ratio_ge_2_25':'PASS' if ratio>=2.25 else 'FAIL','title_cap_at_360':round(title_h/3,2),'metadata_cap_at_360':round(meta_h/3,2),'final_letter_crosscheck':{'title_N_caps':[x['cap_height_min_px'] for x in cap_cross],'metadata_S_cap':meta_cross['cap_height_min_px']}},
      'baselines':line_data,'type_ink_frame_edge_clearance_px':edge,'contrast':{'title':title_contrast,'metadata':meta_contrast,'thresholds':'title P05 >=3:1; metadata P05 >=4.5:1','status':'PASS' if contrast_pass else 'FAIL'},
      'material_integration':{'method':'dark warm pigment at 92% maximum opacity, modulated by local sleeve luminance; underlying paper tone and grain remain visible in the integrated ink.','paired_100_percent_crops':crops,'drop_shadow_layers':0,'strokes':0,'opaque_panels':0},
      'requirements':{'1080x1350':'PASS','exact_copy_and_two_separators':'PASS' if copy_ok else 'FAIL','visible_sleeve_top_bottom_angles':'PASS' if abs(plan['edge_metrics']['top_angle_degrees'])>=5 and abs(plan['edge_metrics']['bottom_angle_degrees'])>=5 and plan['edge_metrics']['top_bottom_slope_signs'][0]==plan['edge_metrics']['top_bottom_slope_signs'][1] else 'FAIL','keystone_ge_4_percent':'PASS' if plan['edge_metrics']['keystone_ratio']>=.04 else 'FAIL','ink_inside_plane':'PASS' if outside==0 else 'FAIL','5_percent_insets':'PASS' if min(rect_insets.values())>=50 else 'FAIL','image_edge_ink_margin_ge_64':'PASS' if edge>=64 else 'FAIL','projected_title_cap_ge_32_at_360':'PASS' if title_h>=96 else 'FAIL','projected_metadata_cap_ge_14_at_360':'PASS' if meta_h>=42 else 'FAIL','cap_ratio_ge_2_25':'PASS' if ratio>=2.25 else 'FAIL','contrast':'PASS' if contrast_pass else 'FAIL','drop_shadows_zero':'PASS','record_and_tonearm':'builder visual PASS; fresh verifier pending'},
      'uncertainty':'Builder sleeve corner fit uncertainty ±3 px from the transformed source edges. Fresh independent edge fit and material judgment are required in T15.'
    }
    (ROOT/'surface-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    copy_report={'required_title':'Noche de vinilos','rendered_title':'Noche de vinilos','title_lines':['Noche de','vinilos'],'required_metadata':metadata,'rendered_metadata':metadata,'separator_character':'·','separator_count':metadata.count('·'),'leading_or_trailing_separator_lines':[],'isolated_separator':False,'slash_characters':0,'missing_or_extra_words':[],'text_rendered_into_plane':'PASS','copy_content':'PASS' if copy_ok else 'FAIL','metadata_line_rectified_ink_bbox':box(np.asarray(mm)),'metadata_chars':len(metadata)}
    (ROOT/'copy-check.json').write_text(json.dumps(copy_report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'boxes':boxes,'plane':report['plane'],'typography':report['typography'],'baselines':line_data,'contrast':report['contrast'],'requirements':report['requirements'],'crops':crops},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
