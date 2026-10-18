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
