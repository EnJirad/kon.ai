# Skill format

KonAI uses the open [Agent Skills specification](https://agentskills.io/specification).
That page is authoritative. This document covers the parts that matter when
writing or reviewing a KonAI skill, plus the conventions this repository adds.

## Anatomy

```
skill-name/
├── SKILL.md          # required: YAML frontmatter + Markdown instructions
├── references/       # optional: detail loaded on demand
├── scripts/          # optional: executable helpers, never auto-run
└── assets/           # optional: templates and data
```

A directory with a valid `SKILL.md` is a skill. Everything else is optional.

## Frontmatter

| Field | Required | Constraint |
| --- | --- | --- |
| `name` | yes | 1–64 chars; lowercase letters, digits, hyphens; no leading, trailing, or double hyphen; **must equal the directory name** |
| `description` | yes | non-empty, max 1024 chars; what the skill does and when to use it |
| `license` | no | license name or reference to a bundled file |
| `compatibility` | no | max 500 chars; environment requirements |
| `metadata` | no | map of string keys to string values |
| `allowed-tools` | no | experimental; space-separated tool list |

Do not invent fields. An unknown field may be ignored by one client and rejected
by another, which breaks portability.

KonAI's own policy:

- every skill sets `license: MIT`;
- no KonAI-specific frontmatter — category, version, status, and task types live
  in [`catalog.json`](../catalog.json), so the skill file stays portable;
- `name` and `description` are the only load-bearing fields for discovery. Treat
  the description as an API: it decides whether the skill is ever read.

## Write a description that routes

The description is the only thing an agent sees before activation. It must say
both **what** the skill does and **when** to use it.

```yaml
# weak — sounds fine, routes nothing
description: Helps with code quality.

# useful — names the trigger and the scope
description: Use before modifying, creating, or deleting code, configuration,
  or documentation, and before reporting any result. Enforces correctness over
  volume, minimal justified changes, reuse of existing implementations, and
  evidence-based reporting instead of claimed success.
```

Include negative edges when they prevent false activation: "Do not use for
stylistic preferences alone."

## Progressive disclosure budgets

| Level | Content | Target |
| --- | --- | --- |
| Discovery | `name` + `description` | ~100 tokens |
| Activation | `SKILL.md` body | under 500 lines, under 5000 tokens |
| Resources | referenced files | loaded only when the skill says so |

If a skill exceeds the budget, move detail into `references/` and point at it:
"read `references/protocol.md` before changing the wire format". Keep reference
chains one level deep.

## Content requirements

A KonAI skill must contain:

1. A single coherent capability — not a swiss-army document.
2. A trigger statement: the situation in which it applies.
3. An ordered procedure an agent can execute.
4. The evidence or verification each step requires.
5. Stop conditions: when to escalate instead of continuing.
6. Failure modes: what "blocked" looks like.
7. Cross-references to other skills instead of copying their instructions.

Reject a skill that contains generic advice, duplicates another skill, asserts
unverified technical claims, or cannot be evaluated on a real task.

## Referencing files

Use paths relative to the skill root, one level deep:

```markdown
Read [the protocol reference](references/protocol.md) before changing the schema.
Run `scripts/extract.py --check` to verify the fixture set.
```

`scripts/validate.py` fails on a broken relative link and warns on a resource no
`SKILL.md` mentions.

## Scripts

Scripts are optional and never run automatically. If you ship one:

- state its language, runtime, and dependencies in `SKILL.md`;
- make it read-only by default and require an explicit flag for writes;
- handle failure with a non-zero exit and a useful message;
- document network access or side effects;
- keep it small enough to read before running.

## Catalog entry

Every skill has one entry in `catalog.json`:

```json
{
  "id": "quality-first",
  "name": "quality-first",
  "description": "<identical to SKILL.md>",
  "category": "quality",
  "path": "skills/quality-first",
  "version": "1.0.0",
  "status": "stable",
  "task_types": ["code-change", "minimal-change"],
  "technologies": []
}
```

The description must match `SKILL.md` exactly; `scripts/validate.py` fails on
drift. That is deliberate: the catalog is the discovery surface, so it may not
promise something the skill does not say.

`status` is one of `draft`, `beta`, `stable`, `deprecated`. `technologies` stays
empty for technology-agnostic skills and lists tags for specific ones.

## Adding a skill

1. Search `catalog.json` and grep existing skills for overlap.
2. Confirm the capability is genuinely distinct; otherwise extend the existing
   skill.
3. Create `skills/<name>/SKILL.md` and one catalog entry.
4. Run `skills-ref validate skills/<name>` and `python3 scripts/validate.py`.
5. Test it on a real task and record the evidence in the pull request.

Full process and quality gates: [CONTRIBUTING.md](../CONTRIBUTING.md).
