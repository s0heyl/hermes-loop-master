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

**Current release: v1.4.0**

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
| ⚙️ **Adaptive modes** | Uses Tiny, Standard, or Critical discipline instead of paying full-loop cost for every task. |
| ✂️ **One-slice work** | Implements only one small, testable change at a time. |
| ✅ **Behavioral verification** | Proves positive, negative, preservation, and failure paths with RED/GREEN evidence. |
| 🧭 **Independent Oracle** | Uses an authoritative second runtime or contract for Critical tasks when available. |
| 🕵️ **Adversarial review** | Checks for fake-done patterns, weak tests, scope creep, and secret leaks. |
| 🔁 **Clean handoff** | Creates resumable state for the next agent/session. |
| 🧼 **Repo hygiene** | Catches generated files, local paths, and unsafe public artifacts. |

### Install

```bash
git clone https://github.com/s0heyl/hermes-loop-master.git
cd hermes-loop-master
bash install.sh --dry-run
bash install.sh
```

Use `--target DIR` for an exact install directory. Replacing an existing recognized install requires `--force`; the installer stages and validates the new copy, keeps a timestamped backup, and rolls back on failure.

Windows PowerShell:

```powershell
.\install.ps1 -DryRun
.\install.ps1
```

Then start a fresh Hermes session and ask:

```text
Use Hermes Loop Master.
Create LOOP.md, keep one slice active at a time, verify and review it,
then repeat until Done When passes or a real blocker requires a handoff.
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
| ⚙️ **حالت تطبیقی** | بسته به ریسک از Tiny، Standard یا Critical استفاده می‌کند. |
| ✂️ **One-slice** | هر بار فقط یک تغییر کوچک و قابل تست انجام می‌شود. |
| ✅ **تست رفتاری** | مسیر مثبت، منفی، حفظ رفتار و خطا را با شواهد RED/GREEN ثابت می‌کند. |
| 🧭 **Independent Oracle** | برای کار Critical از یک runtime یا قرارداد مستقل کمک می‌گیرد. |
| 🕵️ **Review بدبینانه** | Done الکی، تست ضعیف، scope creep و secret leak بررسی می‌شود. |
| 🔁 **Handoff تمیز** | session بعدی بدون حدس‌زدن ادامه می‌دهد. |
| 🧼 **بهداشت ریپو** | فایل generated، مسیر لوکال و چیزهای private کمتر وارد commit می‌شوند. |

### پرامپت آماده

```text
با Hermes Loop Master این تسک را انجام بده.
اول .hermes-loop/LOOP.md را کامل کن.
هر بار فقط یک slice فعال داشته باش؛ بعد از تست و Review،
slice بعدی را تا تکمیل Done When یا رسیدن به blocker واقعی ادامه بده.
در پایان REVIEW.md و HANDOFF.md را کامل کن.
```

---

## 🧪 Real test results

### Built-in fixture check

```bash
python -m unittest discover -s tests -v
python scripts/validate_skill.py SKILL.md
python scripts/harness_check.py --strict --mode standard examples/good-loop
python scripts/harness_check.py --strict --mode critical examples/critical-loop
! python scripts/harness_check.py --strict examples/bad-loop
```

Observed result:

```text
Unit suite: 34/34 pass
SKILL.md: valid without PyYAML
STANDARD: 35/35 (100%, structured RED/GREEN)
CRITICAL: 39/39 (100%, 7/7 behavioral gates)
BAD: 9/34 (26%), rejected as expected
```

| Fixture | Result | Meaning |
|---|---:|---|
| ✅ `good-loop` | `35/35` | Complete Standard loop with structured RED/GREEN evidence. |
| ✅ `critical-loop` | `39/39` | Runnable Critical fixture plus seven behavioral evidence gates. |
| ❌ `bad-loop` | `9/34` | Missing contract, evidence, review checks, and handoff fields. |

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

Historical v1.3 smoke evidence:

```text
3 passed in 0.09s
git diff --check → ok
legacy harness → Score: 27/27 (100%)
```

Bonus signal: the loop also caught accidentally tracked `__pycache__` files and cleaned them from git.

---

## 📦 Repository contents

```text
.
├── SKILL.md
├── install.sh
├── install.ps1
├── templates/
│   ├── LOOP.md
│   ├── REVIEW.md
│   ├── HANDOFF.md
│   └── FEATURES.json
├── scripts/
│   ├── artifact_contract.py
│   ├── security_patterns.py
│   ├── validate_skill.py
│   ├── harness_check.py
│   └── compare_benchmarks.py
├── references/
│   └── behavioral-verification.md
├── examples/
│   ├── good-loop/
│   ├── critical-loop/
│   └── bad-loop/
├── tests/
├── .github/workflows/quality.yml
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

- [x] GitHub Actions CI for skill + fixture validation
- [x] Adaptive Tiny / Standard / Critical modes
- [x] Strict behavioral harness and benchmark comparison
- [x] Safer installer with `--dry-run`, `--force`, and `--target`
- [ ] Python / Node / Flutter / Go / Rust verification recipes
- [ ] Better diff classifier for generated files and weakened tests
- [ ] More real examples: API, UI state, authz negative test, migration dry run

---

## 🤝 Contributing

Contributions are welcome. Keep changes public-safe and evidence-backed.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## 📄 License

MIT — see [LICENSE](LICENSE).
