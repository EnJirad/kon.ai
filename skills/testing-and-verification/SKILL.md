---
name: testing-and-verification
description: Use before reporting any change as complete or fixed, when choosing which tests to run, or when interpreting build and test output. Enforces real evidence, correct interpretation of exit codes and skips, and an explicit success/partial/unverified/failed classification.
license: MIT
---

# Testing and Verification

Rule: a claim about behavior is only as good as the evidence behind it.

## The claim ladder

Never claim more than the evidence supports.

| Evidence you have | You may claim |
| --- | --- |
| You ran the check and it passed | "X is verified" |
| You ran part of the check | "X is partially verified; Y is untested" |
| You reasoned about the code without running it | "unverified" |
| You ran it and it failed | "failing, here is the output" |
| You could not run it | "not run because <reason>" |

Never say "should work", "should pass", or "this fixes it" in place of evidence.

## Selecting tests

Start with the smallest meaningful set, then widen by risk.

1. **The reproduction.** The exact command or test that showed the problem. For
   a fix, confirm it failed before and passes after. If you did not see it fail,
   you do not know that it demonstrates the bug.
2. **The nearest unit tests** for the changed function or module.
3. **The test file's suite**, when the change affects shared behavior.
4. **Integration or end-to-end**, when the change crosses a boundary: network,
   database, filesystem, serialization, permissions.
5. **The full suite**, when the change touches shared code, build config, or
   dependencies — or when the project's rules require it.
6. **Static checks** the project defines: type check, lint, format check,
   schema validation. Run them last if they are not part of the build.

Do not run the full suite first on a large project. Do not run only one unit
test for a change that alters a contract.

## Commands

Use the project's own commands from its manifests or documentation. Do not
invent a runner the project does not use.

- Prefer the script the project declares over a hand-built command.
- Run from the directory the project expects; check the working directory.
- Capture the full output. Do not pipe through a filter that hides failures.
- Note the exit code separately from the output text.

## Interpreting output

Read past the last line. Check for:

- **Exit code** — the authority. Zero with errors in the log is a warning
  condition, not a pass.
- **Skipped tests** — a skip is not a pass. Say how many skipped and why.
- **Warnings** — categorize; do not silently ignore new ones.
- **Partial runs** — a filtered run only proves the filtered cases.
- **Timeouts and flakes** — rerun once for evidence, then report as flaky.
- **Cached results** — a cache hit is not a fresh verification; note it.
- **Coverage** — absence of coverage is not absence of bugs; use it only to show
  what was not exercised.

## Classification

Report exactly one class per claim:

| Class | Meaning | What to say |
| --- | --- | --- |
| **Verified** | the check ran, exited success, nothing skipped that matters | "verified — <command>" |
| **Partially verified** | some paths checked, others not | "verified A; B untested" |
| **Unverified** | not run, or run without observing the relevant output | "unverified — <why>" |
| **Failed** | ran and did not pass | "failing — <actual output>" |

## Reproduction discipline

- Report the exact command, the working directory, and the relevant output.
- For failures, include the failing assertion and the shortest input that shows
  it.
- If the failure is environmental (missing dependency, permission, network),
  separate it from a code failure.
- Preserve a failing case as a regression test when the project has a test
  suite, and state whether it failed before the change.

## Never

- Invent a test name, command, or result.
- Report "all tests pass" from a partial run.
- Treat a skipped or disabled test as passing.
- Describe expected output as observed output.
- Delete or loosen a failing test to make a suite green without stating it.
- Report a build as passing without its exit code.

## Reporting template

```markdown
## Verification
- Reproduction: <command> — failed before / passes after (or: not observed)
- Unit: <command> — <pass/fail/skip counts>
- Integration: <command> — <result>
- Static: <command> — <result>
- Not run: <what and why>
- Classification: verified | partially verified | unverified | failed
```

## Extending for a technology

This skill is deliberately technology-neutral. A technology-specific skill may
add its own commands, fixtures, and environments. It must not weaken the
classification rules or the evidence requirement above.

## Failure conditions

Stop and report when verification cannot run: missing toolchain, absent
credentials, unavailable service, or a broken environment. An unverified result
delivered honestly is acceptable; a fabricated one is not.

## Related

Diagnosing an unknown failure is `root-cause-debugging`; scoping the change is
`quality-first`. This skill decides only what counts as evidence.
