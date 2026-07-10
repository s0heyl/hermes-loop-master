import pathlib
import subprocess
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_skill.py"
BASE_SKILL = (ROOT / "SKILL.md").read_text()


class ValidateSkillTests(unittest.TestCase):
    def run_validator(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "SKILL.md"
            path.write_text(text)
            return subprocess.run(
                ["python", str(VALIDATOR), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )

    def test_hyphenated_prose_does_not_trigger_secret_false_positive(self):
        result = self.run_validator(BASE_SKILL + "\nA restored task-list is only a hypothesis.\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_realistic_openai_style_secret_is_rejected(self):
        fake_secret = "sk-" + "A" * 24
        result = self.run_validator(BASE_SKILL + f"\nLeaked value: {fake_secret}\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("possible secret", result.stderr.lower())

    def test_literal_secret_examples_in_code_are_allowed_when_too_short(self):
        result = self.run_validator(BASE_SKILL + "\nExample prefix: `sk-<redacted>`\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_common_github_and_json_credentials_are_rejected(self):
        samples = [
            "ghp_" + "A" * 36,
            "github_pat_" + "A" * 30,
            '{"api_key":"' + "B" * 24 + '"}',
        ]
        for sample in samples:
            with self.subTest(sample=sample[:12]):
                result = self.run_validator(BASE_SKILL + f"\n{sample}\n")
                self.assertEqual(result.returncode, 1)
                self.assertIn("possible secret", result.stderr.lower())

    def test_windows_user_path_is_rejected(self):
        result = self.run_validator(BASE_SKILL + "\nC:\\Users\\Alice\\secret.txt\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("local path", result.stderr.lower())

    def test_validator_runs_without_pyyaml_site_package(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "SKILL.md"
            path.write_text(BASE_SKILL)
            result = subprocess.run(
                ["python", "-S", str(VALIDATOR), str(path)],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
