from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np, cv2, hashlib, json, math
root=Path('evals/art-direction/diagnostic-2026-10-22/renders/step11')
out=root/'qa/independent'; out.mkdir(parents=True,exist_ok=True)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def lin(a):
 x=np.asarray(a,dtype=np.float32)/255
 return np.where(x<=0.04045,x/12.92,((x+0.055)/1.055)**2.4)
# Thumbnail: independently derive ink delta from pre-type scene, then annotate hand-fit subject envelopes.
thumb=np.array(Image.open(root/'thumbnail/final.png').convert('RGB'))
clean=np.array(Image.open(root/'thumbnail/clean-background.png').convert('RGB'))
delta=np.max(np.abs(thumb.astype(int)-clean.astype(int)),axis=2)
ink=(delta>=24).astype(np.uint8)*255
Image.fromarray(ink).save(out/'thumbnail-ink.png')
num,lab,stats,cent=cv2.connectedComponentsWithStats((ink>0).astype(np.uint8),8)
comps=[{'bbox_xywh':list(map(int,s[:4])),'area_px':int(s[4])} for s in stats[1:] if s[4]>6]
# P glyph is cropped independently from the second line; threshold mask gives its visible core.
pcrop=ink[520:680,90:230]
num2,l2,st2,_=cv2.connectedComponentsWithStats((pcrop>0).astype(np.uint8),8)
pcs=[s for s in st2[1:] if s[4]>12]
pcomp=max(pcs,key=lambda s:s[4]) if pcs else [0,0,0,0,0]
pbox=[int(pcomp[0]+90),int(pcomp[1]+520),int(pcomp[0]+pcomp[2]+90),int(pcomp[1]+pcomp[3]+520)]
pfill=float(pcomp[4]/max(1,pcomp[2]*pcomp[3]))
over=Image.fromarray(thumb).convert('RGBA'); d=ImageDraw.Draw(over)
subjects={'portfolio_board':[665,29,1228,426],'robot_left':[529,190,694,412],'robot_right':[1094,144,1214,465],'robot_low':[980,322,1159,478]}
for n,b in subjects.items(): d.rectangle(b,outline=(30,230,70,255),width=3); d.text((b[0],max(0,b[1]-19)),n,fill=(30,230,70,255))
for n,b in {'kicker':[48,412,256,500],'headline':[48,522,681,670]}.items(): d.rectangle(b,outline=(255,60,60,255),width=3); d.text((b[0],b[1]-19),n,fill=(255,60,60,255))
over.save(out/'thumbnail-annotated.png')
# Flyer: fit four visible sleeve corners from clean pixels by line response in edge ROIs (approximate segment endpoints shown).
fly=np.array(Image.open(root/'flyer/clean-source-crop.png').convert('RGB'))
corners={'TL':[37,230],'TR':[602,301],'BR':[611,845],'BL':[83,795]}
def dist(a,b): return math.dist(a,b)
L=dist(corners['TL'],corners['BL']); R=dist(corners['TR'],corners['BR'])
top=math.degrees(math.atan2(corners['TR'][1]-corners['TL'][1],corners['TR'][0]-corners['TL'][0]))
bottom=math.degrees(math.atan2(corners['BR'][1]-corners['BL'][1],corners['BR'][0]-corners['BL'][0]))
ratio=abs(L-R)/max(L,R)
fo=Image.fromarray(np.array(Image.open(root/'flyer/final.png').convert('RGB'))).convert('RGBA'); fd=ImageDraw.Draw(fo)
pts=[tuple(corners[k]) for k in ['TL','TR','BR','BL']]
fd.line(pts+[pts[0]],fill=(30,230,70,255),width=4)
for name,(x,y) in corners.items(): fd.ellipse((x-6,y-6,x+6,y+6),fill=(255,30,30,255)); fd.text((x+8,y-16),name,fill=(255,30,30,255))
fo.save(out/'flyer-annotated.png')
# Carousel independent 20x25 emptiness using manually traced key subjects and manually transcribed text rectangles.
# All polygons are 360-feed coordinates; text boxes are actual visible-copy extents, expanded 8px by the grid code.
polys=[
 [(220,100),(286,106),(313,168),(347,182),(353,303),(317,327),(246,312),(217,278),(203,205)],
 [(132,176),(275,174),(354,284),(356,369),(273,355),(168,329),(126,282)],
 [(188,314),(360,309),(360,450),(202,450),(176,405)]
]
# separate subject shapes, avoiding whole-photo labeling; polygons include working hands, clay, vessel / trace.
textboxes=[
 [[22,17,176,64],[22,76,218,157],[22,174,224,222]],
 [[22,17,176,64],[22,258,226,338],[22,364,230,420]],
 [[22,17,176,64],[22,76,218,157],[22,174,223,222],[22,395,192,423]]
]
carousel=[]
for i in range(1,4):
 im=Image.open(root/f'carousel/final-{i}-360.png').convert('RGB'); a=np.asarray(im); mask=np.zeros((450,360),np.uint8)
 cv2.fillPoly(mask,[np.array(polys[i-1],np.int32)],1)
 for b in textboxes[i-1]:
  x1,y1,x2,y2=b; cv2.rectangle(mask,(max(0,x1-8),max(0,y1-8)),(min(359,x2+8),min(449,y2+8)),1,-1)
 # explicit grid per spec; outside masks >=90% plus low linear-luminance std <=.025
 lg=lin(a); lum=0.2126*lg[:,:,0]+0.7152*lg[:,:,1]+0.0722*lg[:,:,2]
 grid=np.zeros((25,20),np.uint8)
 for gy in range(25):
  for gx in range(20):
   x,y=gx*18,gy*18; m=mask[y:y+18,x:x+18]; l=lum[y:y+18,x:x+18]
   outside=(m==0).mean()
   grid[gy,gx]=int(outside>=.90 and float(l.std())<=.025)
 count=int(grid.sum()); nlab,labels,st,_=cv2.connectedComponentsWithStats(grid,4)
 largest=int(st[1:,cv2.CC_STAT_AREA].max()) if nlab>1 else 0
 cv2.imwrite(str(out/f'carousel-slide-{i}-subject-text-mask.png'),mask*255)
 # visual grid overlay, green empty cells, magenta subject mask outline
 ov=im.convert('RGBA'); dr=ImageDraw.Draw(ov)
 for gy in range(25):
  for gx in range(20):
   x,y=gx*18,gy*18
   if grid[gy,gx]: dr.rectangle((x,y,x+17,y+17),outline=(20,240,70,190),width=1)
   else: dr.rectangle((x,y,x+17,y+17),outline=(80,80,80,60),width=1)
 ov.save(out/f'carousel-slide-{i}-grid-annotated.png')
 carousel.append({'slide':i,'preview_px':[360,450],'empty_cells':count,'empty_percent':round(count/5,1),'largest_4_connected_empty_component_cells':largest,'largest_component_percent':round(largest/5,1),'thresholds_percent':{'empty_cells_max':35,'largest_component_max':20},'subject_polygon_preview_px':polys[i-1],'text_group_rectangles_preview_px_before_8px_expansion':textboxes[i-1],'segmentation_note':'Manual tight subject polygons and visible-copy boxes; no full-photo occupancy labeling.'})
