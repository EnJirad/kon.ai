# Getting started

First ten minutes with KonAI.

## 1. Decide what you want to fix

Do not install the library and hope for the best. Pick the failure mode you
actually have:

| Your symptom | Start with |
| --- | --- |
| "It broke and I don't know why" | `root-cause-debugging` |
| "I don't know this codebase" | `project-discovery` |
| "The agent says done, I don't believe it" | `testing-and-verification` |
| "It keeps churning through files" | `token-efficient` |
| "It wrote something the repo didn't need" | `quality-first` |

## 2. Install one skill

```bash
git clone --depth 1 https://github.com/EnJirad/kon.ai /tmp/konai
mkdir -p ~/.claude/skills                       # or your agent's directory
cp -r /tmp/konai/skills/root-cause-debugging ~/.claude/skills/
```

Directory names and per-agent paths: [installation.md](installation.md).

## 3. Confirm the agent can see it

```bash
skills-ref validate ~/.claude/skills/root-cause-debugging
```

Then ask the agent something whose answer is the skill:

> Which KonAI skills do you have available, and when would you use
> `root-cause-debugging`?

The expected answer quotes the description and says it applies when a cause is
unknown. It should **not** dump the whole file — discovery only sees name and
description.

## 4. Use it on a real problem

Give the agent the failure, not your theory of the failure:

> The test `checkout.spec.ts > applies discount` fails after my change.
> Use `root-cause-debugging`.

What good output looks like, structurally:

1. It quotes the actual error and the failing assertion.
2. It names the execution path and the files involved.
3. It states a hypothesis and the cheapest way to test it.
4. It changes one thing, then reruns the failing case.
5. It reports the before/after output, or says plainly it is stuck.
6. After two genuinely different attempts, it stops and escalates with what it
   ruled out.

What bad output looks like: several edits in a row with no stated hypothesis, a
dependency bump, a disabled assertion, or "this should fix it".

## 5. Add a second skill only when it earns its place

Good pairs:

- `project-discovery` then `quality-first` — understand, then change minimally.
- `root-cause-debugging` then `testing-and-verification` — fix, then prove it.
- `code-review` then `testing-and-verification` — review, then verify the fix.

Do not install all eight at once. Each one is a procedure the agent may follow;
you want to learn how one behaves before trusting eight.

## A worked example (illustrative, not a recorded session)

> **You:** Add a `--dry-run` flag to `scripts/deploy.sh`.
>
> **Agent:** Loading `project-discovery`. Found: shell scripts under `scripts/`,
> no test suite, CI runs `shellcheck scripts/*.sh`. Entry point:
> `scripts/deploy.sh:12` parses flags. Existing `--force` uses the same pattern,
> so I will extend it rather than add a parser. Loading `quality-first`:
> smallest change is one case branch plus the usage text.
>
> **Agent:** Changed `scripts/deploy.sh:18`. Verified with `shellcheck` (exit 0)
> and `bash -n`. Ran `./scripts/deploy.sh --dry-run` against the staging config:
> printed the planned commands, made no changes. `--force` still works. Tests:
> none exist in this project, so behavior is verified by those two runs, not by
> a suite.

The values on display: evidence over narrative, smallest change, reuse of the
existing pattern, honest limits.

## 6. Verify it helped

Ask yourself after the task:

- Did the agent investigate before editing?
- Did it cite real output, or assert success?
- Was the diff smaller than what you expected?
- Did it stop and ask instead of guessing?

If any answer is no, the skill did not activate. Check that the directory name
matches the `name` field and that your agent's skill support is enabled.

## 7. Keep skills in version control where they matter

If a skill changes how your team's agent works, commit it into the project at
`.agents/skills/` or `.claude/skills/` so reviews cover prompt changes the same
way they cover code changes.

## Next

- Format and conventions: [skill-format.md](skill-format.md)
- Writing your own: [CONTRIBUTING.md](../CONTRIBUTING.md)
- Trust and safety: [SECURITY.md](../SECURITY.md)
