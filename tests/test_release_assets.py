import pathlib
import subprocess
import tempfile
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]


class ReleaseAssetTests(unittest.TestCase):
    def test_version_is_synchronized(self):
        skill = (ROOT / "SKILL.md").read_text()
        frontmatter = yaml.safe_load(skill.split("---", 2)[1])
        self.assertEqual(frontmatter["version"], "1.4.0")
        self.assertIn("## [1.4.0]", (ROOT / "CHANGELOG.md").read_text())
        self.assertIn("v1.4.0", (ROOT / "README.md").read_text())

    def test_ci_runs_full_public_quality_gate(self):
        workflow_path = ROOT / ".github" / "workflows" / "quality.yml"
        workflow = workflow_path.read_text()
        for command in [
            "python -m unittest discover -s tests -v",
            "python scripts/validate_skill.py SKILL.md",
            "python scripts/harness_check.py --strict --mode standard examples/good-loop",
            "python scripts/harness_check.py --strict --mode critical examples/critical-loop",
            "bash install.sh --dry-run",
        ]:
            self.assertIn(command, workflow)

    def test_installer_dry_run_target_and_force_are_safe(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "installed-skill"
            dry = subprocess.run(
                ["bash", "install.sh", "--target", str(target), "--dry-run"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
            self.assertFalse(target.exists())

            first = subprocess.run(
                ["bash", "install.sh", "--target", str(target)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            self.assertTrue((target / "SKILL.md").exists())
            self.assertTrue((target / "references" / "behavioral-verification.md").exists())

            second = subprocess.run(
                ["bash", "install.sh", "--target", str(target)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("--force", second.stderr)

            forced = subprocess.run(
                ["bash", "install.sh", "--target", str(target), "--force"],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(forced.returncode, 0, forced.stdout + forced.stderr)


if __name__ == "__main__":
    unittest.main()
