# Changelog

All notable changes to the KonAI skill library are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Skill versions follow semantic versioning in [`catalog.json`](catalog.json);
repository releases aggregate them.

## [1.0.0] — 2026-11-18

Initial release. Eight technology-agnostic core skills, validated against the
Agent Skills specification.

### Added

- `konai-core` — entry point: discovery, activation, progressive disclosure,
  skill selection, and compatibility limits.
- `project-discovery` — evidence-backed profiling of an unfamiliar repository
  before changing it.
- `architecture-planning` — right-sized design, reuse inventory, option
  comparison, risk register, acceptance criteria.
- `quality-first` — minimal justified changes, reuse before create, honest
  reporting.
- `root-cause-debugging` — evidence-based diagnosis with a failure log and a
  two-approach cap before escalation.
- `code-review` — severity-ranked, evidence-backed review of a diff or pull
  request.
- `testing-and-verification` — test selection, output interpretation, and an
  explicit verified/partial/unverified/failed classification.
- `token-efficient` — retrieval ladder and reporting discipline that cannot be
  satisfied by skipping investigation or verification.
- `catalog.json` — machine-readable discovery index (id, name, description,
  category, path, version, status, task types, technology tags).
- `scripts/validate.py` — library validation: delegates format conformance to
  `skills-ref`, then checks catalog drift, broken relative links, body budget,
  unreferenced resources, and committed credentials.
- Documentation: installation per agent, getting started, skill format,
  contribution rules, security model, roadmap.
- MIT license.

### Notes

- No executable code ships inside any skill directory.
- No dependency is required to use a skill; Python 3 and an optional
  `skills-ref` install are only needed to validate the repository.
- Agent integration paths were verified against vendor documentation on
  2026-11-18. Unverified claims are labelled in
  [docs/installation.md](docs/installation.md).

[1.0.0]: https://github.com/EnJirad/kon.ai/releases/tag/v1.0.0
