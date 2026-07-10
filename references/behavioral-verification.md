# Behavioral Verification Matrix

Artifact completeness proves process discipline; it does not prove that the code is correct. Standard and Critical loops must verify observable behavior, and Critical loops should use an **Independent Oracle** whenever a trustworthy one exists.

## Required paths

| Path | Question | Typical evidence |
|---|---|---|
| **Positive path** | Does an intended valid input still work? | focused unit/integration/smoke test |
| **Negative path** | Is the reported exploit, invalid input, or denied action blocked? | regression test that failed before the fix |
| **Preservation path** | Did the fix accidentally reject or break previously valid behavior? | representative valid edge cases and unchanged baseline tests |
| **Failure path** | Do malformed input, timeout, missing config, and unavailable dependencies fail safely? | fail-closed test with no unintended side effect |

For behavior changes, record both **RED evidence** (the new regression fails for the expected reason before implementation) and **GREEN evidence** (the same check passes after the implementation). A test written after the code without observed RED evidence is useful regression coverage but is not TDD evidence.

For machine-checkable Critical evidence, put each exact label in the `Command / Check` cell and use a canonical result token (`pass`, `fail`, `ok`, `success`, `blocked`, or `skipped`):

```markdown
| T1 | RED evidence: `<same focused command>` | fail | Expected pre-fix failure. |
| T2 | GREEN evidence: `<same focused command>` | pass | Same check after fix. |
| T3 | Positive path: `<command>` | pass | Valid input works. |
| T4 | Negative path: `<command>` | pass | Unsafe input is denied. |
| T5 | Preservation path: `<command>` | pass | Valid edge behavior remains. |
| T6 | Failure path: `<command>` | pass | Malformed input fails safely. |
| T7 | Independent Oracle: `<authoritative check>` | pass | Oracle agrees. |
```

Do not replace these labels with synonyms or hide them only in prose; run the strict harness when it is available.

## Independent Oracle

An Independent Oracle is a second implementation or authoritative runtime that can contradict the code under test. It should not reuse the same helper or assumptions as the implementation.

| Domain | Useful oracle |
|---|---|
| Browser URLs, redirects, frontend state | WHATWG URL/runtime behavior, browser smoke, accessibility tree |
| API | OpenAPI/JSON Schema validator, contract test, real local request |
| Database/migration | disposable real database, constraint violation, forward/rollback dry run |
| Auth/authorization | positive owner case plus unauthenticated and cross-owner negative cases |
| Payment/webhook | provider sandbox vectors, signature fixture, idempotency/replay checks; preserve documented key-rotation semantics such as repeated versioned signatures (accept when any supported signature matches), while rejecting conflicting timestamps and malformed fields |
| Filesystem/archive | isolated temp directory, path traversal corpus, checksum/read-back |
| CLI | invoke the real command and inspect exit code/stdout/stderr |
| Cron/automation | execute the exact scheduled script once and verify call count/output files |
| Deployment | internal health check, public smoke, proxy/config validation, rollback readiness |

If no independent oracle is practical, record `oracle unavailable: <reason>` and compensate with stronger boundary/property/metamorphic tests. Never fabricate oracle output.

## Critical verification matrix

Before a Critical task can be marked complete, the Evidence Log should identify:

- Positive path result;
- Negative path result;
- Preservation path result;
- Failure path result;
- RED evidence and GREEN evidence for behavior changes;
- Independent Oracle result or an explicit reason it was unavailable;
- targeted check followed by the narrowest meaningful broader check;
- side-effect read-back for writes, deployments, migrations, payments, or remote changes.

## Anti-overfitting rules

- Do not infer the full contract only from visible tests; inspect types, docs, callers, boundaries, and platform semantics.
- Add boundary classes, not a long list of near-duplicate examples.
- For security fixes, prove both rejection of unsafe inputs and acceptance of safe edge cases.
- Do not weaken existing assertions to get GREEN.
- Keep hidden/evaluation graders outside the agent's working tree when benchmarking.
