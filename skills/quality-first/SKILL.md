---
name: quality-first
description: Use before modifying, creating, or deleting code, configuration, or documentation, and before reporting any result. Enforces correctness over volume, minimal justified changes, reuse of existing implementations, and evidence-based reporting instead of claimed success.
license: MIT
---

# Quality First

Prime directive:

> Quality over quantity. Evidence over assumptions. Verified results over claimed success.

A small correct change beats a large speculative one. An honest "not verified"
beats an unearned "done".

## Gate before any change

Answer these before editing. If one has no answer, get it first.

1. **What is the requirement?** Restate it in one sentence. If the request is
   ambiguous in a way that changes the implementation, ask instead of guessing.
2. **What already exists?** Search for the behavior before writing it.
3. **What is the smallest change** that satisfies the requirement?
4. **What could this break?** Name the callers, consumers, or data affected.
5. **How will I verify it?** Name the command or observation in advance.

## Reuse before create

Search in this order, and stop at the first hit:

1. An existing function, component, or module that already does this.
2. An existing helper that does most of it and can be extended.
3. A standard library or already-declared dependency.
4. A new implementation — last resort, and only after the first three are ruled
   out with evidence.

State which case applied. "No existing equivalent" is a claim; support it with
what you searched.

## Minimality rules

- Change the narrowest responsible layer. Fix the cause, not every caller.
- Do not reformat, rename, or reorganize unrelated code in the same change.
- Do not add a dependency for something the standard library or an existing
  dependency already provides. If a dependency is genuinely required, say what
  it does, why the alternative was rejected, and what it costs to maintain.
- Do not create an abstraction for a single caller.
- Do not leave commented-out code, unused imports, or empty placeholders.
- Do not delete or rewrite code you do not understand; read it first.

## Change discipline

- Preserve unrelated in-progress work in the working tree.
- Prefer a targeted edit over rewriting a whole file.
- When a fix needs more than two edits in unrelated areas, stop and check
  whether the design is wrong rather than pushing through.
- Keep generated artifacts out of the change unless the project tracks them.

## Verification requirement

Every meaningful modification needs a check that could have failed:

| Change | Minimum evidence |
| --- | --- |
| Code logic | a test or executed scenario that exercises it |
| Build or config | the build or validation command, with its actual output |
| Documentation | rendering or link check when the project provides one |
| Data or migration | a dry run or a reversible test on sample data |
| Refactor with no behavior change | the pre-existing tests still passing |

Load `testing-and-verification` for how to select and interpret checks.

## Reporting honestly

Classify every claim before writing it:

- **Verified** — you ran the check and saw the result.
- **Partially verified** — some paths checked, others not. Say which.
- **Unverified** — not run. Say why.
- **Failed** — ran and did not pass. Include the actual error.

Never upgrade a classification. Never describe expected output as observed
output. If a check could not run because of a missing tool, environment, or
credential, report that as the result rather than omitting it.

## Stop conditions

Stop and report, without further edits, when:

- the requirement is unclear and a wrong guess would be expensive;
- two materially different fix attempts failed (see `root-cause-debugging`);
- the change requires a decision about product behavior, data loss, or cost
  that belongs to the user;
- verification is impossible in the current environment;
- the scope has grown beyond the original request.

## Anti-patterns

| Looks like | Why it hurts | Do instead |
| --- | --- | --- |
| "Implemented, tests pass" with no run | unverifiable claim | run it or say unverified |
| Rewriting a file to change one line | hides the real diff | targeted edit |
| New utility when one exists | duplicate behavior | search, then extend |
| Adding a package for one call | maintenance cost | standard library |
| Fixing symptoms at call sites | repeated bugs | fix the responsible layer |
| Silent scope expansion | unreviewable change | ask or defer |

## Definition of done

- The requirement is met at the narrowest responsible layer.
- Existing behavior that should not change still holds.
- The verification evidence exists and is quoted in the report.
- Unverified areas and remaining limitations are stated.
