---
name: konai-core
description: Entry point to the KonAI skill library. Use when you need to find which KonAI skill applies to a task, explain how skills are structured and loaded, avoid loading the whole library, or reuse a skill from another project. Routes to the right skill instead of repeating it.
license: MIT
---

# KonAI Core

Entry point for the KonAI skill library. Use this skill to decide **which** skill
applies and **how much** of it to load. It routes; it does not replace the other
skills.

## What a skill is

A skill is a directory whose `SKILL.md` starts with YAML frontmatter carrying at
minimum `name` and `description`, followed by Markdown instructions:

```
skill-name/
├── SKILL.md          # required: metadata + instructions
├── references/       # optional: deeper documentation, loaded on demand
├── scripts/          # optional: executable helpers, inspect before running
└── assets/           # optional: templates, data files
```

KonAI uses the open Agent Skills format (see `agentskills.io`). Nothing is
proprietary: an agent that can read `SKILL.md` can use a KonAI skill. The
directory name always equals the `name` field.

## Three levels of loading

| Level | What loads | Budget | Why |
| --- | --- | --- | --- |
| 1. Discovery | `name` + `description` only | ~100 tokens per skill | know the skill exists |
| 2. Activation | the whole `SKILL.md` body | under 5000 tokens | follow the workflow |
| 3. Resources | files under `references/`, `scripts/`, `assets/` | loaded only when the skill says so | detail without startup cost |

Operating rules:

- Do not load every skill body at startup. Discovery metadata is enough until a
  task actually matches.
- Activate one **primary** skill per task. Add at most one supporting skill.
- After activation, read only the sections the current step needs.
- Open a resource file only when the active skill points to it.
- Do not paste a skill's full text into your answer as a substitute for doing
  the work.

## Selecting a skill

Start from the failure or goal, not from the technology. Pick by symptom:

| Situation | Primary skill |
| --- | --- |
| Unfamiliar repository or subsystem | `project-discovery` |
| Something fails and the cause is unknown | `root-cause-debugging` |
| A non-trivial change or design choice | `architecture-planning` |
| About to modify, add, or delete code | `quality-first` |
| Reviewing a diff or pull request | `code-review` |
| Before reporting work as complete | `testing-and-verification` |
| Context is large or retrieval is wasteful | `token-efficient` |

Combining skills:

- Most work is `project-discovery` → `architecture-planning` → `quality-first` →
  `testing-and-verification`.
- A debugging session usually needs only `root-cause-debugging`, plus
  `testing-and-verification` at the end.
- Do not activate a technology-specific skill that does not yet exist; follow
  the core skill and state the gap.

## When not to load a skill

- The task is a one-line answer that needs no repository access.
- A skill you already loaded this session still governs the task; reuse it
  rather than reloading.
- The skill's description does not match the task. A near-miss is a reason to
  read the description again, not to load the body.

## Compatibility limits

Skills change what the agent **knows** and **how it proceeds**. They do not:

- raise the model's reasoning ability;
- grant tools, network access, permissions, or filesystem scope the host agent
  does not already provide;
- override the host's system prompt, safety rules, or approval requirements;
- guarantee that another agent supports features beyond reading `SKILL.md`.

If a skill step needs a capability you do not have, say so and propose the
closest submittable alternative. Never simulate the missing capability.

## Reusing KonAI from another project

Whole library:

```bash
git clone https://github.com/EnJirad/kon.ai
```

One skill only — copy just that directory, for example `skills/quality-first`,
into the agent's skill directory. No install step, manifest, or build is
required; `SKILL.md` is the artifact. Keep the directory name unchanged so the
`name` field still matches.

## Verifying that a skill is active

1. You can quote the skill's `description` from memory of the loaded file.
2. The workflow you are following comes from that file, not from habit.
3. You know which resource files it offers and have opened none you do not need.

If any of these fails, you loaded the wrong skill or guessed at its content.

## Failure conditions

Stop and report instead of improvising when:

- the task matches two skills that give conflicting instructions — prefer the
  one closer to the actual failure, and say which you chose;
- a skill references a file that is missing from the distribution;
- following the skill would require a permission or tool you do not have;
- the skill contradicts the host's rules — the host wins.
