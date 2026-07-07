# Hermes Loop Mastering

**Hermes-native skill for systematic coding agents, real verification, clean handoffs, and safer long-running software work.**

[![Skill](https://img.shields.io/badge/Hermes-Skill-blue)](https://hermes-agent.nousresearch.com/docs)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-SKILL.md-green)](https://agentskills.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hermes Loop Mastering turns vague coding requests into a disciplined engineering loop:

1. **Spec first** — define the contract before editing.
2. **One slice** — make one smallest meaningful change.
3. **Red → green verification** — prove the bug or requirement with real commands.
4. **Adversarial review** — inspect the diff for fake-done shortcuts.
5. **Clean handoff** — leave durable state for the next session.

It is designed for **Hermes Agent**, but the workflow is plain Markdown + shell-friendly validation, so other coding agents and human teams can use it too.

> Status: public, generic, contribution-friendly. No credentials, private project data, MCP servers, or external API keys are required.

---

## Keywords / کلمات کلیدی

**English:** Hermes Agent skill, AI coding agent, coding workflow, software engineering loop, test-driven development, TDD, red-green-refactor, verification harness, agent handoff, context management, long-running agents, code review checklist, regression tests, secret hygiene, scope control, production-safe coding, autonomous software agents, SKILL.md, Agent Skills.

**فارسی:** اسکیل هرمس، ایجنت کدنویسی، کدنویسی سیستماتیک، تست واقعی، توسعه تست‌محور، حلقه کدنویسی، تحویل تمیز بین سشن‌ها، کنترل کانتکست، جلوگیری از Done الکی، بررسی دیف، امنیت سکرت‌ها، کنترل محدوده کار، دیباگ اصولی، ریفکتور امن، کدنویسی قابل اعتماد با هوش مصنوعی.

---

## فارسی — این اسکیل دقیقاً چه کار می‌کند؟

**Hermes Loop Mastering** برای وقتی است که نمی‌خواهید Agent فقط «کد تولید کند» و بعد با اعتمادبه‌نفس بگوید تمام شد. این اسکیل Agent را مجبور می‌کند قبل از کار، معیار Done را بنویسد؛ بعد فقط یک بخش کوچک را تغییر دهد؛ تست واقعی بگیرد؛ diff را بدبینانه بررسی کند؛ و آخر کار یک handoff تمیز برای ادامه کار بسازد.

### ویژگی‌های اصلی

| ویژگی | توضیح |
|---|---|
| **Spec-first** | قبل از تغییر کد، Goal، Done When، Non-goals، Never Touch و Stop If نوشته می‌شود. |
| **One-slice work** | Agent فقط یک تکه قابل تست را انجام می‌دهد، نه چند کار قاطی. |
| **Real verification** | خروجی واقعی تست/لینت/بیلد/اسموک ثبت می‌شود. خروجی ساختگی ممنوع. |
| **Adversarial review** | diff برای Done الکی، تست ضعیف، scope creep، API خیالی و secret leak بررسی می‌شود. |
| **Clean handoff** | فایل `HANDOFF.md` مشخص می‌کند چه تغییر کرده، چه تستی اجرا شده، ریسک چیست و قدم بعدی چیست. |
| **Context budget** | وضعیت کار در فایل‌ها نگهداری می‌شود، نه فقط داخل چت؛ پس سشن بعدی هم می‌تواند ادامه بدهد. |
| **Public-safe by design** | هیچ نیاز به credential، MCP خارجی، secret یا اطلاعات خصوصی ندارد. |

### چه زمانی استفاده کنیم؟

برای این موارد عالی است:

- باگ واقعی که باید reproduce شود؛
- فیچر چندمرحله‌ای؛
- تغییرات حساس مثل auth، payment، migration یا user data؛
- refactorهایی که احتمال scope creep دارند؛
- PR و ریپوهای public؛
- کارهایی که ممکن است چند session طول بکشد.

برای typo یا تغییر خیلی کوچک، مسیر سبک‌تر **Tiny Change Path** داخل خود skill کافی است.

---

## Why this exists

Coding agents are good at producing code. They are less reliable at knowing when the work is truly done.

Common failure modes:

- solving a nearby problem instead of the requested one,
- making several unrelated changes in one pass,
- weakening tests to get green output,
- declaring success after a build starts but before the feature works,
- losing context across sessions,
- committing generated files, secrets, local paths, or private notes.

Hermes Loop Mastering gives the agent a compact operating system for coding tasks: durable task files, strict verification gates, and explicit stop rules.

---

## Feature map

| Capability | File / mechanism | What it prevents |
|---|---|---|
| Execution contract | `.hermes-loop/LOOP.md` | goal drift, vague Done criteria |
| One-slice plan | `Plan` + `Active Slice` | multi-change spaghetti, context rot |
| Evidence log | `Evidence Log` table | invented test output, premature success |
| Diff review | `.hermes-loop/REVIEW.md` | fake-done shortcuts, weak tests, secret leaks |
| Handoff | `.hermes-loop/HANDOFF.md` | lost context between sessions |
| Harness score | `scripts/harness_check.py` | missing loop artifacts and incomplete verification |
| Skill validation | `scripts/validate_skill.py` | malformed `SKILL.md`, unsafe public patterns |

---

## What is inside

```text
.
├── SKILL.md                         # The Hermes skill
├── templates/
│   ├── LOOP.md                      # Task loop state file
│   ├── FEATURES.json                # Optional feature ledger for long projects
│   ├── HANDOFF.md                   # End-of-session handoff template
│   └── REVIEW.md                    # Adversarial diff review checklist
├── scripts/
│   ├── validate_skill.py            # Validates SKILL.md metadata and structure
│   └── harness_check.py             # Scores loop artifacts in a project
├── examples/
│   ├── good-loop/                   # Example project state that should pass
│   └── bad-loop/                    # Example project state that should fail
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

---

## Install for Hermes

Clone the repository:

```bash
git clone https://github.com/s0heyl/hermes-loop-mastering.git
cd hermes-loop-mastering
```

Install into your local Hermes skills directory:

```bash
./install.sh
```

Or copy manually:

```bash
mkdir -p ~/.hermes/skills/software-development
cp -R hermes-loop-mastering ~/.hermes/skills/software-development/hermes-loop-mastering
```

Start a fresh Hermes session so skills are reloaded, then ask for it explicitly:

```text
Use Hermes Loop Mastering to implement this feature safely.
Create LOOP.md, implement one slice, run real verification, update REVIEW.md and HANDOFF.md, then stop.
```

---

## Quick start in a project

From your project root:

```bash
mkdir -p .hermes-loop
cp /path/to/hermes-loop-mastering/templates/LOOP.md .hermes-loop/LOOP.md
cp /path/to/hermes-loop-mastering/templates/HANDOFF.md .hermes-loop/HANDOFF.md
cp /path/to/hermes-loop-mastering/templates/REVIEW.md .hermes-loop/REVIEW.md
```

Then ask Hermes:

```text
Use Hermes Loop Mastering.
Read .hermes-loop/LOOP.md, fill Goal and Done When, implement exactly one next step, run real verification, update REVIEW.md and HANDOFF.md, and stop.
```

For larger projects, add `FEATURES.json` and let each session complete one entry at a time.

---

## The loop contract

Every coding pass follows this contract:

| Phase | Required evidence |
|---|---|
| Orient | Current branch, dirty state, task file, relevant files read |
| Specify | Goal, Done When, Non-goals, Never Touch, Stop If |
| Plan | 3–7 concrete steps with exactly one active slice |
| Act | Smallest implementation slice; no unrelated cleanup |
| Verify | Real command output: tests, lint/typecheck/build, smoke check as applicable |
| Review | Diff checked against fake-done patterns and secret leakage |
| Handoff | Changed files, commands run, open risks, next recommended step |

---

## Real test result / نتیجه تست واقعی

This repository includes fixture checks, and the skill was also tested on a small real Python bug-fix scenario.

### Built-in fixture test

Command:

```bash
python3 scripts/validate_skill.py SKILL.md
python3 scripts/harness_check.py examples/good-loop
python3 scripts/harness_check.py examples/bad-loop
```

Observed result:

```text
OK: SKILL.md is a valid Hermes skill
GOOD: Score: 28/28 (100%)
BAD:  Score: 9/27 (33%)
bad_issues=18
```

Meaning:

| Fixture | Score | Expected? | Why |
|---|---:|---|---|
| `examples/good-loop` | `28/28` | ✅ Pass | Has Done When, evidence, review checklist, handoff, and no secret hits. |
| `examples/bad-loop` | `9/27` | ✅ Fail | Missing Non-goals, Never Touch, Stop If, evidence, review checklist, and handoff fields. |

### Real bug-fix smoke test

A small Python pricing helper initially accepted only exact uppercase coupon input:

```python
def final_price(price, coupon=None):
    if coupon == "SAVE10":
        return price * 0.9
    return price
```

Expected behavior:

```python
final_price(100, " save10 ") == 90
```

The loop required a regression test first. Before the fix:

```text
1 failed, 2 passed
AssertionError: assert 100 == 90
```

After the one-slice implementation:

```python
normalized_coupon = coupon.strip().upper() if isinstance(coupon, str) else coupon
```

Verification passed:

```text
3 passed in 0.09s
git diff --check → ok
harness_check.py . → Score: 27/27 (100%)
```

The loop also caught a real hygiene issue: generated `__pycache__` files had been accidentally tracked during setup. The final diff removed them from git and added `.gitignore`.

**Practical signal:** the skill did not merely make the code pass; it forced proof, diff review, generated-file cleanup, and a resumable handoff.

---

## Example prompts

### English

```text
Use Hermes Loop Mastering for this bug fix.
First write .hermes-loop/LOOP.md with Goal, Done When, Non-goals, Never Touch, and Stop If.
Add a failing regression test, run it, implement one slice, run verification, write REVIEW.md and HANDOFF.md, then stop.
```

### فارسی

```text
با Hermes Loop Mastering این باگ را درست کن.
اول .hermes-loop/LOOP.md را با Goal، Done When، Non-goals، Never Touch و Stop If کامل کن.
بعد یک تست قرمز اضافه کن، اجراش کن، فقط یک slice را fix کن، تست واقعی بگیر، REVIEW.md و HANDOFF.md را کامل کن و متوقف شو.
```

---

## Included checks

Validate the skill file:

```bash
python3 scripts/validate_skill.py SKILL.md
```

Score a project's loop artifacts:

```bash
python3 scripts/harness_check.py examples/good-loop
python3 scripts/harness_check.py examples/bad-loop
```

Expected behavior:

- `good-loop` passes with a high score.
- `bad-loop` fails and lists missing verification/handoff fields.

---

## What this skill does not do

- It does not grant extra permissions.
- It does not install MCP servers.
- It does not require external API keys.
- It does not claim that prompts alone guarantee correctness.
- It does not replace real tests, CI, code review, or human product judgment.
- It does not make destructive git operations safe; force-push, reset, deletion, production deploys, and paid operations still need explicit approval.

---

## Recommended use cases

- production bug fixes,
- multi-step features,
- refactors with risk of scope creep,
- agent handoffs across sessions,
- security-sensitive changes,
- public/open-source contributions where reviewability matters,
- tasks where a future agent must be able to resume from files rather than chat history.

For one-line edits, use judgment: the full loop may be heavier than necessary. The skill includes a lightweight path for tiny changes.

---

## How it can get better

Good next improvements for contributors:

1. **Language-specific recipes** — Python, Node/TypeScript, Flutter, Go, Rust verification ladders.
2. **CI workflow** — add GitHub Actions for `validate_skill.py` and fixture checks once maintainers have a token with workflow scope.
3. **Open-source benchmark set** — run the skill on small public issues and collect pass/fail evidence.
4. **Diff classifier** — detect generated-file noise, deleted assertions, and broad formatting churn more automatically.
5. **Install UX** — add a safer installer with `--dry-run`, `--force`, and target path options.
6. **More examples** — frontend UI state, API endpoint, authz negative test, migration dry run.
7. **Human checklist mode** — concise printable checklist for teams that want the same loop without an agent.

Contributions are welcome, especially examples with real command output and no private data.

---

## Public safety principles

This repository is intentionally generic:

- no private project names,
- no customer data,
- no credentials,
- no environment-specific paths,
- no private operational notes,
- no copied private prompts.

Please keep contributions public-safe.

---

## Roadmap

- More language-specific verification recipes.
- Optional GitHub Actions workflow once maintainers have appropriate token scopes.
- More example fixtures.
- A small installer that copies templates without overwriting existing files.
- Benchmarks on real open-source tasks.

---

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
