---
name: code-review
description: Use when reviewing a diff, pull request, commit, or proposed change before merge, or when self-reviewing your own work. Reports evidence-backed findings ordered by severity, separating real defects from style preferences.
license: MIT
---

# Code Review

Goal: prevent defects from reaching main, and say clearly what is a defect and
what is an opinion.

## Inputs

Read in this order before commenting:

1. The change itself, file by file — the actual diff, not the description.
2. The user-facing intent: issue, pull request description, or commit message.
3. The tests that changed, and the tests that should have changed.
4. The call sites of every changed public symbol.
5. The project's conventions: instruction files, linter config, nearby code.

A review of a diff you have not read is a guess. Say "not reviewed" instead.

## Review order

Spend attention in this order. Stop refining lower layers when time is short.

1. **Correctness** — does it do what it claims, on all paths, including errors?
2. **Security** — trust boundaries, input handling, secrets, permissions.
3. **Regression risk** — existing behavior that could break.
4. **Data and contracts** — schema, API shape, migrations, compatibility.
5. **Maintainability** — duplication, complexity, naming that misleads.
6. **Tests** — do they actually cover the change and could they fail?
7. **Style and formatting** — only if the project enforces it, and only last.

## Severity scale

| Level | Meaning | Merge impact |
| --- | --- | --- |
| **Blocker** | wrong behavior, data loss, security hole, broken build | must fix |
| **Major** | defect on a reachable path, missing error handling, contract break | should fix |
| **Minor** | maintainability issue with a concrete future cost | fix or file |
| **Nit** | preference; project does not enforce it | optional |

Rules:

- A finding's level comes from impact, not from how confident you feel.
- Style, formatting, and naming preferences are nits unless a project rule or
  a correctness risk makes them otherwise.
- Do not inflate severity to seem thorough. Do not deflate it to be agreeable.

## Checklist

**Correctness**

- Boundary and empty cases: zero, one, many, null or none, maximum size.
- Error paths return or propagate; nothing silently swallowed.
- Concurrency: shared state, ordering, idempotency, retries.
- Resource handling: files, connections, locks, listeners.
- Off-by-one, integer width, time zone, locale, encoding, rounding.

**Security**

- Untrusted input validated at the boundary, not deep inside.
- No secret, token, or credential added to code, logs, or fixtures.
- Authorization checked on the server side, not only in the UI.
- Queries parameterized; paths and commands not built from raw input.
- Deserialization, file uploads, and redirects constrained.
- New dependency: real need, maintained, license compatible.

**Regression**

- Changed signatures: every caller updated.
- Changed defaults: documented and intentional.
- Changed output shape: consumers located.
- Migration: reversible, ordered, safe to run while old code is live.

**Maintainability**

- Duplicate implementation of an existing capability.
- Abstraction with a single caller, or indirection that hides control flow.
- Misleading names, dead code, commented-out blocks, unused imports.
- Test coverage that asserts implementation detail instead of behavior.

**Integration**

- Config, environment, and feature flags documented where the project does so.
- Observability: a new failure mode becomes visible in logs or metrics.
- Rollout: can this be reverted without data repair?

## Evidence requirement

Every finding needs:

```markdown
**[Severity] <file>:<line> — <what is wrong>**
Why it matters: <concrete consequence>
Evidence: <the code path, failing input, or contract that proves it>
Fix: <smallest correct change>
```

If you cannot state the consequence, you have a question, not a finding. Ask it
separately from the findings list.

## Output format

1. One-line verdict: approve, approve with comments, or changes required.
2. Blockers and majors, highest impact first.
3. Minors grouped by file.
4. Open questions, clearly separated from defects.
5. What you checked and did not check.

Omit empty sections. Skip praise padding; a review is not a scorecard.

## Do not

- Rewrite the author's work in the comments section; suggest the smallest fix.
- Report a stylistic preference as a defect.
- Claim a defect without tracing the path that triggers it.
- Say "tests pass" unless you ran them or the CI result is visible.
- Demand changes unrelated to the diff under review.

## Limits

State when you could not review a part: generated files, large binaries,
code requiring runtime access, or behavior that needs the deployed environment.

## Related

Diagnosing a defect is `root-cause-debugging`; proving a fix works is
`testing-and-verification`. Do not restate their rules here.
