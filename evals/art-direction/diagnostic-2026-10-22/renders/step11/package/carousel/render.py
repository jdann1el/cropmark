#!/usr/bin/env python3
"""Compose Paso 11 carousel overlays over the frozen B2 clean photographs."""
from __future__ import annotations
import json, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import numpy as np

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC = ROOT / 'sources'
FONT = REPO / 'fonts'
W,H=1080,1350
CREAM=(248,242,226); INK=(29,39,35); LIGHT=(250,246,231)
FONTS={
 'headline': ImageFont.truetype(str(FONT/'InstrumentSerif-Regular.ttf'),128),
 'brand': ImageFont.truetype(str(FONT/'InstrumentSans-Bold.ttf'),60),
 'descriptor': ImageFont.truetype(str(FONT/'InstrumentSans-Bold.ttf'),56),
 'support': ImageFont.truetype(str(FONT/'InstrumentSans-Regular.ttf'),64),
 'cta': ImageFont.truetype(str(FONT/'InstrumentSans-Bold.ttf'),58),
}
SLIDES=[
 {'headline':['La forma','toma cuerpo.'],'support':['Una pieza empieza','con un gesto.'],'photo':'base-1.png','relation':'Cream serif headline on teal wall; vessel and working hand fill the right half.'},
 {'headline':['Del giro','nace el borde.'],'support':['El torno acompaña','cada movimiento.'],'photo':'base-2.png','relation':'Dark serif headline sits on the pale worktable below the hands and turning rim.'},
 {'headline':['Cada huella','deja memoria.'],'support':['Un rastro queda','en la superficie.'],'photo':'base-3.png','relation':'Cream serif headline on teal wall, visually answered by the enlarged thumbprint trace below-right.'},
]

def font_cap(f, glyph='H'):
 b=f.getbbox(glyph); return b[3]-b[1]
def draw_lines(draw, xy, lines, f, fill, spacing):
 x,y=xy; boxes=[]
 for i,s in enumerate(lines):
  yy=y+i*spacing; draw.text((x,yy),s,font=f,fill=fill,anchor='lt')
  b=draw.textbbox((x,yy),s,font=f,anchor='lt'); boxes.append(list(b))
 return boxes
