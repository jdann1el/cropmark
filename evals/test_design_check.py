"""Behavioural checks for declared design relationships, including valid exceptions."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('design',Path(__file__).resolve().parents[1]/'skills/cropmark/qa/design_check.py')
design=importlib.util.module_from_spec(spec);spec.loader.exec_module(design)

class DesignChecks(unittest.TestCase):
    def setUp(self):
        self.data={'version':1,'frames':[{'id':'one','size':[1080,1350],'margin':64,
            'elements':[{'id':'panel','box':[80,80,1000,500]},{'id':'title','box':[112,112,968,220]},{'id':'body','box':[112,260,968,468]}],
            'alignments':[{'axis':'left','elements':['title','body']}],
            'padding':[{'container':'panel','children':['title','body'],'expected':[32,32,32,32]}],
            'gaps':[{'a':'title','b':'body','axis':'y','min':32}], 'tokens':{'display':'A'}}]}
    def check(self): return design.check(self.data,Path('.'))
    def test_valid_composition(self): self.assertTrue(self.check()['passed'])
    def test_accidental_alignment_is_rejected(self):
        self.data['frames'][0]['elements'][2]['box'][0]+=8
        self.assertTrue(any(c['rule']=='R05' and c['status']=='FAIL' for c in self.check()['checks']))
    def test_declared_optical_offset_is_preserved(self):
        f=self.data['frames'][0];f['elements'][2]['box'][0]+=8
        f['alignments'][0].update(offsets={'body':8},reason='Curved opening glyph aligns optically to title')
        self.assertTrue(self.check()['passed'])
    def test_offset_without_reason_invalid(self):
        self.data['frames'][0]['alignments'][0]['offsets']={'body':8}
        with self.assertRaises(ValueError): self.check()
    def test_unequal_padding_fails(self):
        self.data['frames'][0]['elements'][1]['box'][1]+=9
        self.assertFalse(self.check()['passed'])
    def test_crowded_blocks_fail(self):
        self.data['frames'][0]['elements'][2]['box'][1]=230
        self.assertTrue(any(c['rule']=='R07' and c['status']=='FAIL' for c in self.check()['checks']))
    def test_deliberate_overlap_is_not_accidental_gap(self):
        f=self.data['frames'][0];f['elements'][2]['box'][1]=200
        f['gaps'][0].update(allow_overlap=True,reason='Layered wordmark with readable foreground')
        self.assertTrue(self.check()['passed'])
    def test_bleed_requires_visible_purpose(self):
        f=self.data['frames'][0];f['elements'].append({'id':'photo','box':[-20,500,1100,1370],'bleed':True})
        with self.assertRaises(ValueError): self.check()
        f['elements'][-1]['reason']='Full-bleed scene, required type remains safe'
        self.assertTrue(self.check()['passed'])
    def test_unexplained_off_canvas_fails(self):
        self.data['frames'][0]['elements'][0]['box'][0]=-1
        self.assertFalse(self.check()['passed'])
    def test_set_invariants_and_deliberate_variation(self):
        f=copy.deepcopy(self.data['frames'][0]);f['id']='two';f['elements'][2]['box'][1]=300
        self.data['frames'].append(f);self.data['shared_tokens']=['display']
        self.assertTrue(self.check()['passed'])
        f['tokens']['display']='B';self.assertFalse(self.check()['passed'])
    def test_missing_set_token_is_invalid(self):
        self.data['shared_tokens']=['ink']
        with self.assertRaises(ValueError): self.check()
    def test_missing_font_file_fails(self):
        self.data['frames'][0]['elements'][1]['font_path']='missing-font.ttf'
        self.assertFalse(self.check()['passed'])
    def test_empty_input_cannot_pass(self):
        self.data['frames']=[]
        with self.assertRaises(ValueError):self.check()
    def test_nonfinite_or_boolean_geometry_invalid(self):
        for value in [float('nan'),float('inf'),True]:
            self.data['frames'][0]['elements'][0]['box'][0]=value
            with self.assertRaises(ValueError): self.check()
    def test_unknown_reference_invalid(self):
        self.data['frames'][0]['gaps'][0]['a']='missing'
        with self.assertRaises(ValueError):self.check()
    def test_negative_spacing_invalid(self):
        self.data['frames'][0]['gaps'][0]['min']=-2
        with self.assertRaises(ValueError):self.check()

    def run_cli(self, data):
        with tempfile.TemporaryDirectory() as directory:
            contract=Path(directory)/'contract.json'
            contract.write_text(json.dumps(data))
            return subprocess.run([sys.executable,'-B',str(Path(design.__file__)),str(contract)],
                                  capture_output=True,text=True,timeout=10)

    def assert_invalid_cli(self, data):
        result=self.run_cli(data)
        self.assertEqual(result.returncode,2,result.stdout+result.stderr)
        self.assertIn('ERROR cropmark design contract:',result.stderr)
        self.assertNotIn('Traceback',result.stderr)
        self.assertEqual(result.stdout,'')

    def test_cli_rejects_malformed_relationship_collections(self):
        for key in ('alignments','padding','gaps'):
            for value in ({},'',None,True,1,[None],['group']):
                with self.subTest(key=key,value=value):
                    data=copy.deepcopy(self.data)
                    data['frames'][0][key]=value
                    self.assert_invalid_cli(data)

    def test_cli_accepts_explicit_empty_relationship_arrays(self):
        for key in ('alignments','padding','gaps'):
            self.data['frames'][0][key]=[]
        result=self.run_cli(self.data)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue(json.loads(result.stdout)['passed'])

    def test_cli_rejects_unrepresentable_coordinates_without_traceback(self):
        self.data['frames'][0]['size'][0]=10**1000
        self.assert_invalid_cli(self.data)

if __name__=='__main__':unittest.main()
