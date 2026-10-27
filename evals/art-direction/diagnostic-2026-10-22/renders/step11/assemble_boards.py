#!/usr/bin/env python3
"""Assemble Paso 11 comparison boards from frozen finals with external labels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json
R=Path(__file__).resolve().parent; REPO=Path(__file__).resolve().parents[5]
F=REPO/'skills/cropmark/fonts/InstrumentSans-Bold.ttf'; BG=(247,243,232); FG=(31,42,37)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p,size):return Image.open(p).convert('RGB').resize(size,Image.Resampling.LANCZOS)
def board(path,cells,labels,size,band,preview=False):
 w,h=size; ncols=len(cells[0]); nrows=len(cells); out=Image.new('RGB',(ncols*w,nrows*(h+band)),BG); d=ImageDraw.Draw(out); font=ImageFont.truetype(str(F),26 if w>=1000 else 13)
 coords=[]
 for row in range(nrows):
  y=row*(h+band); d.text((18,y+4),labels[row],font=font,fill=FG)
  y+=band
  for col,p in enumerate(cells[row]):
   x=col*w; out.paste(load(p,(w,h)),(x,y)); coords.append({'path':str(p.relative_to(REPO)),'source_sha256':sha(p),'cell_px':[x,y,x+w,y+h],'row':row+1,'column':col+1})
 out.save(path,optimize=True); return {'path':str(path.relative_to(REPO)),'sha256':sha(path),'size_px':list(out.size),'cell_px':[w,h],'label_band_px':band,'cells':coords}
S=R
thumb=[[REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step9/thumbnail/A.png',REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step10/thumbnail/C.png',S/'thumbnail/final.png']]
flyer=[[REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/A.png',REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step9/flyer/A.png',S/'flyer/final.png']]
car=[[S/'baseline/carousel-1.png',S/'baseline/carousel-2.png',S/'baseline/carousel-3.png'],[REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-1.png',REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-2.png',REPO/'evals/art-direction/diagnostic-2026-10-22/renders/step8/B2/final-3.png'],[S/'carousel/final-1.png',S/'carousel/final-2.png',S/'carousel/final-3.png']]
labels=['NO-SKILL direct raster · Paso 9 A','Paso 10 winner · C','Paso 11 candidate']
records=[]
records.append(board(S/'thumb-board.png',thumb,labels,(1280,720),48))
records.append(board(S/'thumb-board-360.png',thumb,labels,(360,203),24))
flabels=['NO-SKILL direct raster · Paso 9 A','Paso 10 winner · A (same image as direct control)','Paso 11 candidate']
records.append(board(S/'flyer-board.png',flyer,flabels,(1080,1350),48))
records.append(board(S/'flyer-board-360.png',flyer,flabels,(360,450),24))
clabels=['NO-SKILL direct raster · revised one-CTA brief','Paso 10 winner B2 · historical copy: three action lines','Paso 11 candidate · one closing CTA']
records.append(board(S/'carousel-board.png',car,clabels,(1080,1350),48))
records.append(board(S/'carousel-board-360.png',car,clabels,(360,450),24))
# Anonymous copies preserve order and equal sizing, using neutral labels.
blind=R/'qa/blind'; blind.mkdir(parents=True,exist_ok=True)
key={'thumb':{'A':'NO-SKILL direct raster · Paso 9 A','B':'Paso 10 winner · C','C':'Paso 11 candidate'},'flyer':{'A':'NO-SKILL direct raster · Paso 9 A','B':'Paso 10 winner · A (duplicate of A)','C':'Paso 11 candidate'},'carousel':{'A':'NO-SKILL direct raster · revised brief','B':'Paso 10 winner B2 · historical copy','C':'Paso 11 candidate'}}
key_path=blind/'key.json'; key_path.write_text(json.dumps(key,ensure_ascii=False,indent=2)+'\n')
for name,rows,sz in [('thumb',thumb[0],(1280,720)),('flyer',flyer[0],(1080,1350))]:
 for i,p in enumerate(rows):load(p,sz).save(blind/f'{name}-{chr(65+i)}.png',optimize=True)
for row,label in zip(car,'ABC'):
 for i,p in enumerate(row):load(p,(1080,1350)).save(blind/f'carousel-{label}-{i+1}.png',optimize=True)
(R/'comparison-manifest.json').write_text(json.dumps({'boards':records,'flyer_cells_1_2_identical':True,'historical_B2_copy_disclosed':True,'blind_key_sha256':sha(key_path)},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'boards':[r['path'] for r in records],'blind_files':len(list(blind.glob('*.png')))},indent=2))
