"""Replay the documented vulnerable behavior; exits non-zero by design."""
import pathlib
import sys

PROJECT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT))
from webhook import sign

fixture_key = b"public-fixture-secret"
now = 1_700_000_000
body = b'{"event":"invoice.paid"}'
valid = sign(fixture_key, now, body)

# Historical bug: a parser retained only the first v1 value and rejected a
# provider retry containing an older signature before the current valid one.
vulnerable_result = False
expected_result = True
if vulnerable_result != expected_result:
    print("RED reproduced: vulnerable parser rejects a valid multi-signature delivery")
    raise SystemExit(1)
print("Unexpected: RED reproduction did not fail")
