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

    def note_panel(self):
        self.data['frames'][0].update(margin=0,elements=[
            {'id':'panel','box':[80,265,1000,960]},
            {'id':'title','box':[136,330,651,514]},
            {'id':'body','box':[138,615,697,779]}],alignments=[],gaps=[],
            padding=[{'container':'panel','children':['title','body'],'balanced_axes':['y']}])
        return self.data['frames'][0]

    def test_real_note_panel_unbalanced_padding_fails_then_centred_ink_passes(self):
        frame=self.note_panel()
        report=self.check()
        self.assertTrue(any(c['rule']=='R06' and c['status']=='FAIL' for c in report['checks']))
        for element in frame['elements'][1:]:
            element['box'][1]+=58
            element['box'][3]+=58
        self.assertTrue(self.check()['passed'])

    def test_expected_asymmetric_padding_remains_valid(self):
        frame=self.note_panel()
        frame['padding'][0].pop('balanced_axes')
        frame['padding'][0]['expected']=[65,303,181,56]
        self.assertTrue(self.check()['passed'])

    def test_expected_and_balanced_axes_both_apply(self):
        frame=self.note_panel()
        frame['padding'][0]['expected']=[65,303,181,56]
        self.assertFalse(self.check()['passed'])

    def test_balance_compares_both_requested_axes(self):
        group=self.data['frames'][0]['padding'][0]
        group.pop('expected');group['balanced_axes']=['x','y']
        self.assertTrue(self.check()['passed'])
        self.data['frames'][0]['elements'][1]['box'][0]-=8
        self.assertTrue(any(c['rule']=='R06' and c['status']=='FAIL' for c in self.check()['checks']))

    def test_optical_balance_offset_requires_reason_and_measured_difference(self):
        frame=self.data['frames'][0]
        group=frame['padding'][0];group.pop('expected');group['balanced_axes']=['y']
        frame['elements'][1]['box'][1]+=8
        self.assertFalse(self.check()['passed'])
        group['balance_offsets']={'y':8}
        with self.assertRaises(ValueError):self.check()
        group['reason']='Rounded heading ink requires 8px more top clearance, inspected in render'
        self.assertTrue(self.check()['passed'])
        group['balance_offsets']['y']=4
        self.assertFalse(self.check()['passed'])

    def test_children_must_be_inside_container_even_if_balance_is_equal(self):
        frame=self.data['frames'][0];frame['alignments']=[];frame['gaps']=[]
        group=frame['padding'][0];group.pop('expected');group['balanced_axes']=['x','y']
        frame['elements'][1]['box']=[77,77,1003,503]
        self.assertFalse(self.check()['passed'])
        frame['elements'][1]['box']=[79,79,1001,501]
        self.assertTrue(self.check()['passed'])

    def test_maximum_gap_rejects_excess_separation_and_preserves_overlap(self):
        frame=self.data['frames'][0];frame['gaps'][0]['max']=36
        self.assertFalse(self.check()['passed'])
        frame['gaps'][0]['max']=40
        self.assertTrue(self.check()['passed'])
        frame['elements'][2]['box'][1]=200
        frame['gaps'][0].update(allow_overlap=True,reason='Legible intentional layered title')
        self.assertTrue(self.check()['passed'])
        frame['elements'][2]['box'][1]=300
        self.assertFalse(self.check()['passed'])

    def test_cli_rejects_invalid_padding_balance_contracts(self):
        invalid=[{}, {'balanced_axes':[]}, {'balanced_axes':'y'}, {'balanced_axes':None},
                 {'balanced_axes':['z']}, {'balanced_axes':['y','y']}, {'balanced_axes':[{}]},
                 {'balanced_axes':['y'],'balance_offsets':[]},
                 {'balanced_axes':['y'],'balance_offsets':{'x':2},'reason':'visible correction'},
                 {'balanced_axes':['y'],'balance_offsets':{'y':True},'reason':'visible correction'},
                 {'balanced_axes':['y'],'balance_offsets':{'y':float('nan')},'reason':'visible correction'},
                 {'balanced_axes':['y'],'balance_offsets':{'y':2}},
                 {'expected':None}, {'expected':[-1,0,0,0]}]
        for values in invalid:
            with self.subTest(values=values):
                data=copy.deepcopy(self.data)
                data['frames'][0]['padding']=[{'container':'panel','children':['title','body'],**values}]
                self.assert_invalid_cli(data)

    def test_cli_rejects_invalid_maximum_gaps(self):
        for maximum in (0,31,-1,True,'40',None,float('inf'),10**1000):
            with self.subTest(maximum=maximum):
                data=copy.deepcopy(self.data)
                data['frames'][0]['gaps'][0]['max']=maximum
                self.assert_invalid_cli(data)

if __name__=='__main__':unittest.main()
