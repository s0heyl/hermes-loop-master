#!/usr/bin/env python3
"""Score Hermes Loop Master artifacts without executing recorded commands."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from artifact_contract import (
    CONTRACT_VERSION,
    EVIDENCE_HEADER,
    MODE_REQUIREMENTS,
    REQUIRED_HANDOFF_SECTIONS,
    REQUIRED_LOOP_SECTIONS,
    REQUIRED_REVIEW_CHECKS,
)
from security_patterns import SECRET_PATTERNS

PASS_RESULTS = {"pass", "ok", "success"}
MODE_RANK = {"tiny": 0, "standard": 1, "critical": 2}
BEHAVIORAL_GATES = [
    "Positive path",
    "Negative path",
    "Preservation path",
    "Failure path",
    "RED evidence",
    "GREEN evidence",
    "Independent Oracle",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def section(text: str, heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)", text, re.M | re.S
    )
    return match.group(1) if match else ""


def classification_value(loop: str) -> str | None:
    body = section(loop, "## Classification").strip()
    if not body:
        return None
    first = body.splitlines()[0].strip().strip("`*").strip().lower()
    return first


def declared_mode(loop: str) -> str | None:
    value = classification_value(loop)
    return value if value in MODE_RANK else None


def artifact_contract_version(loop: str) -> str | None:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", loop, re.S)
    if not match:
        return None
    version = re.search(r"^contract_version:\s*['\"]?([^'\"\s]+)", match.group(1), re.M)
    return version.group(1) if version else None


def evidence_rows(loop: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for raw in section(loop, "## Evidence Log").splitlines():
        if not raw.strip().startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in raw.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0].lower() == "time" or set(cells[0]) <= {"-", ":"}:
            continue
        rows.append(
            {"time": cells[0], "check": cells[1], "result": cells[2].lower(), "notes": cells[3]}
        )
    return rows


def gate_passes(label: str, rows: list[dict[str, str]]) -> bool:
    needle = label.lower()
    for row in rows:
        claim = f"{row['check']} {row['notes']}".lower()
        if needle not in claim:
            continue
        result = row["result"]
        if label == "RED evidence":
            if result == "fail":
                return True
            continue
        if label == "Independent Oracle" and "oracle unavailable:" in claim:
            if result == "skipped" and len(row["notes"].strip()) >= 12:
                return True
            continue
        if result in PASS_RESULTS:
            return True
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    parser.add_argument("--mode", choices=sorted(MODE_REQUIREMENTS))
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def evaluate(root: Path, requested_mode: str | None, strict: bool) -> dict:
    root = root.resolve()
    candidate = root / ".hermes-loop"
    issues: list[str] = []
    if candidate.is_symlink():
        issues.append(".hermes-loop symlink is not allowed")
        loop_dir = candidate
        loop = handoff = review = ""
    else:
        loop_dir = candidate if candidate.exists() else root
        loop = read(loop_dir / "LOOP.md")
        handoff = read(loop_dir / "HANDOFF.md")
        review = read(loop_dir / "REVIEW.md")

    raw_classification = classification_value(loop)
    declared = declared_mode(loop)
    if raw_classification is not None and declared is None:
        issues.append(f"invalid Classification value: {raw_classification}")
    mode = requested_mode or declared or "standard"
    if requested_mode and declared and MODE_RANK[requested_mode] < MODE_RANK[declared]:
        issues.append(f"cannot downgrade declared {declared} mode to {requested_mode}")
        mode = declared

    base_result = {
        "contract_version": CONTRACT_VERSION,
        "root": str(root),
        "mode": mode,
        "strict": strict,
        "score": 0,
        "max_score": 0,
        "ratio": 1.0,
        "behavioral_gates_passed": 0,
        "behavioral_gates_required": 0,
        "issues": issues,
        "secret_hits": [],
        "passed": not issues,
    }
    if mode == "tiny" and not MODE_REQUIREMENTS["tiny"]["full_artifacts"]:
        return base_result

    score = 0
    max_score = 0

    version = artifact_contract_version(loop)
    max_score += 1
    if version == CONTRACT_VERSION:
        score += 1
    else:
        issues.append(
            f"LOOP.md contract_version must be {CONTRACT_VERSION}; found {version or 'missing'}"
        )

    max_score += len(REQUIRED_LOOP_SECTIONS)
    for required in REQUIRED_LOOP_SECTIONS:
        if required in loop:
            score += 1
        else:
            issues.append(f"LOOP.md missing section: {required}")

    done_lines = re.findall(r"^- \[([ xX])\] .+", section(loop, "## Done When"), re.M)
    done_complete = bool(done_lines) and all(mark.lower() == "x" for mark in done_lines)
    max_score += 1
    if done_complete:
        score += 1
    elif not done_lines:
        issues.append("LOOP.md Done When has no checkbox conditions")
    else:
        issues.append("LOOP.md Done When has unchecked conditions")

    rows = evidence_rows(loop)
    max_score += 2
    if EVIDENCE_HEADER in loop:
        score += 1
    else:
        issues.append("LOOP.md Evidence Log header does not match the contract")
    if rows and any(row["result"] in PASS_RESULTS | {"fail", "blocked", "skipped"} for row in rows):
        score += 1
    else:
        issues.append("LOOP.md Evidence Log has no structured result row")

    max_score += 1
    active_text = section(loop, "## Active Slice").strip()
    plan_text = section(loop, "## Plan")
    active_plan_items = re.findall(r"^- \[>\] .+", plan_text, re.M)
    open_plan_items = re.findall(r"^- \[ \] .+", plan_text, re.M)
    completed_marker = active_text.lower().rstrip(".") in {"none — complete", "none - complete"}
    if done_complete:
        if not active_plan_items and not open_plan_items and completed_marker:
            score += 1
        else:
            issues.append("completed loop must have no active/open Plan items and Active Slice 'None — complete.'")
    elif len(active_plan_items) == 1 and active_text and not completed_marker:
        score += 1
    else:
        issues.append("incomplete loop must have exactly one [>] Plan item and one Active Slice")

    max_score += len(REQUIRED_HANDOFF_SECTIONS)
    for required in REQUIRED_HANDOFF_SECTIONS:
        if required in handoff:
            score += 1
        else:
            issues.append(f"HANDOFF.md missing section: {required}")

    max_score += len(REQUIRED_REVIEW_CHECKS) + 1
    review_lower = review.lower()
    for label in REQUIRED_REVIEW_CHECKS:
        if f"- [x] {label.lower()}" in review_lower:
            score += 1
        else:
            issues.append(f"REVIEW.md unchecked fake-done item: {label}")
    verdict = section(review, "## Verdict").strip().splitlines()
    if verdict and verdict[0].strip().lower() == "pass":
        score += 1
    else:
        issues.append("REVIEW.md verdict must be pass")

    features_path = loop_dir / "FEATURES.json"
    if features_path.exists() and not features_path.is_symlink():
        max_score += 1
        try:
            data = json.loads(features_path.read_text(encoding="utf-8"))
            valid = (
                isinstance(data, list)
                and bool(data)
                and all(
                    isinstance(item, dict) and isinstance(item.get("passes"), bool)
                    for item in data
                )
            )
            if valid:
                score += 1
            else:
                issues.append("FEATURES.json must be a non-empty list of objects with boolean passes")
        except Exception as exc:
            issues.append(f"FEATURES.json invalid JSON: {exc}")

    required_gates = []
    if MODE_REQUIREMENTS[mode]["requires_red_green"]:
        required_gates.extend(["RED evidence", "GREEN evidence"])
    if mode == "critical":
        required_gates = BEHAVIORAL_GATES
    max_score += len(required_gates)
    behavioral_passed = 0
    for label in required_gates:
        if gate_passes(label, rows):
            score += 1
            behavioral_passed += 1
        else:
            issues.append(f"{mode} evidence missing or invalid: {label}")

    max_score += 1
    secret_hits: list[str] = []
    if loop_dir.exists() and not loop_dir.is_symlink():
        for path in loop_dir.rglob("*"):
            if path.is_symlink() or not path.is_file() or path.stat().st_size > 1_000_000:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if any(pattern.search(text) for pattern in SECRET_PATTERNS):
                secret_hits.append(str(path.relative_to(loop_dir)))
    if secret_hits:
        issues.append("possible secrets found: " + ", ".join(secret_hits))
    else:
        score += 1

    ratio = score / max_score if max_score else 1.0
    passed = ratio >= 0.8 and not secret_hits
    if strict and issues:
        passed = False
    return {
        **base_result,
        "score": score,
        "max_score": max_score,
        "ratio": round(ratio, 6),
        "behavioral_gates_passed": behavioral_passed,
        "behavioral_gates_required": len(required_gates),
        "issues": issues,
        "secret_hits": secret_hits,
        "passed": passed,
    }


def main() -> int:
    args = parse_args()
    result = evaluate(Path(args.root), args.mode, args.strict)
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Score: {result['score']}/{result['max_score']} ({result['ratio']:.0%}) mode={result['mode']}")
        if result["issues"]:
            print("Issues:")
            for issue in result["issues"]:
                print(f"- {issue}")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
