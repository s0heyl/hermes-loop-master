import json
import pathlib
import sys
import unittest

PROJECT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))
from webhook import sign, verify

FIXTURE_KEY = b"public-fixture-secret"
NOW = 1_700_000_000
BODY = b'{"event":"invoice.paid"}'


class WebhookTests(unittest.TestCase):
    def header(self, timestamp=NOW, signature=None):
        signature = signature or sign(FIXTURE_KEY, timestamp, BODY)
        return f"t={timestamp},v1={signature}"

    def test_positive_path(self):
        self.assertTrue(verify(FIXTURE_KEY, NOW, BODY, self.header()))

    def test_negative_and_failure_paths(self):
        self.assertFalse(verify(FIXTURE_KEY, NOW, BODY, self.header(signature="0" * 64)))
        self.assertFalse(verify(FIXTURE_KEY, NOW, BODY, "malformed"))

    def test_preservation_multiple_signatures(self):
        valid = sign(FIXTURE_KEY, NOW, BODY)
        self.assertTrue(verify(FIXTURE_KEY, NOW, BODY, f"t={NOW},v1={'0' * 64},v1={valid}"))

    def test_replay_boundaries(self):
        self.assertFalse(verify(FIXTURE_KEY, NOW, BODY, self.header(NOW - 301)))
        self.assertTrue(verify(FIXTURE_KEY, NOW, BODY, self.header(NOW - 300)))

    def test_independent_oracle_vector(self):
        vector = json.loads((PROJECT / "oracle_vectors.json").read_text())[0]
        self.assertEqual(sign(vector["key"].encode(), vector["timestamp"], vector["body"].encode()), vector["signature"])


if __name__ == "__main__":
    unittest.main()
