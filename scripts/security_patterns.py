#!/usr/bin/env python3
"""Shared high-confidence secret patterns for public-safety checks.

These heuristics reduce obvious leaks; they do not replace a dedicated secret
scanner such as gitleaks or GitHub secret scanning.
"""
from __future__ import annotations

import re

SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\b(?:gho|ghp|ghr|ghs|ghu)_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"(?i)[\"']?(?:api[_-]?key|secret|password|token)[\"']?"
        r"\s*[:=]\s*[\"']?[^\s\"']{12,}"
    ),
]


def contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)
