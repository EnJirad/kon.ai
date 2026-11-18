# KonAI

**Universal AI Skills Library & Agent Engineering Ecosystem**

KonAI is a small, curated set of portable [Agent Skills](https://agentskills.io)
that help AI coding agents work more reliably: understand an unfamiliar
repository, plan the smallest correct change, debug by cause instead of
guesswork, and report only what they actually verified.

It is not a prompt collection. Each skill is a procedure with explicit triggers,
stop conditions, evidence requirements, and failure modes.

## Why it exists

Agents are capable but wasteful in predictable ways:

- they read a repository instead of searching it;
- they retry a failed fix with different syntax instead of new evidence;
- they add a second implementation of something that already exists;
- they report success they never verified;
- they load every instruction they can find and then lose the thread.

KonAI addresses that with a few narrow skills that change procedure, not
personality. Skills add knowledge and workflows. They do not raise a model's
reasoning ability, grant tools, or override the host agent's rules.

## The core skills

| Skill | Use it when |
| --- | --- |
| [`konai-core`](skills/konai-core/SKILL.md) | finding which skill applies, or how skills load |
| [`project-discovery`](skills/project-discovery/SKILL.md) | working in an unfamiliar repository |
| [`architecture-planning`](skills/architecture-planning/SKILL.md) | a non-trivial change or design choice |
| [`quality-first`](skills/quality-first/SKILL.md) | about to modify, add, or delete code |
| [`root-cause-debugging`](skills/root-cause-debugging/SKILL.md) | something fails and the cause is unknown |
| [`code-review`](skills/code-review/SKILL.md) | reviewing a diff or pull request |
| [`testing-and-verification`](skills/testing-and-verification/SKILL.md) | before reporting work as complete |
| [`token-efficient`](skills/token-efficient/SKILL.md) | context is large or retrieval is wasteful |

A typical session uses at most two: `project-discovery` → `quality-first`, or
`root-cause-debugging` → `testing-and-verification`.

The machine-readable index is [`catalog.json`](catalog.json); it carries the
name, description, category, path, version, status, and task types of every
skill, without duplicating their instructions.

## How skills load

Agent Skills use progressive disclosure, so a large library costs little context
until a task needs it:

| Level | Loaded | Cost |
| --- | --- | --- |
| Discovery | `name` + `description` | ~100 tokens per skill |
| Activation | the full `SKILL.md` body | under 5000 tokens |
| Resources | `references/`, `scripts/`, `assets/` | only when the skill asks |

`catalog.json` covers level 1 for the whole library in about 1.4k tokens. You do
not need every skill resident to benefit from the one you need.

## Use one skill

Copy a single skill directory into your agent's skill location — no build, no
installer, no dependency:

```bash
git clone --depth 1 https://github.com/EnJirad/kon.ai /tmp/konai
cp -r /tmp/konai/skills/root-cause-debugging ~/.claude/skills/
```

Keep the directory name unchanged: the folder name must match the `name` field.

For every supported agent, including project-scoped and read-only installs, see
[docs/installation.md](docs/installation.md). First-time walkthrough:
[docs/getting-started.md](docs/getting-started.md).

## Compatibility

KonAI follows the open Agent Skills format, so nothing here is proprietary.
Verified skill locations include:

| Agent | Project | Personal |
| --- | --- | --- |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.opencode/skills/`, `.agents/skills/` | `~/.config/opencode/skills/`, `~/.agents/skills/` |
| OpenAI Codex | `.agents/skills/` | `~/.agents/skills/` |
| GitHub Copilot | `.github/skills/`, `.agents/skills/` | `~/.copilot/skills/`, `~/.agents/skills/` |

`.agents/skills/` is the shared project path for OpenCode, Codex, and Copilot.
Claude Code reads `.claude/skills/`. Paths and caveats, with sources, are in
[docs/installation.md](docs/installation.md).

Skills are inert text. They cannot execute anything: a skill that ships scripts
only makes them available for the host agent to run, under the host's own
permission rules. See [SECURITY.md](SECURITY.md).

## Validate

```bash
pip install "git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref"
skills-ref validate skills/quality-first     # format conformance
python3 scripts/validate.py                  # library-level checks
```

`scripts/validate.py` delegates spec conformance to `skills-ref` and adds checks
for catalog drift, broken relative links, body budget, unreferenced resources,
and committed credentials. Both must pass before a skill is considered ready.

## Status

Initial release: **v1.0.0** — eight core, technology-agnostic skills, validated
against the Agent Skills specification. Technology-specific skills are planned,
not promised; see [docs/roadmap.md](docs/roadmap.md).

Quality gates and known limits: [docs/release-report.md](docs/release-report.md).

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md). The short version: search the catalog
first, prove the capability is distinct, pass validation, and show evidence that
the skill helped on a real task.

## License

[MIT](LICENSE).

## Repository layout

```
skills/<name>/SKILL.md   one skill per directory
catalog.json             machine-readable index for discovery
scripts/validate.py      library validation
docs/                    usage, installation, format, roadmap
```