# outputs
thumb_json={'file':'thumbnail/final.png','sha256':sha(root/'thumbnail/final.png'),'canvas_px':[1280,720],'ink_delta_threshold_rgb_max':24,'ink_bbox_components':comps,'P_crop_xyxy':[90,520,230,680],'P_visible_bbox_xyxy':pbox,'P_ink_fill':round(pfill,4),'subject_boxes_xyxy':subjects,'headline_boxes_xyxy':{'kicker':[48,412,256,500],'main':[48,522,681,670]},'gap_estimates_px':{'portfolio_board':100,'left_robot':110,'right_robot':374,'low_robot':300},'minimum_gap_px_estimate':100,'overlap_count':0,'edge_clearance_px_min_estimate':48,'duration_zone_intersections':0,'readability_visual':{'168':'3 AIs. 1 Portfolio.; three interacting robots and one shared board identifiable, redesign activity recognizable at small but visible thumbnail scale','320':'exact phrase readable','360':'exact phrase readable'},'pass_checks':{'canvas_copy':True,'min_subject_gap_ge32':True,'zero_overlap':True,'edges_ge40':True,'duration_zone_zero':True,'common_P_cap_ge126':'see caveat below','P_fill_ge0.6613':pfill>=0.6613,'kicker_cap_ge10_at_168':'visual estimated 10 px'},'measurement_limit':'subject boxes are fresh hand-fitted visible bboxes; P selection includes connected diff component in a manual crop and may not isolate the P glyph because adjacent glyph pixels touch; cap result is not certified.'}
(out/'thumbnail.json').write_text(json.dumps(thumb_json,ensure_ascii=False,indent=2)+'\n')
flyjson={'file':'flyer/final.png','sha256':sha(root/'flyer/final.png'),'canvas_px':[1080,1350],'independent_clean_source':'flyer/clean-source-crop.png','corners_TL_TR_BR_BL_px':corners,'edge_lengths_L_R_px':[round(L,1),round(R,1)],'top_bottom_edge_angles_degrees':[round(top,2),round(bottom,2)],'keystone_ratio':round(ratio,4),'baseline_fits_and_rectified_residual':'not independently resolved to 1 degree / 3 px; full independent line-baseline fit needed','corner_residual_against_builder':'not reported as independent numeric because my fit is manual and uncertainty is approximately 3 px','insets':'visual estimate; title and metadata are close to sleeve left/top edges, no measured plane-coordinate proof of 5%','content_visual':'Noche de / Vinilos; Sala Taller · 14 nov · 21:00; 2 separators, none leading/trailing; grooves/platter/tonearm visible','title_cap_at_360':'visual pass approx 34 px','metadata_cap_at_360':'visual borderline approx 13 px; requirement 14 px not demonstrated','conservative_ratio':'not independently measured','material':'appears pigment-like with grain visible; paired crops present at 100%','technical_status':'FAIL: required projected cap/inset/baseline residual and P05 glyph-core contrast were not independently established; no technical PASS inferred from producer report'}
(out/'flyer.json').write_text(json.dumps(flyjson,ensure_ascii=False,indent=2)+'\n')
carjson={'slides':carousel,'photo_coverage':{'1':100,'2':100,'3':100},'photo_edges_reached':{'1':['top','right','bottom','left'],'2':['top','right','bottom','left'],'3':['top','right','bottom','left']},'closing_subject_bbox_preview_px':[176,132,360,450],'closing_subject_bbox_area_percent_estimate':round((184*318)/(360*450)*100,1),'trace_diameter_px_360_estimate':25,'trace_diameter_px_master_estimate':75,'cta_pixels':[0,0,1],'removed_strings_pixel_count':{'EXPLORA EL TALLER':0,'SIGUE EL PROCESO':0},'cta_style':'one unboxed final CTA with underline; slides 1 and 2 have no apparent action','relationships':['slide 1 cream headline on teal negative field with active hand/pot on right','slide 2 dark headline crosses teal/table transition adjacent to wheel, low contrast','slide 3 cream headline relates to large vessel/trace area on right'],'caps':'visual check: headline and support readable except slide 2 first line low contrast; numerical glyph-core caps not certified','safe_edges':'pixel review indicates text/group inset >=64 master for headline groups; CTA bottom inset approx 72px master, pass visually; other key-detail 24px clearance not fully certified','technical_status':'FAIL: slide 2 dark headline P05 contrast/readability unresolved; empty-grid/manual estimates below thresholds where measured; trace estimate 75px master <90'}
(out/'carousel.json').write_text(json.dumps(carjson,ensure_ascii=False,indent=2)+'\n')
print('thumbnail',json.dumps(thumb_json,ensure_ascii=False))
print('flyer',json.dumps(flyjson,ensure_ascii=False))
print('carousel',json.dumps(carousel,ensure_ascii=False))
