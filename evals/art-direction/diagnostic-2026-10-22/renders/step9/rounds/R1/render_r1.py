#!/usr/bin/env python3
"""Paso 9 R1: one measured correction pass for B3, flyer B and thumbnail B."""
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
REPO = ROOT.parents[4]
sys.path.insert(0, str(REPO / "skills/cropmark/engines/pillow"))
import cm  # noqa: E402
sys.path.insert(0, str(ROOT))
import render_s9 as r0  # noqa: E402

OUT = ROOT / "rounds/R1"
LIGHT = (255, 255, 255)
DARK = (38, 34, 29)

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def group(im, role, text, pos, size, font_name, leading, target, color=None, underline=False):
    f = r0.font(font_name, size)
    mask = r0.group_mask(im.size, text, pos, f, leading)
    candidates = {"light": r0.metrics(im, mask, LIGHT, target), "dark": r0.metrics(im, mask, DARK, target)}
    key = color or max(candidates, key=lambda k: candidates[k]["contrast_p05"])
    ink = LIGHT if key == "light" else DARK
    cm.text(im, pos, text, f, ink, leading=leading, role=role)
    if underline:
        b = mask.getbbox()
        if b: ImageDraw.Draw(im).line((b[0], b[3]+8, b[2], b[3]+8), fill=ink, width=3)
    return {"role":role,"text":text.replace("\n"," "),"editable_text":text,"position":list(pos),
            "font_file":font_name,"font_size":size,"visible_cap_height_px_master":r0.visible_cap(f),
            "visible_cap_height_px_at_360":round(r0.visible_cap(f)*360/1080,2),
            "ink_srgb":list(ink),"contrast":candidates[key],"candidate_contrast":candidates,
            "effects":{"shadow":False,"stroke":False,"text_panel":False},"underline":underline}

def b3_specs():
    return [
      {"headline":"La forma\ntoma cuerpo.","headline_pos":(70,170),
       "support":"Una pieza\nempieza con\nun gesto.","support_pos":(70,555),
       "cta":"EXPLORA EL\nTALLER","cta_pos":(70,770),"brand_pos":(70,60),"desc_pos":(70,128),
       "headline_size":132,"small_color":"dark","reason":"Move support/action to left wall quiet band and move headline above the complete vessel rim.",
       "relation":"rim echo stays above the complete vessel lip; small copy is gathered in the left wall quiet band"},
      {"headline":"Del giro\nnace el borde.","headline_pos":(70,260),
       "support":"El torno acompaña\ncada movimiento.","support_pos":(70,500),
       "cta":"SIGUE EL\nPROCESO","cta_pos":(70,635),"brand_pos":(70,60),"desc_pos":(70,128),
       "headline_size":116,"small_color":"dark","reason":"Move action copy into the measured left-wall gap, clear of the wheel and hand.",
       "relation":"wheel arc answers the lower-left headline; action copy sits above it on the calm wall"},
      {"headline":"Cada huella\ndeja memoria.","headline_pos":(70,575),
       "support":"Un rastro queda en\nla superficie.","support_pos":(70,235),
       "cta":"MIRA LAS PIEZAS","cta_pos":(70,1195),"brand_pos":(70,80),"desc_pos":(70,148),
       "headline_size":124,"small_color":"light","reason":"Use pure white for brand, descriptor and support on the measured darker clay field.",
       "relation":"headline remains beside the thumbprint trace; secondary copy uses pure white on the darker clay field"},
    ]

def render_b3():
    result=[]; outdir=OUT/"B3";outdir.mkdir(parents=True,exist_ok=True)
    for i,s in enumerate(b3_specs(),1):
        cm.reset(); src=ROOT/f"B3/base-{i}.png"; base=r0.fit(src,(1080,1350)); im=base.copy(); gs=[]
        col=s["small_color"]
        gs.append(group(im,"brand","TALLER BARRO",s["brand_pos"],60,"InstrumentSans-Bold.ttf",1.05,r0.TARGET_SMALL,col))
        gs.append(group(im,"descriptor","CERÁMICA",s["desc_pos"],60,"InstrumentSans-Bold.ttf",1.05,r0.TARGET_SMALL,col))
        gs.append(group(im,"headline",s["headline"],s["headline_pos"],s["headline_size"],"InstrumentSerif-Regular.ttf",1.02,r0.TARGET_LARGE,col))
        gs.append(group(im,"support",s["support"],s["support_pos"],58,"InstrumentSans-Regular.ttf",1.12,r0.TARGET_SMALL,col))
        cta_color = "dark" if i == 3 else col
        gs.append(group(im,"cta",s["cta"],s["cta_pos"],58,"InstrumentSans-Bold.ttf",1.05,r0.TARGET_SMALL,cta_color,underline=(i==3)))
        out=outdir/f"final-{i}.png"; cm.save(im,str(out))
        boxes=json.loads(Path(str(out)+".boxes.json").read_text())
        boxes.update({"condition":"B3 Cropmark R1","round":"R1","source_base":str(src.relative_to(ROOT)),
                      "crop":r0.crop_sidecar(src,(1080,1350)),"groups":gs,"headline_image_relation":s["relation"]})
        Path(str(out)+".boxes.json").write_text(json.dumps(boxes,ensure_ascii=False,indent=2)+"\n")
        r0.svg_overlay(f"rounds/R1/B3/final-{i}.svg",(1080,1350),gs)
        result.append({"slide":i,"final":str(out.relative_to(ROOT)),"reason":s["reason"],"groups":gs,
                       "headline_image_relation":s["relation"],"source_sha256":sha(src),"final_sha256":sha(out)})
    return result

