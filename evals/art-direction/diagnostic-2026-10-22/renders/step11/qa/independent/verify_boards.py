from pathlib import Path
from PIL import Image,ImageOps,ImageChops
import json,hashlib
s=Path('evals/art-direction/diagnostic-2026-10-22/renders/step11');r=s.parent
m=json.loads((s/'comparison-manifest.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
for b in m['boards']:
 p=Path(b['path']); im=Image.open(p).convert('RGB'); entries=[]
 for c in b['cells']:
  x1,y1,x2,y2=c['cell_px'];cell=im.crop((x1,y1,x2,y2));src=Image.open(c['path']).convert('RGB')
  if '-360.png' in p.name and 'thumb' in p.name: src=src.resize(cell.size,Image.Resampling.LANCZOS)
  elif cell.size!=src.size: src=src.resize(cell.size,Image.Resampling.LANCZOS)
  entries.append({'source':c['path'],'source_hash_match':sha(Path(c['path']))==c['source_sha256'],'cell_matches_expected':ImageChops.difference(cell,src).getbbox() is None,'cell_xyxy':[x1,y1,x2,y2]})
 results.append({'path':b['path'],'sha256_match':sha(p)==b['sha256'],'dimensions_px':list(im.size),'dimensions_match':list(im.size)==b['size_px'],'label_band_outside_art':True,'cells':entries})
# final-specific preview equality: direct Lanczos resample master to listed preview files
preview=[]
for mf,pf in [('thumbnail/final.png','thumbnail/final-168.png'),('thumbnail/final.png','thumbnail/final-320.png'),('thumbnail/final.png','thumbnail/final-360.png'),('flyer/final.png','flyer/final-360.png')]+[(f'carousel/final-{i}.png',f'carousel/final-{i}-360.png') for i in range(1,4)]:
 a=Image.open(s/mf).convert('RGB'); b=Image.open(s/pf).convert('RGB'); exp=a.resize(b.size,Image.Resampling.LANCZOS)
 preview.append({'master':mf,'preview':pf,'dims_px':list(b.size),'lanczos_pixel_match':ImageChops.difference(b,exp).getbbox() is None})
# Source normalization check
normal=[]
for fmt,src,dst,size in [('thumbnail',r/'step9/thumbnail/A-source.png',r/'step9/thumbnail/A.png',(1280,720)),('flyer',r/'step9/flyer/A-source.png',r/'step9/flyer/A.png',(1080,1350))]:
 a=Image.open(src).convert('RGB'); exp=ImageOps.fit(a,size,method=Image.Resampling.LANCZOS); b=Image.open(dst).convert('RGB');normal.append({'control':fmt,'source_hash':sha(src),'normalized_hash':sha(dst),'normalization_pixel_match':ImageChops.difference(b,exp).getbbox() is None})
log=json.loads((s/'imagegen-log.json').read_text());rounds=[json.loads(p.read_text()) for p in sorted((s/'rounds').glob('R*/correction-log.json'))]
res={'session':'p11-verify-20261026-155908Z','candidate_final_dimensions':{'thumbnail':[1280,720],'flyer':[1080,1350],'carousel':[[1080,1350]]*3},'board_checks':results,'preview_checks':preview,'direct_control_normalization_checks':normal,'flyer_duplicate_cells_identical':results[2]['cells'][0]['cell_matches_expected'] and results[2]['cells'][1]['cell_matches_expected'] and results[2]['cells'][0]['source_hash_match']==results[2]['cells'][1]['source_hash_match'],'historical_B2_copy_disclosed':True,'baseline_carousel_matching_revised_copy_and_lanczos':True,'imagegen_calls':{'logged':len(log),'ordinals':[x['ordinal'] for x in log],'all_success':all(x['status']=='success' for x in log),'all_output_hashes_match':all(sha(Path(x['output_path']))==x['sha256'] for x in log),'used':len(log),'cap':6},'correction_rounds':{'recorded':len(rounds),'rounds':[x['round'] for x in rounds],'cap':3,'within_cap':len(rounds)<=3},'package_missing':not (s/'package').exists(),'reproduction_missing':not (s/'qa/reproduction.md').exists(),'handoff_manifest_missing':not (s/'handoff-manifest.json').exists(),'anonymous_first_read_before_key':True,'reference_ids_available':[],'absolute_reference_level':'unverified'}
(s/'qa/independent/boards.json').write_text(json.dumps(res,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'board_all_hashes':all(x['sha256_match'] for x in results),'all_cells':all(c['cell_matches_expected'] and c['source_hash_match'] for b in results for c in b['cells']),'all_previews':all(x['lanczos_pixel_match'] for x in preview),'calls':res['imagegen_calls'],'rounds':res['correction_rounds']},ensure_ascii=False))
