---
name: project-discovery
description: Use when starting work in an unfamiliar repository or an unread subsystem, before changing anything. Builds a compact, evidence-backed project profile — stack, entry points, build and test commands, conventions, and risks — with targeted probes instead of reading everything.
license: MIT
---

# Project Discovery

Goal: enough verified context to make a confident change, and no more.

A profile that invents its architecture is worse than no profile. Mark every
statement as **verified** (you saw the file or ran the command) or **inferred**
(the evidence suggests it).

## Probe order

Stop when the next action is safe. Do not read source files before step 5.

1. **Instructions first.** Look for and read `AGENTS.md`, `CLAUDE.md`,
   `.github/copilot-instructions.md`, `CONTRIBUTING.md`, and any
   `.harness/` or project-rules directory. Project rules outrank your defaults,
   including the skills in this library.
2. **Top-level shape.** List the repository root and one level down. Identify
   source roots, tooling directories, and the docs directory.
3. **Manifests.** Find the build and dependency manifests (see the table below).
   Read the manifest, not the lockfile. A lockfile is evidence of a resolved
   graph; open it only when versions matter.
4. **Commands.** Grep the manifest and CI config for the scripts or tasks that
   build, test, lint, and run the project. Prefer the documented command over an
   inferred one.
5. **Entry points.** Identify the process or app entry point, the public API
   surface, or the main module. Confirm by following one import path.
6. **Structure.** Sketch the top two levels of the source tree with one line per
   meaningful directory. Ignore the exclusions below.
7. **Conventions.** Sample two or three files in the same layer to see naming,
   error handling, and test layout. Do not sample the whole tree.
8. **Tests.** Locate the test command, the framework, and one representative
   test. Note whether tests are colocated or separate.
9. **Integration edges.** Database, external API, queue, or filesystem access.
   Read the configuration keys, never the secret values.
10. **State.** Current branch, uncommitted changes, and whether the working tree
    already contains unrelated work you must preserve.

## Exclusions

Do not read or inventory these unless the task is specifically about them:

`node_modules`, `vendor`, `dist`, `build`, `target`, `out`, `.next`, `coverage`,
`__pycache__`, `.gradle`, `Pods`, `.venv`, lockfiles, minified files, binaries,
images, generated sources, databases, logs, and any file matching secrets or
credentials patterns.

Never print the contents of `.env`, keystores, tokens, or key files. Read the
variable **names** from an example file instead.

## Ecosystem quick reference

| Manifest found | Stack signal | Build / test hint |
| --- | --- | --- |
| `package.json` | Node, JS/TS | read `scripts` for `build`, `test`, `lint`; check `packageManager` |
| `pnpm-workspace.yaml`, `turbo.json`, `nx.json` | monorepo | scope commands to the affected package |
| `pyproject.toml`, `requirements.txt` | Python | `pytest`, `ruff`, or `tox`; check the configured runner |
| `Cargo.toml` | Rust | `cargo build`, `cargo test`; check workspace members |
| `build.gradle` / `build.gradle.kts` | JVM or Android | `./gradlew` tasks; check `settings.gradle` modules |
| `AndroidManifest.xml` | Android app | Gradle module structure, `minSdk`, flavors |
| `pom.xml` | Java/Maven | `mvn verify`, module aggregation |
| `*.xcodeproj`, `Package.swift` | iOS/macOS | schemes, SPM dependencies |
| `go.mod` | Go | `go build ./...`, `go test ./...` |
| `Gemfile` | Ruby | `bundle exec rspec` |
| `composer.json` | PHP | `composer test` / `phpunit` |
| `Dockerfile`, `compose.yaml` | containerized | service topology and ports |
| `*.tf`, `chart/`, `k8s/` | infrastructure | plan/apply targets, environments |

Treat the hint column as a prompt to verify, not as a fact.

## Compact profile

Produce this before changing code. Keep it short; drop empty rows.

```markdown
## Project profile
- Purpose: <one sentence, verified from README or entry point>
- Stack: <language(s), framework(s), versions from manifests>
- Layout: <source root> / <tests> / <docs>
- Entry point: <path:line>
- Build: <command>            [verified: <how>]
- Test: <command>             [verified: <how>]
- Lint/format: <command or none>
- Data: <database/cache/external service or none>
- Conventions: <naming, error handling, test style — from sampled files>
- Rules: <project instruction files found, with the constraint that matters>
- Risks: <generated code, vendored code, flaky area, missing tests>
- Unknowns: <what you could not verify>
```

## Rules

- One probe per question. Do not open files to "get a feel".
- Prefer the project's own documentation over your inference.
- Absence of evidence is a finding: "no test command found" is a result, not a
  gap to fill by guessing.
- Do not describe architecture you have not traced. "Likely MVC" without a file
  that proves it is speculation; say "unverified".
- Do not assume a directory name implies behavior; confirm with one import or
  call site.
- Preserve existing work: note the branch and dirty files before editing.

## Stop condition

Stop discovering when you can answer, with evidence:

1. Where does the behavior I must change live?
2. How do I build and test it?
3. What project rules constrain the change?
4. What else consumes it?

Hand off to `architecture-planning` for design work, `quality-first` before
editing, and `testing-and-verification` before reporting.
