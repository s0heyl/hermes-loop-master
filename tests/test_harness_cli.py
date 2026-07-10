import json
import pathlib
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HARNESS = ROOT / "scripts" / "harness_check.py"


class HarnessCliTests(unittest.TestCase):
    def run_harness(self, *args):
        return subprocess.run(
            ["python", str(HARNESS), *map(str, args)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_json_output_is_machine_readable(self):
        result = self.run_harness("--json", "--mode", "standard", ROOT / "examples" / "good-loop")
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["passed"])
        self.assertEqual(data["mode"], "standard")
        self.assertEqual(data["contract_version"], "1.0")
        self.assertEqual(data["score"], data["max_score"])

    def test_critical_fixture_passes_strict_behavioral_gates(self):
        result = self.run_harness("--json", "--strict", "--mode", "critical", ROOT / "examples" / "critical-loop")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["passed"])
        self.assertEqual(data["behavioral_gates_passed"], 7)
        self.assertEqual(data["behavioral_gates_required"], 7)

    def test_standard_fixture_fails_when_forced_into_critical_mode(self):
        result = self.run_harness("--json", "--strict", "--mode", "critical", ROOT / "examples" / "good-loop")
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertFalse(data["passed"])
        self.assertTrue(any("critical evidence missing" in issue for issue in data["issues"]))

    def test_strict_mode_fails_on_any_contract_issue(self):
        result = self.run_harness("--json", "--strict", "--mode", "standard", ROOT / "examples" / "bad-loop")
        self.assertEqual(result.returncode, 1)
        data = json.loads(result.stdout)
        self.assertFalse(data["passed"])
        self.assertGreater(len(data["issues"]), 0)

    def test_critical_keywords_outside_evidence_rows_do_not_pass(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "loop"
            shutil.copytree(ROOT / "examples" / "good-loop", target)
            with (target / "LOOP.md").open("a") as stream:
                stream.write("\n<!-- Positive path Negative path Preservation path Failure path RED evidence GREEN evidence Independent Oracle -->\n")
            result = self.run_harness("--json", "--strict", "--mode", "critical", target)
            self.assertEqual(result.returncode, 1)
            self.assertLess(json.loads(result.stdout)["behavioral_gates_passed"], 7)

    def test_unchecked_done_when_and_blocked_verdict_fail_strict(self):
        import shutil
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "loop"
            shutil.copytree(ROOT / "examples" / "critical-loop", target)
            loop = (target / "LOOP.md").read_text().replace("- [x] Forged", "- [ ] Forged", 1)
            (target / "LOOP.md").write_text(loop)
            review = (target / "REVIEW.md").read_text().replace("## Verdict\npass", "## Verdict\nblocked")
            (target / "REVIEW.md").write_text(review)
            result = self.run_harness("--json", "--strict", target)
            self.assertEqual(result.returncode, 1)
            issues = json.loads(result.stdout)["issues"]
            self.assertTrue(any("unchecked" in issue for issue in issues))
            self.assertTrue(any("verdict must be pass" in issue for issue in issues))

    def test_cli_cannot_downgrade_declared_critical_mode(self):
        result = self.run_harness("--json", "--strict", "--mode", "standard", ROOT / "examples" / "critical-loop")
        self.assertEqual(result.returncode, 1)
        self.assertTrue(any("cannot downgrade" in issue for issue in json.loads(result.stdout)["issues"]))

    def test_tiny_mode_does_not_require_full_artifacts(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            result = self.run_harness("--json", "--strict", "--mode", "tiny", tmp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(result.stdout)
            self.assertTrue(data["passed"])
            self.assertEqual(data["max_score"], 0)

    def test_symlinked_loop_directory_is_rejected(self):
        import os
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp) / "root"
            outside = pathlib.Path(tmp) / "outside"
            root.mkdir(); outside.mkdir()
            os.symlink(outside, root / ".hermes-loop")
            result = self.run_harness("--json", "--strict", root)
            self.assertEqual(result.returncode, 1)
            self.assertTrue(any("symlink" in issue for issue in json.loads(result.stdout)["issues"]))


if __name__ == "__main__":
    unittest.main()
