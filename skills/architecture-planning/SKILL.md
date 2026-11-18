---
name: architecture-planning
description: Use before implementing a non-trivial feature or refactor, when choosing between technical approaches, or when deciding how much design is enough. Produces the smallest maintainable plan, with reuse of existing components, named risks, and testable acceptance criteria.
license: MIT
---

# Architecture Planning

Purpose: spend design effort proportional to the change, and no more.

A plan for a one-line fix is waste. Code for a cross-cutting change without a
plan is risk.

## Right-size gate

Ask first: **can this be done correctly with a local edit?** If yes, do it and
skip this skill. Planning is warranted when the change:

- crosses more than one module, service, or layer;
- changes a contract others depend on (API shape, schema, event, file format);
- introduces a dependency, background process, or new storage;
- has more than one plausible approach with different trade-offs;
- cannot be verified cheaply after the fact.

## Steps

1. **Restate the requirement** in one sentence, plus what is explicitly out of
   scope.
2. **Collect constraints**: project rules, existing conventions, platform limits,
   compatibility requirements, deadline or budget signals stated by the user.
3. **Inspect the current architecture** using `project-discovery`. You cannot
   extend a design you have not read.
4. **Inventory reuse.** List existing components that already solve part of the
   problem. Planning that ignores them creates a duplicate system.
5. **Compare at most three options.** More are rarely distinct.
6. **Pick one and justify it** against the criteria, not against taste.
7. **Name the risks** and their early warning signals.
8. **Define acceptance criteria** that a test can decide.
9. **Define the verification plan** before implementation starts.
10. **Write it down compactly** — a plan nobody can check is not a plan.

## Reuse inventory

For each candidate: what it does, why it does not fully fit (or does), and
whether extending it is cheaper than adding alongside it.

Prefer, in order: extend existing → compose existing → extract a shared piece
with more than one caller → build new.

Never add a second mechanism for a problem the codebase already solves.

## Option comparison

```markdown
| Option | Fits constraints | New surface | Risk | Reversibility | Cost to maintain |
|--------|------------------|-------------|------|---------------|------------------|
| A (reuse X) | ... | ... | ... | ... | ... |
| B (extend Y) | ... | ... | ... | ... | ... |
```

Rules:

- Two options minimum, three maximum.
- Score against the constraints from step 2, not general preference.
- Prefer the option that is easiest to undo when uncertainty is high.
- State the deciding factor in one sentence.

## Smallest suitable design

- Solve the stated requirement; do not anticipate the next three features.
- No abstraction with one implementation and no second caller in sight.
- No configuration option without a concrete case that needs it.
- No new service when a function is enough; no new table when a column is
  enough; no new queue when a synchronous call is fast enough.
- New dependencies need a stated reason and a rejected simpler alternative.
- Keep boundaries where they already are unless a boundary is the problem.

## Risk register

```markdown
| Risk | Likelihood | Impact | Early signal | Mitigation |
|------|-----------|--------|--------------|------------|
```

Include at least: data loss or migration, contract breakage for existing
consumers, performance under real volume, and failure of the chosen approach
being invisible.

## Acceptance criteria

Each criterion must be:

- **decidable** — there is a check that returns pass or fail;
- **observable** — from the outside of the implementation;
- **scoped** — the requirement, not the implementation detail.

```markdown
- [ ] <observable behavior> — verified by <test or command>
```

If a criterion cannot be tested in this environment, say so at planning time,
not at report time.

## Decision record

Keep it short enough to live next to the code or in the pull request:

```markdown
### Decision: <title>
- Context: <problem and constraints>
- Options: <A, B — one line each>
- Chosen: <option> because <deciding factor>
- Consequences: <what becomes easier, what becomes harder>
- Revisit if: <signal that invalidates this choice>
```

## Failure conditions

Stop planning and escalate when:

- the requirement depends on product behavior only the user can decide;
- two options differ only on facts you cannot measure here;
- the smallest correct design still requires a migration, downtime, or
  irreversible change;
- project rules forbid the only acceptable approach.

## Handoff

Hand the chosen design to `quality-first` for implementation and
`testing-and-verification` for evidence. Use `code-review` on the result against
the acceptance criteria, not against the plan's prose.
