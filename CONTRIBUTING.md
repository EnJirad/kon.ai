# Contributing to KonAI

The library is deliberately small. Size is not a goal; usefulness is. A pull
request that adds a tenth debugging skill weakens the library more than one that
fixes a sentence in an existing procedure.

## Before you write

1. **Search the catalog.** `catalog.json` lists every skill with its description
   and task types. `grep -ri "<topic>" skills/` searches the bodies.
2. **Check for overlap.** If an existing skill covers 70% of what you want, the
   contribution is an edit to that skill, not a new one.
3. **Name the real task.** State a task where the current library fails and your
   change succeeds. "It would be nice to have" is not a task.
4. **Confirm the scope is one capability.** If the draft has two unrelated
   procedures, it is two skills — or one skill and a reference file.

## What a contribution must contain

Open a pull request with:

- **Purpose** — the capability, in one sentence.
- **Use cases** — when an agent should activate it, and when it should not.
- **Scope** — what is inside and explicitly outside.
- **Requirements** — tools, runtimes, or access the procedure assumes.
- **Evidence** — a real task the skill was tested on, and what changed in the
  agent's behavior. Paste the before/after, or describe the observable
  difference. Do not submit "looks good".
- **Dependencies** — anything the skill requires beyond reading files. Ideally
  none.
- **Known limitations** — where the skill does not help or could mislead.
- **Format check** — the output of both validation commands below.

For an edit to an existing skill, include the same evidence plus what the old
wording caused to go wrong.

## Quality bar

Every skill must have:

1. A clear purpose, stated in the description.
2. A specific task scope.
3. A description that routes correctly — triggering when relevant, staying quiet
   when not.
4. Actionable instructions, ordered as a procedure.
5. Edge cases that actually occur.
6. Failure conditions and stop rules.
7. Verification guidance tied to observable evidence.
8. Minimal context: no restating background the agent already has.
9. No duplication of another skill's instructions — cross-reference instead.

A skill is rejected when it:

- gives generic advice ("write clean code") without an executable step;
- repeats another skill;
- makes technical claims without support;
- references files, commands, or tools that do not exist;
- needs capabilities the target agents do not have;
- presents invented examples as recorded results;
- has no identifiable use case;
- adds complexity the library must then maintain.

## Validation

```bash
# format conformance — the official reference validator
pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
skills-ref validate skills/<your-skill>

# library-level checks — catalog sync, links, budget, orphans, credentials
python3 scripts/validate.py
```

Both must pass. `--strict` turns warnings into failures, which is the right mode
for a release pull request.

Format rules and catalog schema: [docs/skill-format.md](docs/skill-format.md).

## Review process

1. **Scope review** — is this distinct from what exists?
2. **Format review** — validation, naming, budgets.
3. **Technical review** — is the procedure correct, and does it hold outside the
   author's stack?
4. **Security review** — instructions that could cause destructive edits,
   exfiltration, or unsafe script execution are blockers.
5. **Practical test** — a reviewer runs the skill on a real task and records what
   happened.
6. **Merge** — with a catalog entry, a CHANGELOG line, and a version bump when
   the behavior changed.

Reviewers may request a reference file instead of a longer `SKILL.md`. That is
not a rejection; it is the progressive-disclosure budget talking.

## Editorial rules

- Imperative voice, second person. "Read the error", not "the agent should read".
- No filler, no motivational framing, no anthropomorphism.
- One idea per bullet.
- Tables for decisions, not for prose.
- Cite a command or a file, not an authority.
- Never claim a capability the reader's agent may not have.
- Write in English, keep terminology stable across skills.

## Versioning

Skills use semantic versioning in `catalog.json`:

| Bump | When |
| --- | --- |
| **major** | the procedure changes in a way that can alter outcomes, or the trigger conditions change |
| **minor** | new steps, new edge cases, new optional references |
| **patch** | wording, typos, broken links, clarifications with no behavior change |

Trivial formatting alone does not warrant a release. `CHANGELOG.md` records
meaningful changes — new skills, changed workflows, corrected instructions,
removals, compatibility changes — grouped by release.

## Scope policy for technology-specific skills

A technology skill (Android, React, Rust, …) is accepted only when it:

- references the core skills instead of restating them;
- contains knowledge that is genuinely specific to that technology;
- cannot be expressed as a two-line addition to a core skill;
- has a maintainer who can keep it current with the technology;
- names its version assumptions explicitly.

See [docs/roadmap.md](docs/roadmap.md) for the planned order.

## Security

Do not add a script that writes, deletes, or sends data without an explicit
opt-in flag. Do not add instructions that require credentials. Never commit
secrets, tokens, or real customer data — including in examples and fixtures.
Read [SECURITY.md](SECURITY.md) before adding executable resources.

## License

Contributions are accepted under the repository's [MIT license](LICENSE). By
opening a pull request you confirm you wrote the material or have the right to
contribute it.
