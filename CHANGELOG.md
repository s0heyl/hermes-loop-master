# Changelog

## [1.4.0] - 2026-07-10

Adaptive verification and measurable quality upgrade:

- Added Tiny, Standard, and Critical execution modes with explicit efficiency targets.
- Added a canonical artifact contract shared by the skill, templates, and harness.
- Added Critical behavioral gates for positive, negative, preservation, and failure paths.
- Added RED/GREEN evidence and Independent Oracle guidance for high-risk work.
- Added strict and JSON harness output plus a 100% Critical fixture.
- Fixed secret-scanner false positives for ordinary text such as `task-list`.
- Added deterministic benchmark comparison tooling with correctness regression gates.
- Added unit tests and GitHub Actions quality checks.
- Added atomic Bash installer staging with `--target`, `--dry-run`, `--force`, recognized-target protection, backup, and rollback.
- Added a PowerShell installer for Windows.
- Removed the runtime PyYAML dependency from skill validation.
- Added a runnable Critical webhook fixture with deterministic oracle vectors.

## 1.3.0 - 2026-07-07

README redesign:

- Reworked README into shorter, cleaner English and Persian sections.
- Added cyberpunk/matrix loop ASCII banner.
- Expanded badge set for release, license, stars, last commit, Hermes, Agent Skills, no API keys, and real verification.
- Simplified feature tables, install instructions, safety notes, and roadmap.
- Kept real test evidence with concise examples.

## 1.2.0 - 2026-07-07

Repository rename and branding update:

- Renamed public repository to `hermes-loop-master`.
- Updated public title to **Hermes Loop Master**.
- Updated install paths, README links, scripts, and skill metadata.
- Kept the workflow and validation behavior unchanged.

## 1.1.0 - 2026-07-07

Documentation upgrade:

- Expanded README with English and Persian explanations.
- Added keyword-rich feature sections for discoverability.
- Added real test result section with fixture scores and a concrete bug-fix example.
- Added example prompts in English and Persian.
- Added a public improvement roadmap for contributors.

## 1.0.1 - 2026-07-07

Public hygiene fix:

- Removed environment-specific validator examples.
- Kept validator checks generic and public-safe.

## 1.0.0 - 2026-07-07

Initial public release:

- Hermes-native `SKILL.md` for spec-first coding loops.
- Project-local loop templates: `LOOP.md`, `HANDOFF.md`, `REVIEW.md`, `FEATURES.json`.
- Validation scripts for skill metadata and loop artifact quality.
- Good and bad fixtures for real smoke testing.
- Public-safe contribution and security guidelines.