def render_flyer():
    cm.reset();src=ROOT/"flyer/B-base-source.png";base=r0.fit(src,(1080,1350));im=base.copy()
    gs=[group(im,"event","Noche de vinilos",(84,278),76,"InstrumentSerif-Regular.ttf",1.0,r0.TARGET_LARGE,"dark"),
        group(im,"venue_date","Sala Taller ·\n14 nov · 21:00",(86,438),60,"InstrumentSans-Bold.ttf",1.12,r0.TARGET_SMALL,"dark")]
    out=OUT/"flyer-B.png";cm.save(im,str(out));boxes=json.loads(Path(str(out)+".boxes.json").read_text())
    boxes.update({"condition":"Flyer B Cropmark R1","round":"R1","source_base":str(src.relative_to(ROOT)),
                  "crop":r0.crop_sidecar(src,(1080,1350)),"groups":gs,"metadata_hierarchy":"Sala Taller · / 14 nov · 21:00"})
    Path(str(out)+".boxes.json").write_text(json.dumps(boxes,ensure_ascii=False,indent=2)+"\n")
    r0.svg_overlay("rounds/R1/flyer-B.svg",(1080,1350),gs)
    return {"final":str(out.relative_to(ROOT)),"reason":"Raise metadata cap height and keep room/date/time in one coherent group with no orphan separator.",
            "groups":gs,"source_sha256":sha(src),"final_sha256":sha(out)}

def render_thumb():
    cm.reset();src=ROOT/"thumbnail/B-base-R1-source.png";base=r0.fit(src,(1280,720));im=base.copy()
    text="3 AIs.\n1 Portfolio.";f=r0.font("BricolageGrotesque-Bold.ttf",100);pos=(52,480)
    mask=r0.group_mask(im.size,text,pos,f,1.03)
    candidates={"light":r0.metrics(base,mask,LIGHT,r0.TARGET_LARGE),"dark":r0.metrics(base,mask,DARK,r0.TARGET_LARGE)}
    ink=LIGHT;cm.text(im,pos,text,f,ink,leading=1.03,role="headline")
    g={"role":"headline","text":"3 AIs. 1 Portfolio.","editable_text":text,"position":list(pos),
       "font_file":"BricolageGrotesque-Bold.ttf","font_size":100,"visible_cap_height_px_master":r0.visible_cap(f),
       "visible_cap_height_px_at_168":round(r0.visible_cap(f)*168/1280,2),"ink_srgb":list(ink),
       "contrast":candidates["light"],"candidate_contrast":candidates,"effects":{"shadow":False,"stroke":False,"text_panel":False}}
    out=OUT/"thumbnail-B.png";cm.save(im,str(out));boxes=json.loads(Path(str(out)+".boxes.json").read_text())
    boxes.update({"condition":"Thumbnail B Cropmark R1","round":"R1","source_base":str(src.relative_to(ROOT)),
                  "crop":r0.crop_sidecar(src,(1280,720)),"groups":[g]})
    Path(str(out)+".boxes.json").write_text(json.dumps(boxes,ensure_ascii=False,indent=2)+"\n")
    r0.svg_overlay("rounds/R1/thumbnail-B.svg",(1280,720),[g])
    deliver=ROOT/"thumbnail/B-R1.png";im.save(deliver)
    Path(str(deliver)+".boxes.json").write_text(json.dumps(boxes,ensure_ascii=False,indent=2)+"\n")
    Path(str(deliver)+".sidecar.json").write_text(json.dumps({"condition":"Thumbnail B Cropmark R1","source_base":str(src.relative_to(ROOT)),"groups":[g],"output_sha256":sha(deliver)},ensure_ascii=False,indent=2)+"\n")
    return {"final":str(deliver.relative_to(ROOT)),"working_render":str(out.relative_to(ROOT)),"groups":[g],
            "source_sha256":sha(src),"final_sha256":sha(deliver)}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    record={"round":"R1","corrective_passes":{"B3":1,"flyer_B":1,"thumbnail_B":1},
            "B3":render_b3(),"flyer_B":render_flyer(),"thumbnail_B":render_thumb(),
            "R0_untouched":True,"A_untouched":True,
            "rounds_note":"One correction pass per requested piece; no image generation, source-image changes, shadows, strokes, or panels."}
    (OUT/"render-log.json").write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"B3":[x["final"] for x in record["B3"]],"flyer_B":record["flyer_B"]["final"],"thumbnail_B":record["thumbnail_B"]["final"]},indent=2))

if __name__=="__main__":main()
