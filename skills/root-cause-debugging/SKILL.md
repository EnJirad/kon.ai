---
name: root-cause-debugging
description: Use when something fails and the cause is unknown — build or compile error, failing test, crash, wrong output, hang, or flaky behavior. Forces evidence-based diagnosis, keeps a failure log, forbids repeating a failed approach, and caps attempts before escalating.
license: MIT
---

# Root Cause Debugging

Rule: a fix without a diagnosis is a guess. A guess repeated is a stall.

## Step 0 — Read the actual error

Before anything else:

- Read the **whole** message, not the first line and not a remembered summary.
- Get the full stack trace. Truncated traces hide the real frame.
- Identify the **first frame that belongs to this project**. Framework internals
  below it usually describe symptoms, not cause.
- Note the error class, exit code, and the exact command that produced it.

If you cannot reproduce the failure, that is the first problem to solve.

## The eight steps

1. **Capture** the failing command, its full output, and the environment
   (branch, dependency versions, platform) when the output mentions them.
2. **Locate** the execution path: which entry point reaches the failing line.
   Follow call sites upward until you reach code the change or user controls.
3. **Inspect** the relevant source, not the whole repository. Read the function
   that fails and the code that calls it.
4. **Check configuration and dependencies** when the path crosses them:
   manifest, lockfile, environment variables, build config, schema. A surprising
   number of "code" bugs are configuration divergence.
5. **Form one falsifiable hypothesis**: "X is null/wrong/misconfigured because Y."
   It must predict an observable difference.
6. **Run the cheapest discriminating test.** Choose the check that splits the
   hypothesis space fastest — a log line, a narrow test, a one-off probe —
   before changing production code.
7. **Apply the smallest justified fix** at the responsible layer. Not at call
   sites that merely surface the fault.
8. **Verify** with the original failing command, then with the nearby tests that
   could regress. Report the actual output.

## Failure log

Keep this while debugging. It is what prevents a retry loop.

| # | Attempt | Hypothesis | Evidence | Result | Why it failed | Next |
| --- | --- | --- | --- | --- | --- | --- |
| 1 |  |  |  |  |  |  |
| 2 |  |  |  |  |  |  |

Before every new attempt, write the row. If the new attempt would repeat a row
with the same hypothesis and the same evidence, do not run it.

## Stop rules

- **Two materially different approaches.** After two genuinely different fixes
  fail, stop changing code. Escalate.
- "Materially different" means a different hypothesis about the cause. Retrying
  the same fix with a different syntax, a longer timeout, a cache clear, or a
  version bump is **not** a new approach unless new evidence justifies it.
- Stop earlier than two when the next step needs information, access, or a
  decision you do not have.
- A fix that makes the symptom disappear without explaining the cause is not a
  fix. Record it as unresolved.

## Traps

| Trap | Why it wastes time | Do instead |
| --- | --- | --- |
| Change code and rerun, repeatedly | no hypothesis, no learning | form a hypothesis first |
| Upgrade or downgrade a dependency | masks the cause, adds risk | read the error first |
| Disable a check, lint rule, or test | hides evidence | find why it fires |
| Catch and ignore the exception | moves the failure | handle or surface it |
| Copy a fix from a similar issue | different codebase, different cause | verify it applies here |
| Edit several things at once | cannot attribute the result | one change per attempt |
| Trust a passing suite after a failure | flakiness or skips | rerun the specific failure |

## Escalation package

When you stop, hand over:

- the exact failing command and its full output;
- the failure log rows so far;
- the code path you traced, with paths and lines;
- the hypotheses eliminated and the evidence that eliminated them;
- the smallest question or decision you need to proceed.

Do not escalate with "it doesn't work". Escalate with what you now know.

## Fix quality

- Fix the cause at the layer that owns the invariant.
- If the cause is a contract violation, fix the contract or both sides — not
  only the caller that happened to break.
- Preserve the failing case as a regression test when the project has tests, and
  note whether it fails before the fix and passes after.
- Remove temporary probes, logs, and debug flags before reporting.

## Failure conditions

Say so plainly when:

- the error is environmental (missing tool, permission, network) and cannot be
  reproduced here;
- the root cause lies outside the repository;
- two approaches have failed and the remaining options need a decision that is
  not yours to make.

## Related

Before reporting the fix, follow `testing-and-verification`. When the fix grows
past a local correction, `quality-first` governs its scope.
