"""Dependency-free signed webhook example used by the Critical fixture."""
import hashlib
import hmac


def sign(secret: bytes, timestamp: int, body: bytes) -> str:
    return hmac.new(secret, str(timestamp).encode() + b"." + body, hashlib.sha256).hexdigest()


def verify(secret: bytes, now: int, body: bytes, header: str, tolerance: int = 300) -> bool:
    try:
        fields = [part.strip() for part in header.split(",")]
        timestamps = [int(part[2:]) for part in fields if part.startswith("t=")]
        signatures = [part[3:] for part in fields if part.startswith("v1=")]
    except (AttributeError, TypeError, ValueError):
        return False
    if len(timestamps) != 1 or not signatures:
        return False
    timestamp = timestamps[0]
    if abs(now - timestamp) > tolerance:
        return False
    expected = sign(secret, timestamp, body)
    return any(hmac.compare_digest(expected, candidate) for candidate in signatures)
