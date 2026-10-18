"""HTML rendering behavior checks. Uses an isolated copy; installs nothing.

Pass --skill, --out, --node, --node-modules, --browsers as in test_contracts.py.
Evidence includes exact commands, diagnostics, output metadata and a results file.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unittest

parser = argparse.ArgumentParser()
for name in ('skill', 'out', 'node', 'node-modules', 'browsers'):
    parser.add_argument('--' + name, required=True)
args = parser.parse_args()
out = Path(args.out).resolve()
if out.exists() and any(out.iterdir()):
    raise SystemExit('Refusing to overwrite existing evidence')
out.mkdir(parents=True, exist_ok=True)
mirror = out / 'isolated-skill'
shutil.copytree(Path(args.skill).resolve(), mirror, ignore=shutil.ignore_patterns('node_modules', '__pycache__'))
(mirror / 'engines/html/node_modules').symlink_to(Path(args.node_modules).resolve(), target_is_directory=True)
shutil.copyfile(__file__, out / 'test_html_v05.py')
env = dict(os.environ, PLAYWRIGHT_BROWSERS_PATH=str(Path(args.browsers).resolve()))
env.pop('CHROME_PATH', None)
records = []

class HTMLBehavior(unittest.TestCase):
    def render(self, content='', *, style='', attributes='id="test"', scale=1, body=None):
        folder = out / (self._testMethodName + '-' + str(len(records)))
        folder.mkdir()
        html = folder / 'page.html'
        html.write_text('<!doctype html><body style="margin:0">' + (body if body is not None else
            '<section class="frame" ' + attributes + ' style="position:relative;width:400px;height:300px;background:white;' + style + '">' + content + '</section>'))
        cmd = [args.node, str(mirror / 'engines/html/render.mjs'), str(html), str(folder / 'png'), str(scale)]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
        record = {'test': self._testMethodName, 'argv': cmd, 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        records.append(record)
        (folder / 'command.json').write_text(json.dumps(record, indent=2))
        return result, sorted((folder / 'png').glob('*.png'))

    def assertRejected(self, result, images):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('ERROR cropmark HTML', result.stderr)
        self.assertEqual(images, [])

    def strict_qa(self, image):
        cmd = [sys.executable, str(mirror / 'qa/qa.py'), 'post', '--strict', '--out', str(image.parent.parent / 'qa'), str(image)]
        result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=60)
        record = {'test': self._testMethodName, 'argv': cmd, 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
        records.append(record)
        (image.parent.parent / 'qa-command.json').write_text(json.dumps(record, indent=2))
        return result

    def integration_render(self, content='', *, style='', attributes='id="test"'):
        result, images = self.render(content, style='width:1080px;height:1350px;' + style, attributes=attributes)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(images), 1)
        meta = json.loads(Path(str(images[0]) + '.boxes.json').read_text())
        return images[0], meta

    def assertContrastRejected(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('contrast', result.stdout)
        self.assertNotIn('effective font not recorded', result.stdout)
        self.assertNotIn('ERROR', result.stderr)
        self.assertNotIn('no text boxes', result.stdout)

    def test_integration_opaque_text_passes_strict_qa(self):
        image, meta = self.integration_render('<p style="position:absolute;left:100px;top:200px;margin:0;font:60px Arial;color:black">Readable text</p>')
        self.assertEqual(meta['boxes'][0]['opacity'], 1)
        self.assertEqual(meta['boxes'][0]['bg'], [255, 255, 255])
        result = self.strict_qa(image)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_integration_translucent_background_fails_strict_contrast(self):
        image, meta = self.integration_render('<p style="position:absolute;left:100px;top:200px;margin:0;font:60px Arial;color:black;background:rgba(255,255,255,.01)">Almost invisible</p>', style='background:black')
        self.assertTrue(all(0 < channel < 4 for channel in meta['boxes'][0]['bg']))
        self.assertContrastRejected(self.strict_qa(image))

    def test_integration_ancestor_opacity_fails_strict_contrast(self):
        image, meta = self.integration_render('<div style="opacity:.1"><p style="position:absolute;left:100px;top:200px;margin:0;font:60px Arial;color:black;opacity:.1">Almost invisible</p></div>')
        self.assertAlmostEqual(meta['boxes'][0]['opacity'], .01)
        self.assertIsNone(meta['boxes'][0]['bg'])
        self.assertContrastRejected(self.strict_qa(image))

    def test_integration_explicit_text_free_passes_and_undeclared_fails(self):
        image, meta = self.integration_render(attributes='id="test" data-text-free="true"')
        self.assertIs(meta['text_free'], True)
        self.assertEqual(self.strict_qa(image).returncode, 0)
        image, meta = self.integration_render()
        self.assertNotIn('text_free', meta)
        result = self.strict_qa(image)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('explicit text_free', result.stdout)

    def test_missing_first_family_rejects_silent_fallback(self):
        result, images = self.render('<p style="font:30px MissingCropmarkFamilyABC, sans-serif">Fallback</p>')
        self.assertRejected(result, images)
        self.assertIn('MissingCropmarkFamilyABC', result.stderr)

    def test_explicit_system_family_reports_effective_fonts(self):
        result, images = self.render('<p style="font:30px Arial, sans-serif">System font</p>')
        self.assertEqual(result.returncode, 0, result.stderr)
        meta = json.loads(Path(str(images[0]) + '.boxes.json').read_text())
        self.assertTrue(meta['boxes'][0]['effectiveFonts'])
        self.assertTrue(all(f['familyName'] and f['glyphCount'] > 0 for f in meta['boxes'][0]['effectiveFonts']))

    def test_generic_and_bundled_families_are_valid(self):
        result, images = self.render('<p style="font:30px serif">Generic</p><p style="font:30px Anton-Regular">Bundled</p>')
        self.assertEqual(result.returncode, 0, result.stderr)
        boxes = json.loads(Path(str(images[0]) + '.boxes.json').read_text())['boxes']
        self.assertTrue(any(f['isCustomFont'] for f in boxes[1]['effectiveFonts']))

    def test_invalid_scale_rejected(self):
        for scale in (0, -1, 'NaN', 'Infinity'):
            self.assertRejected(*self.render('Text', scale=scale))

    def test_unsafe_and_duplicate_ids_rejected(self):
        self.assertRejected(*self.render('Text', attributes='id="../../escape"'))
        self.assertRejected(*self.render(body='<section class="frame" id="same" style="width:400px;height:300px"></section>' * 2))

    def test_corrupt_image_decode_rejected(self):
        self.assertRejected(*self.render('<img src="data:image/png;base64,bm90LWFuLWltYWdl">'))

    def test_missing_background_image_rejected(self):
        self.assertRejected(*self.render(style="background-image:url(missing-background.png)"))

    def test_stroke_overflow_rejected_and_explicit_bleed_preserved(self):
        text = '<span style="position:absolute;left:0;top:100px;font:40px Arial;-webkit-text-stroke:20px black">Stroke</span>'
        self.assertRejected(*self.render(text))
        result, images = self.render(text.replace('<span ', '<span data-role="bleed" '), scale=2)
        self.assertEqual(result.returncode, 0, result.stderr)
        meta = json.loads(Path(str(images[0]) + '.boxes.json').read_text())
        self.assertEqual(meta['size'], [800, 600])
        self.assertEqual(meta['boxes'][0]['strokeWidth'], 40)
        self.assertEqual(meta['boxes'][0]['stroke_fill'], 'rgb(0, 0, 0)')
        self.assertLess(meta['boxes'][0]['box'][0], 0)
        self.assertEqual(meta['boxes'][0]['role'], 'bleed')
        self.assertEqual(meta['boxes'][0]['boundsKind'], 'css-range-with-stroke-expansion')

result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(HTMLBehavior))
(out / 'results.json').write_text(json.dumps({'tests_run': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'commands': records}, indent=2))
raise SystemExit(0 if result.wasSuccessful() else 1)
