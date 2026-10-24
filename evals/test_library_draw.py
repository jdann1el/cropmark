import json
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
DRAW = REPO / "skills" / "cropmark" / "scripts" / "draw.py"
SKILL = REPO / "skills" / "cropmark"
LIBRARY = SKILL / "library"


class DrawTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.history = self.root / "history.json"
        self.env = os.environ.copy()
        self.env["HOME"] = str(self.home)
        self.env["CROPMARK_HISTORY"] = str(self.history)

    def run_cli(self, args, cwd=None, script=DRAW, env=None):
        return subprocess.run(
            [sys.executable, str(script), *args],
            cwd=cwd or self.root,
            env=env or self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    @staticmethod
    def drawn_ids(output):
        return re.findall(r"^\d+\. ([a-z0-9-]+) —", output, flags=re.M)

    def test_same_seed_and_history_is_deterministic(self):
        self.history.write_text(json.dumps({"picks": [
            {"direction": "frame-system"}, {"direction": "across-the-swipe"}
        ]}), encoding="utf-8")
        args = ["--format", "carousel", "--brief", "example brief", "--seed", "4401", "--options", "3"]
        first = self.run_cli(args)
        second = self.run_cli(args)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(first.stdout, second.stdout)
        self.assertEqual(len(self.drawn_ids(first.stdout)), 3)
        self.assertEqual(first.stdout.count("· Borrow:"), 6)
        self.assertNotRegex(first.stdout, r"T-6|forced[- ]justification|stretch short phrases")

    def test_different_seeds_change_the_deal(self):
        base = ["--format", "carousel", "--brief", "example brief", "--options", "3"]
        first = self.run_cli([*base, "--seed", "201"])
        second = self.run_cli([*base, "--seed", "202"])
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertNotEqual(self.drawn_ids(first.stdout), self.drawn_ids(second.stdout))

    def test_asset_filter_excludes_directions_needing_a_face(self):
        spec = importlib.util.spec_from_file_location("cropmark_draw", DRAW)
        draw = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = draw
        spec.loader.exec_module(draw)
        directions = json.loads((LIBRARY / "directions.json").read_text(encoding="utf-8"))["directions"]
        input_data = {"format": "thumbnail", "have": ["product-photo"], "tone": None, "avoid": []}
        pool, feasible, notes = draw.candidate_pool(directions, input_data)
        by_id = {d["id"]: d for d in directions}
        self.assertEqual({d["id"] for d in feasible}, {"artefact-in-scene", "duel"})
        self.assertTrue(all("face-photo" not in by_id[item]["needs"] for item in (d["id"] for d in feasible)))
        self.assertTrue(any("Widened" in note for note in notes))
        result = self.run_cli([
            "--format", "thumbnail", "--brief", "example brief", "--have", "product-photo", "--seed", "33", "--options", "3"
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        ids = self.drawn_ids(result.stdout)
        self.assertEqual(len(ids), 3)
        self.assertIn("Widened from 2 asset-feasible direction(s)", result.stdout)

    def test_history_avoidance_prefers_directions_outside_last_five(self):
        directions = json.loads((LIBRARY / "directions.json").read_text(encoding="utf-8"))["directions"]
        carousel = [d for d in directions if "carousel" in d["formats"]]
        recent = [d["id"] for d in carousel[:5]]
        self.history.write_text(json.dumps({"picks": [{"direction": item} for item in recent]}), encoding="utf-8")
        result = self.run_cli([
            "--format", "carousel", "--brief", "example brief", "--have", "product-photo,brand-asset", "--seed", "101", "--options", "3"
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(self.drawn_ids(result.stdout)), 3)
        self.assertTrue(set(self.drawn_ids(result.stdout)).isdisjoint(recent), result.stdout)

    def test_redraw_without_reason_fails(self):
        result = self.run_cli(["--redraw", "direction"])
        self.assertEqual(result.returncode, 2)
        self.assertIn("--redraw requires --reason", result.stderr)

    def test_choice_and_redraw_reasons_are_recorded(self):
        base = ["--format", "carousel", "--brief", "example brief", "--seed", "4401"]
        deal = self.run_cli([*base, "--options", "3"])
        self.assertEqual(deal.returncode, 0, deal.stderr)
        choose = self.run_cli([
            *base, "--direction", "type-is-the-image", "--why", "It carries the catalog inventory as typography."
        ])
        self.assertEqual(choose.returncode, 0, choose.stderr)
        state_path = self.root / ".cropmark" / "direction.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["choice"]["direction"], "type-is-the-image")
        self.assertEqual(state["reason"], "It carries the catalog inventory as typography.")
        self.assertEqual(state["redraw_count"], 0)
        style = self.run_cli(["--redraw", "style", "--reason", "Test a different existing style card."])
        self.assertEqual(style.returncode, 0, style.stderr)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["redraw_count"], 1)
        self.assertEqual(state["redraw_reasons"][0]["reason"], "Test a different existing style card.")
        direction = self.run_cli(["--redraw", "direction", "--reason", "Test another composition engine."])
        self.assertEqual(direction.returncode, 0, direction.stderr)
        state = json.loads(state_path.read_text(encoding="utf-8"))
        self.assertEqual(state["redraw_count"], 2)
        self.assertEqual(state["redraw_reasons"][1]["reason"], "Test another composition engine.")
        self.assertNotEqual(state["choice"]["direction"], "type-is-the-image")

    def test_real_library_check_and_json_schema(self):
        result = self.run_cli(["--check"])
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Library check passed: 21 refs, 12 directions.", result.stdout)
        refs = json.loads((LIBRARY / "refs.json").read_text(encoding="utf-8"))
        directions = json.loads((LIBRARY / "directions.json").read_text(encoding="utf-8"))
        self.assertEqual(len(refs["refs"]), 21)
        self.assertEqual(len(directions["directions"]), 12)

    def test_check_rejects_broken_json_fixture(self):
        fixture = self.root / "cropmark"
        shutil.copytree(SKILL / "scripts", fixture / "scripts")
        shutil.copytree(SKILL / "styles", fixture / "styles")
        (fixture / "library").mkdir()
        refs = json.loads((LIBRARY / "refs.json").read_text(encoding="utf-8"))
        directions = json.loads((LIBRARY / "directions.json").read_text(encoding="utf-8"))
        refs["refs"][0].pop("title")
        refs["refs"][1]["imagery"] += " https://cdn.example.invalid/study.png"
        (fixture / "library" / "refs.json").write_text(json.dumps(refs), encoding="utf-8")
        (fixture / "library" / "directions.json").write_text(json.dumps(directions), encoding="utf-8")
        result = self.run_cli(["--check"], script=fixture / "scripts" / "draw.py")
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing required fields: title", result.stderr)
        self.assertIn("image or CDN URL found", result.stderr)


if __name__ == "__main__":
    unittest.main()
