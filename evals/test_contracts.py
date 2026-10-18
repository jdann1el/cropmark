"""Independent deterministic regression contracts. Does not modify the tested skill.

Original failures are preserved on v0.4.0. This suite is not the visual release gate.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, subprocess, sys, time, unittest
from PIL import Image, ImageChops, ImageDraw

parser = argparse.ArgumentParser()
parser.add_argument('--skill', required=True)
parser.add_argument('--out', required=True)
parser.add_argument('--node', required=True)
parser.add_argument('--node-modules', required=True)
parser.add_argument('--browsers', required=True)
parser.add_argument('--only', nargs='*', help='Run only these QT IDs; preserve prior evidence without repeating unchanged tests')
ARGS = parser.parse_args()
SOURCE, OUT = Path(ARGS.skill).resolve(), Path(ARGS.out).resolve()
if OUT.exists() and any(OUT.iterdir()):
    raise SystemExit('Refusing to overwrite an existing test run')
OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(__file__, OUT / 'test_contracts.py')
sys.dont_write_bytecode = True
sys.path.insert(0, str(SOURCE / 'engines/pillow'))
import cm

ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PLAYWRIGHT_BROWSERS_PATH=str(Path(ARGS.browsers).resolve()))
ENV.pop('CHROME_PATH', None)
MIRROR = OUT / 'isolated-skill'
shutil.copytree(SOURCE, MIRROR, ignore=shutil.ignore_patterns('node_modules', '__pycache__', '*.pyc'))
(MIRROR / 'engines/html/node_modules').symlink_to(Path(ARGS.node_modules).resolve(), target_is_directory=True)
EXECUTIONS, OUTCOMES = [], []

def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def execute(argv, directory, tag):
    started = time.perf_counter()
    result = subprocess.run(argv, env=ENV, cwd=directory, capture_output=True, text=True, timeout=60)
    record = {'argv': argv, 'cwd': str(directory), 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'elapsed_seconds': time.perf_counter() - started}
    save_json(directory / (tag + '.command.json'), record)
    EXECUTIONS.append(record)
    return result

def contains(outer, inner):
    return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]

class Contracts(unittest.TestCase):
    def setUp(self):
        self.folder = OUT / self._testMethodName
        self.folder.mkdir()
        cm.reset()

    def qa(self, image=None, fmt='post', tag='qa'):
        argv = [sys.executable, str(SOURCE / 'qa/qa.py'), fmt, '--out', str(self.folder / (tag + '-previews'))]
        if image is not None:
            argv.append(str(image))
        return execute(argv, self.folder, tag)

    def fixture(self, label, *, size=(1080, 1350), color=(17, 17, 17), declared=None, xy=(80, 100), box=None):
        image = Image.new('RGB', size, 'white')
        ImageDraw.Draw(image).text(xy, 'QA', font=cm.font('Anton-Regular', 60), fill=color)
        path = self.folder / (label + '.png')
        image.save(path)
        save_json(Path(str(path) + '.boxes.json'), {'size': list(size), 'boxes': [{'text': 'QA', 'box': box or [xy[0], xy[1], xy[0] + 120, xy[1] + 90], 'fill': declared if declared is not None else list(color), 'bg': [255, 255, 255], 'size': 60}]})
        return path

    def render(self, body, tag='render', scale=1):
        path = self.folder / (tag + '.html')
        path.write_text('<!doctype html><meta charset="utf-8"><body style="margin:0">' + body + '</body>')
        target = self.folder / (tag + '-png')
        result = execute([ARGS.node, str(MIRROR / 'engines/html/render.mjs'), str(path), str(target), str(scale)], self.folder, tag)
        return result, sorted(target.glob('*.png'))

    @staticmethod
    def frame(content):
        return '<section class="frame" id="case" style="position:relative;width:1080px;height:1350px;background:white">' + content + '</section>'

    def test_QT01_rejects_zero_image_arguments(self):
        r = self.qa()
        self.assertNotEqual(r.returncode, 0, 'Zero images must not be a successful complete validation')

    def test_QT01_accepts_a_real_valid_input(self):
        self.assertEqual(self.qa(self.fixture('valid')).returncode, 0)

    def test_QT02_missing_metadata_cannot_be_a_complete_text_validation(self):
        path = self.fixture('missing-metadata')
        Path(str(path) + '.boxes.json').unlink()
        r = self.qa(path)
        self.assertNotEqual(r.returncode, 0, 'A text-bearing fixture without metadata cannot pass complete text validation')

    def test_QT02_invalid_schema_is_not_accepted(self):
        path = self.fixture('missing-size')
        save_json(Path(str(path) + '.boxes.json'), {'boxes': []})
        r = self.qa(path)
        self.assertNotEqual(r.returncode, 0, 'Metadata without coordinate size is invalid')

    def test_QT03_accepts_correct_high_contrast_hex(self):
        r = self.qa(self.fixture('hex', declared='#111111'))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_QT03_rejects_real_white_on_white(self):
        r = self.qa(self.fixture('invisible', color=(255, 255, 255), declared='#ffffff'))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('contrast', r.stdout.lower())

    def test_QT04_rejects_translucent_low_contrast_ink(self):
        r = self.qa(self.fixture('alpha-low', color=(230, 230, 230), declared='rgba(0,0,0,0.1)'))
        self.assertNotEqual(r.returncode, 0, 'The actual composed gray ink is below 3:1, not black at 21:1')

    def test_QT04_accepts_opaque_rgba_ink(self):
        r = self.qa(self.fixture('alpha-opaque', color=(0, 0, 0), declared='rgba(0,0,0,1)'))
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_QT05_metadata_contains_actual_stroked_ink(self):
        im = cm.new(1280, 720, 'white')
        declared = cm.text(im, (300, 100), 'W', cm.font('Anton-Regular', 120), fill=(0, 0, 0), stroke=30, stroke_fill=(64, 64, 64))
        actual = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
        cm.save(im, str(self.folder / 'stroke.png'))
        save_json(self.folder / 'measurement.json', {'declared': declared, 'actual_pixel_ink': actual})
        self.assertTrue(contains(declared, actual), f'{declared} omits ink {actual}')

    def test_QT06_metadata_contains_multiline_descenders(self):
        im = cm.new(1280, 720, 'white')
        declared = cm.text(im, (150, 100), 'Ág\njyp', cm.font('DMSerifDisplay-Italic', 120), fill=(0, 0, 0), leading=1.2)
        actual = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
        cm.save(im, str(self.folder / 'multiline.png'))
        save_json(self.folder / 'measurement.json', {'declared': declared, 'actual_pixel_ink': actual})
        self.assertTrue(contains(declared, actual), f'{declared} omits ink {actual}')

    def test_QT08_missing_font_file_is_not_silently_substituted(self):
        with self.assertRaises(OSError):
            cm.font('MissingFontForDeterministicTest', 60)

    def test_QT07_tracking_metadata_contains_actual_ink(self):
        measurements = []
        for tracking in (-0.05, 0.12):
            im = cm.new(1280, 720, 'white')
            declared = cm.text(im, (150, 100), 'AVÁ gjy', cm.font('DMSerifDisplay-Italic', 120), fill=(0, 0, 0), tracking=tracking)
            actual = ImageChops.difference(im, Image.new('RGB', im.size, 'white')).getbbox()
            cm.save(im, str(self.folder / ('tracking-' + str(tracking) + '.png')))
            measurements.append({'tracking_em': tracking, 'declared': declared, 'actual_pixel_ink': actual, 'contains': contains(declared, actual)})
        save_json(self.folder / 'measurement.json', measurements)
        self.assertTrue(all(x['contains'] for x in measurements), str(measurements))

    def pill_case(self, text, name='Anton-Regular', size=80):
        im = cm.new(1080, 1350, 'white')
        font = cm.font(name, size)
        outer = cm.pill(im, (100, 200), text, font, color=(0, 0, 0))
        mask = Image.new('L', im.size)
        mask.putdata([255 if max(pixel) <= 30 else 0 for pixel in im.getdata()])
        ink = mask.getbbox()
        cm.save(im, str(self.folder / (name + '.png')))
        self.assertIsNotNone(ink)
        self.assertTrue(contains(outer, ink), f'Text escapes pill: {outer}, {ink}')
        self.assertLessEqual(abs((outer[1] + outer[3] - ink[1] - ink[3]) / 2), 1.5, 'Ink must be vertically centered within raster rounding tolerance')
        return outer

    def test_QT09_short_pill_contains_centered_ink(self):
        self.pill_case('NEW')

    def test_QT10_long_pill_fits_after_fitting(self):
        text = 'Clase de prueba 9 €'
        font = cm.fit(text, 'InstrumentSans-Bold', 700, start=80, min_size=20)
        box = self.pill_case(text, 'InstrumentSans-Bold', font.size)
        self.assertLessEqual(box[2], 1080)

    def test_QT11_accents_and_glyphs_in_multiple_pill_fonts(self):
        for name in ('InstrumentSans-Bold', 'DMSerifDisplay-Italic', 'Caveat-Variable'):
            f = cm.font(name, 60)
            missing = f.getmask('\U0010ffff')
            absent = [char for char in 'Éçà€' if (f.getmask(char).size, bytes(f.getmask(char))) == (missing.size, bytes(missing))]
            self.assertFalse(absent, f'{name} lacks required glyphs {absent}')
            self.pill_case('Élan · 9 €', name, 60)

    def test_QT12_fit_does_not_silently_return_an_overflowing_minimum(self):
        text = 'Long supplied text that cannot fit in this tiny allocated width'
        try:
            f = cm.fit(text, 'Anton-Regular', 20, start=60, min_size=40)
        except ValueError:
            return
        self.assertLessEqual(f.getlength(text), 20, 'No fit at the minimum size must be reported as impossible, not returned as a fit')

    def test_QT21_renderer_rejects_documents_without_frames(self):
        r, images = self.render('<p>No output frame</p>')
        self.assertNotEqual(r.returncode, 0, f'Rendered {len(images)} images but returned success')

    def test_QT22_renderer_rejects_missing_essential_image(self):
        r, images = self.render(self.frame('<img id="hero" src="missing-required-image.png" width="700" height="700">'))
        self.assertNotEqual(r.returncode, 0, f'Missing hero image was exported as {len(images)} apparently successful PNG')

    def test_QT23_metadata_maps_to_the_same_pixel_coordinates_at_scale_two(self):
        body = self.frame('<p style="position:absolute;left:100px;top:180px;margin:0;font:80px Anton-Regular;color:black">Scale</p>')
        mapped = []
        for scale in (1, 2):
            r, images = self.render(body, 'scale-' + str(scale), scale)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(len(images), 1)
            im = Image.open(images[0])
            meta = json.loads(Path(str(images[0]) + '.boxes.json').read_text())
            factor = im.width / meta['size'][0]
            mapped.append([v * factor for v in meta['boxes'][0]['box']])
        save_json(self.folder / 'coordinate-comparison.json', {'scale1_pixel_box': mapped[0], 'scale2_pixel_box': mapped[1]})
        self.assertTrue(all(abs(b - a * 2) <= 2 for a, b in zip(*mapped)), f'Inconsistent physical pixel boxes: {mapped}')

    def test_QT24_valid_four_slice_sequence_has_four_correct_counters(self):
        content = ''.join(f'<b style="position:absolute;left:{80 + i * 1080}px;top:100px;font:80px Anton-Regular">{i + 1}/4</b>' for i in range(4))
        body = '<section class="frame" id="sequence" data-slices="4" style="position:relative;width:4320px;height:1350px;background:white">' + content + '</section>'
        r, images = self.render(body)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(len(images), 4)
        for i, path in enumerate(images):
            self.assertEqual(Image.open(path).size, (1080, 1350))
            texts = [x['text'] for x in json.loads(Path(str(path) + '.boxes.json').read_text())['boxes']]
            self.assertEqual(texts, [f'{i + 1}/4'])

    def test_QT24_invalid_slice_counts_are_rejected(self):
        bad = []
        for i, count in enumerate(('0', '-1', '2.5')):
            body = f'<section class="frame" id="invalid" data-slices="{count}" style="width:1080px;height:1350px;background:white">Invalid count</section>'
            r, images = self.render(body, 'invalid-' + str(i))
            if r.returncode == 0:
                bad.append({'count': count, 'outputs': len(images)})
        self.assertFalse(bad, f'Invalid counts accepted: {bad}')

    def test_QT25_story_text_avoids_top_and_bottom_overlays(self):
        bad = []
        for tag, y in (('top', 100), ('bottom', 1690)):
            r = self.qa(self.fixture(tag, size=(1080, 1920), xy=(80, y)), fmt='story', tag=tag)
            if r.returncode == 0:
                bad.append(tag)
        self.assertFalse(bad, f'Story safe-zone violations accepted: {bad}')

    def test_QT25_story_central_text_is_accepted(self):
        self.assertEqual(self.qa(self.fixture('center', size=(1080, 1920), xy=(80, 800)), fmt='story').returncode, 0)

    def test_QT26_timestamp_corner_text_is_rejected_for_the_right_reason(self):
        r = self.qa(self.fixture('timestamp', size=(1280, 720), xy=(1100, 620), box=[1100, 620, 1250, 710]), fmt='thumb')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('duration-badge', r.stdout)

class EvidenceResult(unittest.TextTestResult):
    def startTest(self, test):
        self._started = time.perf_counter()
        super().startTest(test)

    def record(self, test, state, error=None):
        OUTCOMES.append({'test': test.id().split('.')[-1], 'case': test._testMethodName.split('_')[1], 'status': state, 'elapsed_seconds': time.perf_counter() - self._started, 'error': self._exc_info_to_string(error, test) if error else None})

    def addSuccess(self, test):
        self.record(test, 'PASS')
        super().addSuccess(test)

    def addFailure(self, test, error):
        self.record(test, 'FAIL', error)
        super().addFailure(test, error)

    def addError(self, test, error):
        self.record(test, 'ERROR', error)
        super().addError(test, error)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Contracts)
    if ARGS.only:
        suite = unittest.TestSuite(t for t in suite if t._testMethodName.split('_')[1] in ARGS.only)
    runner = unittest.TextTestRunner(verbosity=2, resultclass=EvidenceResult)
    result = runner.run(suite)
    source_hashes = {str(p.relative_to(SOURCE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SOURCE.rglob('*')) if p.is_file() and 'node_modules' not in p.parts and '__pycache__' not in p.parts}
    save_json(OUT / 'results.json', {'created_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'skill': str(SOURCE), 'source_files': source_hashes, 'tests': OUTCOMES, 'commands': EXECUTIONS, 'tests_run': result.testsRun, 'passed': result.testsRun - len(result.failures) - len(result.errors), 'failed': len(result.failures), 'errors': len(result.errors), 'complete_28_case_gate': False, 'note': 'Independent technical contracts only. Red tests on a frozen baseline are findings, not repaired behavior. QT08 and QT25 are partial coverage: HTML font fallback and Reel variants remain untested. Visual/content cases are not implicitly passed.'})
    raise SystemExit(0 if result.wasSuccessful() else 1)
