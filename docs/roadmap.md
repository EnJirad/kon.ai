# Roadmap

Technology-specific skills are **not** built yet. This file records the order in
which they will be considered and the bar each must clear. Dates are deliberately
absent: a skill ships when it is correct, not when a calendar says so.

## Why nothing technology-specific exists yet

The eight core skills change procedure and apply to any stack. A technology skill
changes *knowledge*, and knowledge rots: framework versions move, APIs are
deprecated, idioms change. Each one is a maintenance commitment, not a content
addition.

Adding `react` because it is popular produces a skill that is confidently wrong
in eighteen months. Adding it because there is a specific class of failure the
core skills cannot prevent is a different thing.

## Admission criteria

A technology skill is added only when all of the following hold:

1. **Distinct content.** It carries knowledge the core skills do not: ecosystem
   conventions, build and test commands, framework-specific failure modes,
   version constraints.
2. **References, never restates.** It links to `project-discovery`,
   `root-cause-debugging`, `quality-first`, and `testing-and-verification`
   instead of copying them.
3. **A named failure it prevents.** "Useful for React" is not a criterion.
   "Prevents the wrong render-phase side effect during migration from X to Y" is.
4. **Versioned assumptions.** It names the versions it is true for, in
   `compatibility` and in the body.
5. **Verifiable examples.** Commands and APIs are checked against current
   documentation, not memory.
6. **A maintainer.** Someone who will update it when the technology changes.
7. **Validated.** Passes `skills-ref validate` and `scripts/validate.py`.

## Priority order

Ordered by the frequency of the failure and the cost of getting it wrong, not by
popularity.

| # | Candidate | The gap it would close | Blocks |
| --- | --- | --- | --- |
| 1 | `android-development` | Gradle/SDK version alignment, manifest and permission changes, device-verification limits | emulator vs. device evidence, build reproducibility |
| 2 | `web-frontend` | bundler and dev-server behavior, asset pipelines, browser-only verification | "it works in the build" claims |
| 3 | `testing-strategy-js` | runner selection and interpretation for Jest/Vitest/Playwright, mocking boundaries | false-positive suites |
| 4 | `react-nextjs` | server/client boundary mistakes, hydration and data-fetching errors | the most common framework-level bug class |
| 5 | `backend-api` | contract versioning, idempotency, pagination, error envelopes | silent client breakage |
| 6 | `database-migrations` | reversible migrations, online DDL, backfill ordering | data loss |
| 7 | `kotlin-jvm` | coroutine and build-tooling failure modes | concurrency bugs |
| 8 | `python-engineering` | packaging, virtual environments, dependency resolution | unreproducible environments |
| 9 | `rust-engineering` | borrow-checker diagnosis, feature flags, unsafe boundaries | stalled debugging |
| 10 | `devops-infrastructure` | plan/apply safety, secret handling, rollout and rollback | irreversible infrastructure changes |
| 11 | `security-review` | authz boundaries, injection classes, secret flow | shipping vulnerabilities |
| 12 | `performance-optimization` | measurement before optimization, profiling, budget setting | speculative rewrites |

Order is a starting point. A candidate moves up when a real contributing failure
appears in an issue with evidence.

## Explicitly not planned

- **Persona and tone skills.** They change style, not capability.
- **Wrapper skills** that restate a vendor's documentation.
- **Framework-of-the-month skills** without a maintainer.
- **Skills that require a paid service** to be useful.
- **A package manager or installer.** Git, `gh skill`, symlinks, and plugins
  already distribute a folder containing `SKILL.md`. Adding a registry would add
  maintenance without making a skill more portable.

## How to propose one

Open an issue containing: the failure the skill prevents, a real task where the
core skills were insufficient, the versions in scope, and whether you will
maintain it. See [CONTRIBUTING.md](../CONTRIBUTING.md).
