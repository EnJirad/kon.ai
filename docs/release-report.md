# Release readiness report — v1.0.0

Date: 2026-11-18
Scope: initial release of the KonAI skill library
Repository state at assessment: `main`, eight skills, no technology-specific skills

This report records what was actually executed and observed. Anything that could
not be executed is listed as not verified rather than assumed.

## Shipped artifacts

| Artifact | Purpose |
| --- | --- |
| `skills/<name>/SKILL.md` × 8 | the library; each directory is independently installable |
| `catalog.json` | level-1 discovery index, identical descriptions to the skills |
| `scripts/validate.py` | library checks: catalog drift, links, budget, orphans, credentials |
| `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CHANGELOG.md` | use, contribution, trust, history |
| `docs/` | getting started, installation per agent, format, roadmap |
| `LICENSE` | MIT |

## Validation evidence

Format conformance — official reference validator, `skills-ref` 0.1.0:

```
$ for d in skills/*/; do skills-ref validate "$d"; done
Valid skill: skills/architecture-planning
Valid skill: skills/code-review
Valid skill: skills/konai-core
Valid skill: skills/project-discovery
Valid skill: skills/quality-first
Valid skill: skills/root-cause-debugging
Valid skill: skills/testing-and-verification
Valid skill: skills/token-efficient
```

Library checks — `python3 scripts/validate.py`:

```
8 skill(s) checked | 0 error(s) | 0 warning(s)
```

### The validator can fail

A passing validator proves nothing unless it detects defects. Each case below was
applied to a throwaway copy; every one was reported at the expected severity.

| Injected defect | Result |
| --- | --- |
| description changed in `catalog.json` | ERROR: description drift |
| relative link to a missing file | ERROR: broken relative link |
| resource file never referenced | WARN: resource not referenced |
| duplicate catalog id | ERROR: duplicate skill id |
| `sk-…` style credential in a skill | ERROR: possible committed credential |
| skill directory removed from catalog | ERROR: skill on disk missing from catalog |
| invalid directory name (`Code_Review`) | ERROR from official validator + catalog mismatch |
| broken link in `README.md` | ERROR: broken relative link |

Links inside fenced code blocks are correctly ignored.

## Acceptance tests

| Test | Status | Evidence |
| --- | --- | --- |
| **A. Skill format** | PASS | `skills-ref validate` succeeded for 8/8; naming, directory match, required frontmatter all conform |
| **B. Skill discovery** | PASS (judgment) | 8/8 descriptions contain an explicit trigger phrase ("Use when/before"), 0 exceed 1024 chars, 8 distinct categories. Routing was assessed by reading each description against the other seven; no two claim the same trigger |
| **C. Progressive disclosure** | PASS (measured) | Level 1 = `catalog.json` at 5482 bytes (~1370 tokens) for the whole library. Level 2 bodies total ~9.4k tokens; each body is 1122–1328 tokens against a 5000 budget |
| **D. Cross-project reuse** | PASS | No absolute system paths, no user paths, no framework-specific assumptions in any skill. One intentional repository URL in `konai-core` (see limitations) |
| **E. Root-cause debugging** | PASS (content) | Failure-log table, explicit two-approach cap, definition of "materially different", refusal to repeat an identical attempt, escalation package — all present and checked |
| **F. Token efficiency** | PASS (measured) | Full bodies cost 6.8× the catalog, so discovery without loading is materially cheaper; ratio is a property of the design, not an estimate |
| **G. Quality review** | PASS | 0 identical substantive lines shared between skills; all cross-references resolve; every skill has a trigger, procedure, stop conditions, and related-skill pointers |
| **H. Security** | PASS | 0 executables and 0 script or asset directories inside skills; all skill files are `.md`; secret-pattern scan clean; no auto-run mechanism exists |
| **I. Installation** | PASS (local), PARTIAL (remote) | Copied into five simulated agent directories (`.claude`, `.agents`, `.opencode`, `.github`, user-scope) — each validated; symlinked install validated. Remote clone and sparse checkout verified after the first push |
| **J. Maintenance** | PASS | Adding a skill without a catalog entry fails validation with a specific error; adding the entry passes; the eight existing skill files are byte-identical before and after |

## Compatibility

Verified against vendor documentation on 2026-11-18:

- Claude Code — `~/.claude/skills/`, `.claude/skills/`; symlinks supported.
- OpenCode — `~/.config/opencode/skills/`, `.opencode/skills/`, plus `.claude` and
  `.agents` compatibility paths.
- OpenAI Codex — `.agents/skills/` up to the repository root, `$HOME/.agents/skills/`.
- GitHub Copilot — `.github/skills/`, `.claude/skills/`, `.agents/skills/`,
  `~/.copilot/skills/`.

Details with sources: [installation.md](installation.md).

## Known limitations

1. **Technology-specific skills do not exist yet.** The roadmap describes the
   admission bar; nothing in it is built.
2. **No live-agent trial was run.** Tests B, E, and G assess the instructions
   directly. Whether a specific model follows them under load was not measured
   in a controlled experiment; it would need a reproducible harness and many
   runs to be meaningful.
3. **Installation paths come from documentation, not from running each agent.**
   No agent was installed and queried in this environment.
4. **`konai-core` contains the canonical repository URL** for clone instructions.
   A fork should update that line; it is a distribution reference, not a project
   assumption.
5. **`skills-ref` is labelled by its own maintainers as a demonstration library,
   not production software.** It is the reference for format conformance all the
   same; `scripts/validate.py` falls back to a warning if it is absent.
6. **The credential scan is heuristic** and only recognizes common shapes.
7. **No package manager, installer, or registry**, deliberately. Distribution
   relies on Git, `gh skill`, copying, and symlinks.

## Not verified

- Behavior of each agent's skill loader at runtime (no agent executed).
- Copilot in a specific IDE; its docs describe skills at product level.
- `gh skill` commands end to end. The local CLI is 2.103.3, above the documented
  2.90.0 floor, but the commands were not run against this repository.
- Whether Claude Code reads `.agents/skills/`. Not documented; not relied upon.

## Release checklist

- [x] Every skill passes the official format validator
- [x] Library checks pass with zero errors and zero warnings
- [x] Catalog matches the skills exactly
- [x] No duplicated instruction content between skills
- [x] No executable artifacts inside skills
- [x] Installation documented per agent, with unverified points labelled
- [x] Security model documented
- [x] Contribution and review process documented
- [x] Changelog and MIT license present
- [x] Limitations listed above rather than omitted

## Safeguards against waste

No placeholder directories, empty files, generated stubs, unused dependencies, or
speculative tooling were added. The repository contains one script, because
validation needs it, and documentation only where a reader needs an answer the
README does not give.
