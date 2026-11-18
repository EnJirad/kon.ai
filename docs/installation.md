# Installing KonAI skills

A skill is a directory containing `SKILL.md`. Installation means placing that
directory where your agent looks for skills. There is no build step, no
installer requirement, and no runtime dependency.

Verified 2026-11-18 against each agent's documentation. Paths are quoted from
those pages; anything unverified is marked as such.

## Pick a skill, install one skill

You never need the whole library:

```bash
git clone --depth 1 https://github.com/EnJirad/kon.ai /tmp/konai
cp -r /tmp/konai/skills/root-cause-debugging ~/.claude/skills/
```

Copy the directory as-is. Do not rename it, and do not extract `SKILL.md` alone:
the folder name must equal the `name` in the frontmatter, and any
`references/`, `scripts/`, or `assets/` must travel with it.

## Installation by agent

### Claude Code

Documented locations (`code.claude.com/docs/en/skills`):

| Scope | Path |
| --- | --- |
| Personal (all projects) | `~/.claude/skills/<name>/SKILL.md` |
| Project (committed) | `.claude/skills/<name>/SKILL.md` |
| Monorepo subdirectory | `<subdir>/.claude/skills/<name>/SKILL.md` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` |

```bash
mkdir -p ~/.claude/skills
cp -r /tmp/konai/skills/quality-first ~/.claude/skills/
```

Claude Code explicitly supports symlinks for a skill entry, so a single checked
out copy can be linked into several projects:

```bash
ln -s /path/to/kon.ai/skills/quality-first .claude/skills/quality-first
```

Do not name a skill folder `synced`; that name is reserved.

*Unverified:* Claude Code reading `.agents/skills/`. Its documentation lists only
`.claude/skills/` locations, so use `.claude/skills/` there.

### OpenCode

Documented locations (`opencode.ai/docs/skills/`):

| Scope | Path |
| --- | --- |
| Global | `~/.config/opencode/skills/` |
| Global compatibility | `~/.claude/skills/`, `~/.agents/skills/` |
| Project | `.opencode/skills/` |
| Project compatibility | `.claude/skills/`, `.agents/skills/` |

OpenCode searches from the current directory up to the project root and includes
matching directories at every level. Extra sources can be declared in the
`skills` array of `opencode.json`, including relative, absolute, `~/`, and
`https://` catalog URLs.

```bash
mkdir -p .opencode/skills
cp -r /tmp/konai/skills/project-discovery .opencode/skills/
```

OpenCode derives a skill's identity from its path rather than the frontmatter
`name`, treats the spec fields as optional, and resolves precedence as
`.claude` < `.agents` < global OpenCode < project OpenCode < explicit config.
KonAI still fills `name` and `description` because the portable format requires
them.

### OpenAI Codex

Documented scopes (`developers.openai.com/codex/skills`). Note the path is
`.agents/skills`, **not** `.codex/skills`:

| Scope | Path |
| --- | --- |
| Repository (current directory) | `$CWD/.agents/skills/` |
| Repository (parents to root) | `.agents/skills/` at each level up to repo root |
| User | `$HOME/.agents/skills/` |
| Admin | `/etc/codex/skills/` |

```bash
mkdir -p .agents/skills
cp -r /tmp/konai/skills/code-review .agents/skills/
```

Codex follows symlinked skill folders. Skills can be disabled per project with
`[[skills.config]]` entries in `~/.codex/config.toml`.

*Unverified:* `~/.codex/skills/`. That directory holds configuration, not
skills; the documented user path is `$HOME/.agents/skills/`.

### GitHub Copilot

Documented locations (`docs.github.com` → Copilot → agent skills):

| Scope | Path |
| --- | --- |
| Project | `.github/skills/`, `.claude/skills/`, `.agents/skills/` |
| Personal | `~/.copilot/skills/`, `~/.agents/skills/` |

```bash
mkdir -p .github/skills
cp -r /tmp/konai/skills/testing-and-verification .github/skills/
```

With GitHub CLI ≥ 2.90.0, the public-preview `gh skill` commands install into
the right directory for the host, and can pin a revision:

```bash
gh skill preview EnJirad/kon.ai quality-first
gh skill install EnJirad/kon.ai quality-first@v1.0.0
```

Copilot also supports `.github/copilot-instructions.md` for always-on guidance.
That is a different mechanism: instructions for every task, skills for tasks
that match.

### Other compatible agents

Anything that reads `SKILL.md` with `name` and `description` frontmatter can use
a KonAI skill. The cross-tool convention is `.agents/skills/` (project) and
`~/.agents/skills/` (user); use your agent's documented directory if it differs.
The [Agent Skills client showcase](https://agentskills.io/clients) lists current
compatibility with links to each client's setup page.

## Project-scoped install without vendoring

Commit the skill into the repository when the team should share it. When you
want a shared, pinned checkout instead, use sparse checkout:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/EnJirad/kon.ai
cd kon.ai
git sparse-checkout set skills/quality-first skills/testing-and-verification
```

Then symlink the directories into `.agents/skills/` or `.claude/skills/`.

## Verify an installation

```bash
skills-ref validate .claude/skills/quality-first
skills-ref read-properties .claude/skills/quality-first
```

The second command prints the `name` and `description` the agent will see during
discovery. If the directory name and `name` disagree, `validate` fails.

Then confirm activation: ask the agent a task that matches the description and
check that it follows the skill's steps rather than its own habits.

## Updating

```bash
git -C /tmp/konai pull
cp -r /tmp/konai/skills/quality-first ~/.claude/skills/   # replaces the folder
```

Read the diff before updating. Skills are instructions the agent will follow;
treat an update like a dependency change. Version history is in
[CHANGELOG.md](../CHANGELOG.md); pin a tag or SHA when you need stability.

## Uninstalling

Delete the skill directory. Nothing else is created by installing a skill.

## Packaging for broader distribution

The library is intentionally not a package. A `package.json`, registry, or
installer would add a maintenance surface without making `SKILL.md` any more
portable. If a real distribution need appears, prefer the existing mechanisms
(Git, `gh skill`, symlinks, plugins) over a new one.