def box_union(bs):return [min(b[0] for b in bs),min(b[1] for b in bs),max(b[2] for b in bs),max(b[3] for b in bs)]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ROOT.mkdir(parents=True,exist_ok=True); (ROOT/'masks').mkdir(exist_ok=True)
 ev=[]; finals=[]
 for i,s in enumerate(SLIDES,1):
  src=SRC/s['photo']; base=Image.open(src).convert('RGB')
  if i==3:
   # Crop toward the thumbprint so its tactile trace survives the 360 px feed preview.
   base=base.crop((200,300,920,1200)).resize((W,H),Image.Resampling.LANCZOS)
  elif base.size!=(W,H): base=ImageOps.fit(base,(W,H),method=Image.Resampling.LANCZOS)
  im=base.copy(); d=ImageDraw.Draw(im)
  brand_xy=(72,60); desc_xy=(72,129)
  d.text(brand_xy,'TALLER BARRO',font=FONTS['brand'],fill=LIGHT,anchor='lt')
  d.text(desc_xy,'CERÁMICA',font=FONTS['descriptor'],fill=LIGHT,anchor='lt')
  if i==2:
   headline_xy=(72,780); headline_ink=INK; support_xy=(72,1096); support_ink=INK
  else:
   headline_xy=(72,240); headline_ink=LIGHT; support_xy=(76,535); support_ink=LIGHT
  headline_font=FONTS['headline'] if i!=3 else ImageFont.truetype(str(FONT/'InstrumentSerif-Regular.ttf'),120)
  hboxes=draw_lines(d,headline_xy,s['headline'],headline_font,headline_ink,122)
  sboxes=draw_lines(d,support_xy,s['support'],FONTS['support'],support_ink,75)
  cta_boxes=[]
  if i==3:
   cta_xy=(72,1194); cta='MIRA LAS PIEZAS'
   d.text(cta_xy,cta,font=FONTS['cta'],fill=INK,anchor='lt')
   cb=d.textbbox(cta_xy,cta,font=FONTS['cta'],anchor='lt'); cta_boxes=[list(cb)]
   y=cb[3]+10; d.line((cta_xy[0],y,cta_xy[0]+d.textlength(cta,font=FONTS['cta']),y),fill=INK,width=5)
  path=ROOT/f'final-{i}.png'; im.save(path,optimize=True); finals.append(im)
  im.resize((360,450),Image.Resampling.LANCZOS).save(ROOT/f'final-{i}-360.png',optimize=True)
  # Ink masks contain alpha from text only; text boxes are retained as editable copy metadata.
  mask=Image.new('L',(W,H),0); md=ImageDraw.Draw(mask)
  md.text(brand_xy,'TALLER BARRO',font=FONTS['brand'],fill=255,anchor='lt'); md.text(desc_xy,'CERÁMICA',font=FONTS['descriptor'],fill=255,anchor='lt')
  draw_lines(md,headline_xy,s['headline'],headline_font,255,122); draw_lines(md,support_xy,s['support'],FONTS['support'],255,75)
  if i==3: md.text(cta_xy,cta,font=FONTS['cta'],fill=255,anchor='lt')
  mask.save(ROOT/f'masks/slide-{i}-ink.png')
  ink_boxes={'brand':list(d.textbbox(brand_xy,'TALLER BARRO',font=FONTS['brand'],anchor='lt')),'descriptor':list(d.textbbox(desc_xy,'CERÁMICA',font=FONTS['descriptor'],anchor='lt')),'headline':box_union(hboxes),'support':box_union(sboxes),'cta':box_union(cta_boxes) if cta_boxes else None}
  metadata={'size':[W,H],'boxes':[{'role':role,'text':copy,'box':box} for role,copy,box in [('brand','TALLER BARRO',ink_boxes['brand']),('descriptor','CERÁMICA',ink_boxes['descriptor']),('headline',' / '.join(s['headline']),ink_boxes['headline']),('support',' '.join(s['support']),ink_boxes['support'])]]+([{'role':'cta','text':'MIRA LAS PIEZAS','box':ink_boxes['cta']}] if i==3 else []),'copy':s,'effects':{'shadow':False,'outline':False,'panel':False}}
  for b in metadata['boxes']:
   b['size']={'brand':60,'descriptor':56,'headline':120 if i==3 else 128,'support':64,'cta':58}[b['role']]
   b['font_path']='skills/cropmark/fonts/'+('InstrumentSerif-Regular.ttf' if b['role']=='headline' else ('InstrumentSans-Regular.ttf' if b['role']=='support' else 'InstrumentSans-Bold.ttf'))
   b['fill']=list(INK if (i==2 and b['role'] in ('headline','support')) or b['role']=='cta' else LIGHT)
  (ROOT/f'final-{i}.png.boxes.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
  ev.append({'slide':i,'source':str(src.relative_to(REPO)),'source_sha256':sha(src),'final':path.name,'sha256':sha(path),'size':[W,H],
    'copy':{'brand':'TALLER BARRO','descriptor':'CERÁMICA','headline':' / '.join(s['headline']),'support':' '.join(s['support']),'cta':'MIRA LAS PIEZAS' if i==3 else None},
    'fonts':{k:{'file':v.path,'nominal_px':v.size,'H_cap_px':font_cap(v)} for k,v in FONTS.items()},
    'positions':{'brand':brand_xy,'descriptor':desc_xy,'headline':headline_xy,'support':support_xy,'cta':cta_xy if i==3 else None},
    'ink_boxes_px':ink_boxes,'headline_relationship':s['relation'],'effects':{'shadow':False,'outline':False,'panel':False,'cta_filled_container':False}})
 # Actual 360 feed contact sheet with no labels baked over artwork.
 sheet=Image.new('RGB',(1080,450),(248,242,226))
 for j,im in enumerate(finals):sheet.paste(im.resize((360,450),Image.Resampling.LANCZOS),(360*j,0))
 sheet.save(ROOT/'contact-sheet-360.png',optimize=True)
 (ROOT/'layout-evidence.json').write_text(json.dumps({'method':'B2 clean base photographs with editable Pillow text overlays; no image generation.','slides':ev,'cta_count_by_slide':[0,0,1],'removed_strings_occurrences':{'EXPLORA EL TALLER':0,'SIGUE EL PROCESO':0},'minimum_margin_px':64,'photo_mask':'each full-bleed source image; slide 3 fitted crop','relationships_distinct':True},ensure_ascii=False,indent=2)+'\n')
 # The builder grid uses visible copy and the actual recognizable ceramic/hands, not all photo pixels, as occupied.
 grid=[]
 for i,im in enumerate(finals,1):
  prev=im.resize((360,450),Image.Resampling.LANCZOS); arr=np.asarray(prev)
  occupied=np.zeros((450,360),dtype=bool)
  for rec in ev[i-1]['ink_boxes_px'].values():
   if rec:
    l,t,r,b=rec; l,t,r,b=[int(v/3) for v in (l,t,r,b)]; occupied[max(0,t-8):min(450,b+8),max(0,l-8):min(360,r+8)]=True
  # Annotated primary subject bounds from the source photography.
  subj={1:[150,145,360,360],2:[128,138,360,360],3:[173,188,360,365]}[i]
  l,t,r,b=subj; occupied[t:b,l:r]=True
  empty=[]
  for gy in range(25):
   row=[]
   for gx in range(20):
    x0,y0=gx*18,gy*18; cell=occupied[y0:y0+18,x0:x0+18]; pix=arr[y0:y0+18,x0:x0+18].astype(float)/255
    lin=np.where(pix<=0.04045,pix/12.92,((pix+0.055)/1.055)**2.4); lum=.2126*lin[:,:,0]+.7152*lin[:,:,1]+.0722*lin[:,:,2]
    row.append(bool((np.mean(~cell)>=.90) and lum.std()<=.025))
   empty.append(row)
  n=sum(sum(x) for x in empty); (ROOT/f'masks/slide-{i}-empty-grid.json').write_text(json.dumps({'grid':empty,'empty_cells':n,'total_cells':500,'empty_percent':100*n/500,'subject_bbox_preview_px':subj},indent=2)+'\n')
 (ROOT/'empty-area.json').write_text(json.dumps({'method':'360x450, 20x25 grid of 18px cells; text ink expanded 8px; subject boxes manually annotated per slide.','slides':[json.loads((ROOT/f'masks/slide-{i}-empty-grid.json').read_text()) for i in (1,2,3)]},indent=2)+'\n')
 print(json.dumps({'slides':[{'file':e['final'],'sha256':e['sha256'],'headline_box':e['ink_boxes_px']['headline'],'support_box':e['ink_boxes_px']['support'],'cta':e['copy']['cta']} for e in ev]},indent=2))
if __name__=='__main__':main()
