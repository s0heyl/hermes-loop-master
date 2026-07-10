#!/usr/bin/env python3
"""Validate a Hermes/Agent Skills SKILL.md file."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from security_patterns import SECRET_PATTERNS

REQUIRED_HEADINGS = [
    "# Hermes Loop Master",
    "## Overview",
    "## When to Use",
    "## Verification Checklist",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    sys.exit(1)


def parse_top_level_frontmatter(text: str) -> dict[str, str]:
    """Parse the scalar top-level keys needed by the validator.

    Agent Skills frontmatter can contain nested YAML, but validation only needs
    its top-level scalar metadata. Keeping this parser narrow removes an
    installer-time dependency without pretending to implement all of YAML.
    """
    result: dict[str, str] = {}
    for number, line in enumerate(text.splitlines(), 1):
        if not line or line[:1].isspace() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"malformed top-level line {number}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in result:
            raise ValueError(f"invalid or duplicate top-level key on line {number}")
        if value:
            result[key] = value.strip("'\"")
    return result


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "SKILL.md")
    if not path.exists():
        fail(f"not found: {path}")

    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("frontmatter must start at byte 0 with ---")

    match = re.search(r"\n---\s*\n", text[4:])
    if not match:
        fail("frontmatter closing --- not found")

    # match indexes are relative to text[4:]
    close_start = match.start() + 4
    frontmatter = text[4:close_start]
    body = text[match.end() + 4 :]

    try:
        meta = parse_top_level_frontmatter(frontmatter)
    except ValueError as exc:
        fail(f"frontmatter parse error: {exc}")

    if not isinstance(meta, dict):
        fail("frontmatter must parse to a mapping")

    for key in ["name", "description", "version", "author", "license"]:
        if not meta.get(key):
            fail(f"missing frontmatter key: {key}")

    name = str(meta["name"])
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
        fail("name must be lowercase kebab-case and <=64 characters")

    description = str(meta["description"])
    if len(description) > 1024:
        fail("description exceeds 1024 characters")
    if not description.startswith("Use when "):
        fail("description should start with 'Use when '")

    if not body.strip():
        fail("body is empty")
    if len(text) > 100_000:
        fail("SKILL.md exceeds 100,000 characters")

    for heading in REQUIRED_HEADINGS:
        if heading not in body:
            fail(f"missing required heading: {heading}")

    forbidden = [
        "api_key=",
        "BEGIN PRIVATE KEY",
        "gho_",
        "PRIVATE_PROJECT_NAME_PLACEHOLDER_SHOULD_NOT_APPEAR",
    ]
    lowered = text.lower()
    for needle in forbidden:
        if needle.lower() in lowered:
            fail(f"forbidden/private pattern found: {needle}")

    for pattern in SECRET_PATTERNS:
        if pattern.search(text):
            fail(f"possible secret pattern found: {pattern.pattern}")

    local_path_patterns = [
        r"/home/[^\s/]+/[^\s]+",
        r"/Users/[^\s/]+/[^\s]+",
        r"(?i)\b[A-Z]:[\\/]Users[\\/][^\\/\s]+[\\/][^\s]+",
    ]
    for pattern in local_path_patterns:
        if re.search(pattern, text):
            fail(f"possible local path pattern found: {pattern}")

    print(f"OK: {path} is a valid Hermes skill ({len(text)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
