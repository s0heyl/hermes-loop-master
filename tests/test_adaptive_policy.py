import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_contract():
    path = ROOT / "scripts" / "artifact_contract.py"
    spec = importlib.util.spec_from_file_location("artifact_contract", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load contract: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AdaptivePolicyTests(unittest.TestCase):
    def test_mode_requirements_are_machine_readable(self):
        contract = load_contract()
        self.assertEqual(set(contract.MODE_REQUIREMENTS), {"tiny", "standard", "critical"})
        self.assertFalse(contract.MODE_REQUIREMENTS["tiny"]["full_artifacts"])
        self.assertEqual(contract.MODE_REQUIREMENTS["tiny"]["target_tool_calls"], 8)
        self.assertEqual(contract.MODE_REQUIREMENTS["standard"]["target_tool_calls"], 20)
        self.assertTrue(contract.MODE_REQUIREMENTS["critical"]["full_artifacts"])
        self.assertTrue(contract.MODE_REQUIREMENTS["critical"]["requires_oracle"])
        self.assertTrue(contract.MODE_REQUIREMENTS["critical"]["requires_red_green"])

    def test_skill_explains_adaptive_modes_and_budget_overrides(self):
        skill = (ROOT / "SKILL.md").read_text()
        self.assertIn("## Adaptive Modes", skill)
        for mode in ["Tiny", "Standard", "Critical"]:
            self.assertIn(f"**{mode}**", skill)
        self.assertIn("record why the budget was exceeded", skill)
        self.assertIn("references/behavioral-verification.md", skill)

    def test_behavioral_reference_defines_verification_matrix(self):
        reference = (ROOT / "references" / "behavioral-verification.md").read_text()
        for phrase in [
            "Positive path",
            "Negative path",
            "Preservation path",
            "Failure path",
            "RED evidence",
            "GREEN evidence",
            "Independent Oracle",
            "oracle unavailable:",
            "repeated versioned signatures",
            "canonical result token",
            "Security boundary classes",
            "bool` is a subclass of `int",
            "hmac.compare_digest",
        ]:
            self.assertIn(phrase, reference)

    def test_loop_template_uses_three_supported_classifications(self):
        template = (ROOT / "templates" / "LOOP.md").read_text()
        self.assertIn("tiny | standard | critical", template)
        self.assertNotIn("tiny | standard | high-risk", template)


if __name__ == "__main__":
    unittest.main()
