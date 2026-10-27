from pathlib import Path
from PIL import Image, ImageOps
import numpy as np, json
S=Path('evals/art-direction/diagnostic-2026-10-22/renders/step11')
def lin(x):
 x=x.astype(np.float64)/255
 return np.where(x<=.04045,x/12.92,((x+.055)/1.055)**2.4)
def lum(a):
 q=lin(a);return .2126*q[:,:,0]+.7152*q[:,:,1]+.0722*q[:,:,2]
def scan(bg,fg,groups):
 base=np.asarray(bg.convert('RGB')).astype(float);final=np.asarray(fg.convert('RGB')).astype(float);B=lum(base);F=lum(final);res={}
 for name,(box,color) in groups.items():
  x1,y1,x2,y2=box;c=np.array(color,dtype=float);b=base[y1:y2,x1:x2];f=final[y1:y2,x1:x2];v=c[None,None,:]-b;alpha=np.clip(((f-b)*v).sum(2)/((v*v).sum(2)+1e-6),0,1);core=alpha>=.98
  old=B[y1:y2,x1:x2][core];new=F[y1:y2,x1:x2][core]
  if len(old):
   ratio=(np.maximum(old,new)+.05)/(np.minimum(old,new)+.05)
   res[name]={'core_pixels':int(len(ratio)),'P05':round(float(np.percentile(ratio,5)),2),'median':round(float(np.median(ratio)),2),'share_below_4_5_percent':round(float((ratio<4.5).mean()*100),2),'share_below_3_percent':round(float((ratio<3).mean()*100),2)}
  else:res[name]={'core_pixels':0,'status':'no >=.98 alpha pixels in defined crop'}
 return res
slides=[('step8/B2/base-1.png',None,{'brand':([24,20,174,41],[250,246,231]),'descriptor':([24,43,125,63],[250,246,231]),'headline':([24,78,220,155],[250,246,231]),'support':([24,174,220,220],[250,246,231])}),('step8/B2/base-2.png',None,{'brand':([24,20,174,41],[250,246,231]),'descriptor':([24,43,125,63],[250,246,231]),'headline':([24,259,230,339],[29,39,35]),'support':([24,365,230,420],[29,39,35])}),('step8/B2/base-3.png',(200,300,920,1200),{'brand':([24,20,174,41],[250,246,231]),'descriptor':([24,43,125,63],[250,246,231]),'headline':([24,78,225,160],[250,246,231]),'support':([24,174,220,223],[250,246,231]),'cta':([24,398,200,423],[29,39,35])})]
out={'method':'known foreground/background projection from clean photographic bases; alpha-core >=0.98; linearized sRGB','carousel':{}}
for i,(src,crop,groups) in enumerate(slides,1):
 b=Image.open(S.parent/src).convert('RGB')
 if crop:b=b.crop(crop).resize((1080,1350),Image.Resampling.LANCZOS)
 elif b.size!=(1080,1350):b=ImageOps.fit(b,(1080,1350),method=Image.Resampling.LANCZOS)
 bg=b.resize((360,450),Image.Resampling.LANCZOS)
 out['carousel'][str(i)]=scan(bg,Image.open(S/f'carousel/final-{i}-360.png'),groups)
fb=Image.open(S/'flyer/clean-source-crop.png').convert('RGB');ff=Image.open(S/'flyer/final.png').convert('RGB')
out['flyer']=scan(fb,ff,{'title_line_1':([90,300,590,445],[69,51,39]),'title_line_2':([90,445,590,600],[69,51,39]),'metadata':([90,610,620,750],[69,51,39])})
(S/'qa/independent/contrast-core.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False))
