"""Regression contracts for unsafe defaults and delivery validation.

Run CM_SKILL=/path/to/skills/cropmark python -m unittest this_file.py.
Fixtures have independent expected outcomes; no image generation required.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw

SKILL = Path(os.environ.get('CM_SKILL', Path(__file__).resolve().parents[1]/'skills/cropmark'))
spec = importlib.util.spec_from_file_location('cropmark_cm_under_test', SKILL/'engines/pillow/cm.py')
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)

class SafeCutout(unittest.TestCase):
    def test_QT04_pillow_translucent_fill_is_composited(self):
        im=cm.new(300,200,'white')
        cm.text(im,(50,50),'W',cm.font('Anton-Regular',80),fill=(0,0,0,25))
        self.assertGreaterEqual(min(im.getchannel('R').getdata()),229)

    def test_QT08_unavailable_weight_is_not_silently_ignored(self):
        with self.assertRaises(ValueError): cm.font('Anton-Regular',40,weight=700)

    def test_QT14_default_cleanup_preserves_legitimate_green(self):
        src = Image.new('RGBA', (20,20), (20,160,20,255))
        self.assertEqual(cm.clean_cutout(src).tobytes(), src.tobytes())

    def test_QT15_default_cleanup_preserves_fine_alpha(self):
        src = Image.new('RGBA', (25,25), (80,40,20,0))
        d = ImageDraw.Draw(src); d.line((12,2,12,22), fill=(80,40,20,160))
        self.assertEqual(cm.clean_cutout(src).tobytes(), src.tobytes())

    def test_QT16_default_cleanup_preserves_translucent_material(self):
        src=Image.new('RGBA',(25,25),(100,180,130,85))
        ImageDraw.Draw(src).line((5,5,20,20),fill=(255,255,255,210))
        self.assertEqual(cm.clean_cutout(src).tobytes(),src.tobytes())

    def test_QT13_key_keeps_enclosed_white_detail(self):
        src=Image.new('RGB',(60,60),'white')
        d=ImageDraw.Draw(src);d.rectangle((10,10,49,49),fill='black');d.rectangle((20,20,39,39),fill='white')
        out=cm.key_out(src,bg=(255,255,255),tol=20,feather=0)
        self.assertEqual(out.getpixel((0,0))[3],0)
        self.assertEqual(out.getpixel((30,30))[3],255)

    def test_QT11_missing_glyph_is_reported(self):
        with self.assertRaises(ValueError):
            cm.text(cm.new(200,200,'white'),(50,50),'\U0010ffff',cm.font('Anton-Regular',30))
    def test_QT11_decorative_text_helpers_reject_missing_glyph(self):
        for helper in (cm.sticky,cm.tag):
            with self.assertRaises(ValueError): helper(cm.new(500,500,'white'),(100,100),'\U0010ffff',cm.font('Anton-Regular',30))

class DeliveryQA(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def run_qa(self,*args):
        return subprocess.run([sys.executable,str(SKILL/'qa/qa.py'),*map(str,args)],cwd=self.root,text=True,capture_output=True)
    def image(self,name='piece.png',meta=True):
        p=self.root/name;Image.new('RGB',(1080,1350),'white').save(p)
        if meta:Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[]}))
        return p
    def test_QT01_no_args_is_structured_usage_failure(self):
        r=self.run_qa();self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
    def test_QT02_strict_rejects_missing_metadata(self):
        r=self.run_qa('post','--strict',self.image(meta=False));self.assertEqual(r.returncode,1)
    def test_QT02_strict_accepts_explicit_no_text(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[],'text_free':True}))
        self.assertEqual(self.run_qa('post','--strict',p).returncode,0)
    def test_QT02_strict_rejects_undeclared_empty_text_metadata(self):
        self.assertEqual(self.run_qa('post','--strict',self.image()).returncode,1)
    def test_QT02_shapes_cannot_account_for_undeclared_text(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'role':'shape','text':'','box':[100,100,200,200]}]}))
        self.assertEqual(self.run_qa('post','--strict',p).returncode,1)
    def test_QT02_shape_label_cannot_bypass_text_checks(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'role':'shape','text':'Unexpected','box':[100,100,200,200]}]}))
        self.assertEqual(self.run_qa('post','--strict',p).returncode,1)
    def test_QT02_non_string_text_is_invalid_input(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'text':42,'box':[100,100,200,200]}]}))
        r=self.run_qa('post','--strict',p);self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
    def test_QT08_html_effective_font_record_is_accepted(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'text':'A','box':[100,100,180,180],'color':'black','bg':'white','size':60,'effectiveFonts':[{'familyName':'Arial','glyphCount':1}]}]}))
        self.assertEqual(self.run_qa('post','--strict',p).returncode,0)
    def test_QT05_readable_outline_is_not_rejected_as_white_ink(self):
        p=self.root/'outlined.png'
        im=cm.new(1080,1350,'white');cm.text(im,(100,100),'READ',cm.font('Anton-Regular',100),fill=(255,255,255),stroke=8)
        cm.save(im,str(p))
        self.assertEqual(self.run_qa('post','--strict',p).returncode,0)
    def test_QT04_translucent_background_requires_backdrop(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'text':'A','box':[100,100,180,180],'color':'black','bg':'rgba(255,255,255,0.01)','size':60,'effectiveFonts':[{'familyName':'Arial'}]}]}))
        self.assertNotEqual(self.run_qa('post','--strict',p).returncode,0)
    def test_QT02_filename_cannot_suppress_a_failure(self):
        p=self.root/'fake_original.png';Image.new('RGB',(12,12),'white').save(p)
        self.assertEqual(self.run_qa('post',p).returncode,1)
    def test_QT03_invalid_color_is_diagnostic_not_white(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'text':'A','box':[100,100,180,180],'fill':'not-a-color','size':60}]}))
        r=self.run_qa('post',p);self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)
    def test_QT25_reel_right_overlay_rejected(self):
        p=self.root/'reel.png';Image.new('RGB',(1080,1920),'white').save(p)
        Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1920],'boxes':[{'text':'A','box':[970,500,1050,580],'fill':'black','bg':'white','size':60}]}))
        r=self.run_qa('reel',p)
        self.assertEqual(r.returncode,1)
        self.assertIn('safe zone',r.stdout.lower())
        self.assertNotIn('Traceback',r.stderr)
    def reel_fixture(self,y):
        p=self.root/'reel-text.png'
        im=cm.new(1080,1920,'white');cm.text(im,(100,y),'SAFE',cm.font('Anton-Regular',60),fill=(0,0,0));cm.save(im,str(p))
        return self.run_qa('reel',p)
    def test_QT25_reel_central_text_accepted(self):
        self.assertEqual(self.reel_fixture(600).returncode,0)
    def test_QT25_reel_top_overlay_rejected_for_safe_zone(self):
        r=self.reel_fixture(100);self.assertEqual(r.returncode,1);self.assertIn('safe zone',r.stdout.lower())
    def test_QT25_reel_bottom_overlay_rejected_for_safe_zone(self):
        r=self.reel_fixture(1300);self.assertEqual(r.returncode,1);self.assertIn('safe zone',r.stdout.lower())
    def test_QT02_invalid_box_is_structured_failure(self):
        p=self.image();Path(str(p)+'.boxes.json').write_text(json.dumps({'size':[1080,1350],'boxes':[{'text':'A','box':[180,100,100,180]}]}))
        r=self.run_qa('post',p);self.assertEqual(r.returncode,2);self.assertNotIn('Traceback',r.stderr)

if __name__=='__main__':unittest.main(verbosity=2)
