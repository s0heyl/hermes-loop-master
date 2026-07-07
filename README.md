# Hermes Loop Master

```text
╔════════════════════════════════════════════════════════════════════╗
║  0101  SPEC  →  SLICE  →  VERIFY  →  REVIEW  →  HANDOFF  1010   ║
║                                                                    ║
║           _____   _____   _____       _______ _______              ║
║    |     |     | |     | |_____]      |  |  | |_____|              ║
║    |____ |_____| |_____| |            |  |  | |     |              ║
║                                                                    ║
║              M A T R I X   L O O P   F O R   H E R M E S          ║
╚════════════════════════════════════════════════════════════════════╝
```

**A Hermes-native skill for systematic coding loops, real verification, and clean agent handoffs.**

[![Release](https://img.shields.io/github/v/release/s0heyl/hermes-loop-master?style=for-the-badge)](https://github.com/s0heyl/hermes-loop-master/releases)
[![License](https://img.shields.io/github/license/s0heyl/hermes-loop-master?style=for-the-badge)](LICENSE)
[![Stars](https://img.shields.io/github/stars/s0heyl/hermes-loop-master?style=for-the-badge)](https://github.com/s0heyl/hermes-loop-master/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/s0heyl/hermes-loop-master?style=for-the-badge)](https://github.com/s0heyl/hermes-loop-master/commits/main)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-7c3aed?style=for-the-badge)](https://hermes-agent.nousresearch.com/docs)
[![Agent Skills](https://img.shields.io/badge/SKILL.md-Agent%20Skills-00c853?style=for-the-badge)](https://agentskills.io/)
[![No API Keys](https://img.shields.io/badge/API%20Keys-Not%20Required-00bcd4?style=for-the-badge)](#safety)
[![Verification](https://img.shields.io/badge/Verification-Real%20Commands-ff9800?style=for-the-badge)](#real-test-results)

---

## 🇬🇧 English

### What is it?

Hermes Loop Master is a **coding-agent discipline skill**. It stops an agent from jumping straight into code and calling work done too early.

It forces a simple loop:

```text
SPEC → ONE SLICE → REAL TEST → ADVERSARIAL REVIEW → CLEAN HANDOFF
```

### Why use it?

Use it when a coding task is:

- 🐞 a real bug fix,
- 🚀 a multi-step feature,
- 🔐 security/auth/payment/data sensitive,
- 🧹 a refactor with scope-creep risk,
- 🌍 public/open-source work,
- 🧠 likely to continue across multiple sessions.

### Core features

| Feature | What it does |
|---|---|
| 🧾 **Spec-first** | Writes Goal, Done When, Non-goals, Never Touch, Stop If before editing. |
| ✂️ **One-slice work** | Implements only one small, testable change at a time. |
| ✅ **Real verification** | Records actual test/lint/build/smoke command output. |
| 🕵️ **Adversarial review** | Checks for fake-done patterns, weak tests, scope creep, and secret leaks. |
| 🔁 **Clean handoff** | Creates resumable state for the next agent/session. |
| 🧼 **Repo hygiene** | Catches generated files, local paths, and unsafe public artifacts. |

### Install

```bash
git clone https://github.com/s0heyl/hermes-loop-master.git
cd hermes-loop-master
./install.sh
```

Then start a fresh Hermes session and ask:

```text
Use Hermes Loop Master.
Create LOOP.md, implement one slice, run real verification,
write REVIEW.md and HANDOFF.md, then stop.
```

### Project files

```text
.hermes-loop/
├── LOOP.md      # Goal, Done When, plan, evidence log
├── REVIEW.md    # Fake-done / secret / scope review
└── HANDOFF.md   # What changed, evidence, risks, next step
```

---

## 🇮🇷 فارسی

### این چیه؟

**Hermes Loop Master** یک اسکیل برای کدنویسی سیستماتیک با Hermes است. کاری می‌کند Agent قبل از کدنویسی، هدف و معیار Done را واضح کند، فقط یک بخش کوچک را تغییر دهد، تست واقعی بگیرد، diff را بدبینانه بررسی کند و در پایان handoff تمیز بنویسد.

حلقه اصلی:

```text
مشخصات کار → یک تغییر کوچک → تست واقعی → بازبینی بدبینانه → تحویل تمیز
```

### کی استفاده کنیم؟

برای این کارها عالی است:

- 🐞 باگ واقعی که باید reproduce شود؛
- 🚀 فیچر چندمرحله‌ای؛
- 🔐 تغییرات حساس مثل auth، payment، data، migration؛
- 🧹 refactorهایی که ممکن است از کنترل خارج شوند؛
- 🌍 ریپوهای public یا PRهای قابل بررسی؛
- 🧠 کارهایی که ممکن است چند session طول بکشند.

### ویژگی‌ها

| ویژگی | کاربرد |
|---|---|
| 🧾 **Spec-first** | قبل از تغییر کد، Goal و Done When و Non-goals نوشته می‌شود. |
| ✂️ **One-slice** | هر بار فقط یک تغییر کوچک و قابل تست انجام می‌شود. |
| ✅ **تست واقعی** | خروجی واقعی تست/لینت/بیلد ثبت می‌شود؛ خروجی خیالی ممنوع. |
| 🕵️ **Review بدبینانه** | Done الکی، تست ضعیف، scope creep و secret leak بررسی می‌شود. |
| 🔁 **Handoff تمیز** | session بعدی بدون حدس‌زدن ادامه می‌دهد. |
| 🧼 **بهداشت ریپو** | فایل generated، مسیر لوکال و چیزهای private کمتر وارد commit می‌شوند. |

### پرامپت آماده

```text
با Hermes Loop Master این تسک را انجام بده.
اول .hermes-loop/LOOP.md را کامل کن.
فقط یک slice انجام بده.
تست واقعی بگیر.
REVIEW.md و HANDOFF.md را کامل کن و بعد متوقف شو.
```

---

## 🧪 Real test results

### Built-in fixture check

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
```

| Fixture | Result | Meaning |
|---|---:|---|
| ✅ `good-loop` | `28/28` | Complete loop: spec, evidence, review, handoff. |
| ❌ `bad-loop` | `9/27` | Missing Non-goals, evidence, review checks, handoff fields. |

### Real bug-fix smoke test

Buggy code accepted only exact coupon text:

```python
def final_price(price, coupon=None):
    if coupon == "SAVE10":
        return price * 0.9
    return price
```

Expected:

```python
final_price(100, " save10 ") == 90
```

Before fix:

```text
1 failed, 2 passed
AssertionError: assert 100 == 90
```

After one-slice fix:

```python
normalized_coupon = coupon.strip().upper() if isinstance(coupon, str) else coupon
```

Final evidence:

```text
3 passed in 0.09s
git diff --check → ok
harness_check.py . → Score: 27/27 (100%)
```

Bonus signal: the loop also caught accidentally tracked `__pycache__` files and cleaned them from git.

---

## 📦 Repository contents

```text
.
├── SKILL.md
├── install.sh
├── templates/
│   ├── LOOP.md
│   ├── REVIEW.md
│   ├── HANDOFF.md
│   └── FEATURES.json
├── scripts/
│   ├── validate_skill.py
│   └── harness_check.py
├── examples/
│   ├── good-loop/
│   └── bad-loop/
├── CONTRIBUTING.md
├── SECURITY.md
└── LICENSE
```

---

## 🔐 Safety

Hermes Loop Master:

- does **not** need API keys;
- does **not** install MCP servers;
- does **not** grant extra permissions;
- does **not** replace CI, code review, or human judgment;
- does **not** make destructive commands safe automatically.

Keep public contributions generic: no private paths, customer data, credentials, private chat logs, or proprietary prompts.

---

## 🛠️ Roadmap

- [ ] GitHub Actions CI for skill + fixture validation
- [ ] Python / Node / Flutter / Go / Rust verification recipes
- [ ] Better diff classifier for generated files and weakened tests
- [ ] More real examples: API, UI state, authz negative test, migration dry run
- [ ] Safer installer with `--dry-run`, `--force`, and `--target`

---

## 🤝 Contributing

Contributions are welcome. Keep changes public-safe and evidence-backed.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT — see [LICENSE](LICENSE).
