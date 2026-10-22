"""Regression checks for resources required by a standalone installed skill."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('validate_skill',Path(__file__).with_name('validate_skill.py'))
validator=importlib.util.module_from_spec(spec)


class ResourceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec.loader.exec_module(validator)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.skill=self.root/'skill'
        (self.skill/'qa').mkdir(parents=True)
        self.page=self.skill/'qa'/'rubric.md'

    def check(self, text):
        self.page.write_text(text)
        return validator.resource_failures(self.skill)

    def test_external_required_resource_is_rejected_even_when_it_exists(self):
        (self.root/'protocol.md').write_text('experiment')
        for reference in ('see `../../protocol.md`','Read [protocol](../../protocol.md).'):
            with self.subTest(reference=reference):
                self.assertTrue(any('outside skill package' in x for x in self.check(reference)))

    def test_nested_backtick_resource_must_exist(self):
        self.assertTrue(any('missing' in x for x in self.check('Read `missing.md` before review.')))

    def test_explicitly_generated_inline_output_is_not_an_installed_resource(self):
        for verb in ('save','write','create','generate'):
            with self.subTest(verb=verb):
                self.assertEqual(self.check(f'Before rendering, {verb} `direction.md`.'),[])

    def test_output_exception_does_not_hide_read_resource_on_same_line(self):
        text='Save `direction.md`; read `../../protocol.md` and use `templates/direction.md`.'
        failures=self.check(text)
        self.assertEqual(len(failures),2,failures)
        self.assertTrue(any('outside skill package' in x for x in failures))
        self.assertTrue(any('templates/direction.md' in x and 'missing' in x for x in failures))

    def test_reading_output_name_and_writing_template_are_still_checked(self):
        for text in ('Read `direction.md`.','Save `templates/direction.md`.'):
            with self.subTest(text=text):
                self.assertTrue(any('missing' in x for x in self.check(text)))

    def test_local_resources_and_fragment_links_are_valid(self):
        (self.skill/'qa'/'checklist.md').write_text('checks')
        self.assertEqual(self.check('Read `checklist.md` and [checks](checklist.md#review).'),[])

    def test_cli_examples_fenced_code_and_remote_links_are_ignored(self):
        text='''Run `python3 ../../tool.py contract.json`.
For example, `../../example.md` is a placeholder.
```md
Read [demo](../../demo.md) and `../../demo.md`.
```
See [reference](https://example.com/source) and [section](#review).
'''
        self.assertEqual(self.check(text),[])


if __name__=='__main__':unittest.main()
