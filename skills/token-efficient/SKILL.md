---
name: token-efficient
description: Use when the repository or context is large, a task touches many files, responses are getting verbose, tool calls are repeating, or a context budget is limited. Cuts retrieval and reporting waste without skipping investigation, testing, or security review.
license: MIT
---

# Token Efficient

Goal: spend context on the task, not on finding the task.

Priority order — never invert it:

1. Correctness and honesty.
2. Necessary investigation.
3. Necessary verification.
4. Context economy.

Saving tokens by loading less than you need is a bug, not an optimization.

## Retrieval ladder

Climb one step at a time. Stop as soon as you have what the next action needs.

| Step | Action | Typical tool |
| --- | --- | --- |
| 1 | List the directory before assuming its contents | `ls`, file listing |
| 2 | Search for the symbol, string, or filename | `grep`, `rg`, code search |
| 3 | Read a ranged slice around the hit | line-ranged read |
| 4 | Read the whole file | only when the structure is unclear |
| 5 | Read related files | only when a call site or type demands it |

Never open a file "for context" when a search would answer the question.

## Search before reading

- Search for the identifier, not the concept: `createOrder(`, not "order logic".
- Search the definition first, then the callers that change behavior.
- A match count of zero is information: record it, then widen the pattern once.
- If a search returns hundreds of hits, narrow by path or extension instead of
  reading them all.

## Reading

- Read the smallest range that answers the question; expand only on a boundary
  you must see (function start, type definition).
- For an unfamiliar file, read the top-level structure first: imports, exports,
  class or function signatures.
- Do not re-read a file you already read unless it changed or you need a section
  you skipped. Recall the earlier content instead.
- Prefer one ranged read over several tiny reads of the same file.

## Tool-call discipline

- Batch independent reads, searches, and listings in one round.
- Do not repeat an identical failed command. Change the input or the hypothesis.
- Do not re-run a passing check to "be sure" without a change in between.
- Prefer a tool's structured output over shelling out for the same information.
- Do not chain unrelated investigation into one command whose output you cannot
  attribute.

## Skill and resource loading

- Load a skill body only when its description matches the task (see
  `konai-core`).
- Do not load a reference or asset file the active skill does not require.
- Do not summarize a skill you loaded into your reply; act on it.

## Handoffs and subagents

- Delegate only work whose raw output you do not need: broad searches, wide
  comparisons, multi-file inventories.
- A delegation prompt must be self-contained: goal, scope, constraints, and the
  expected shape of the answer.
- Never delegate the final judgment about a change you are making.
- Do not round-trip a decision through a subagent that you can settle from
  evidence already in context.

## Reporting

- Lead with the outcome, then the evidence, then the limits.
- One line per fact. No restating the request, no narrating routine tool calls.
- Quote only the output lines that support the claim; trim the rest.
- Do not repeat the same content as prose and as a list.
- Do not paste whole files into the answer unless asked; cite path and lines.

## Never cut these

| Must keep | Why |
| --- | --- |
| The full error text | truncated errors cause wrong fixes |
| The failing test name and assertion | without it, no reproduction |
| Reading the code you change | guessing produces regressions |
| Requirements clarification | a wrong build is the most expensive outcome |
| Verification runs | unverified work is unfinished work |
| Security review of scripts and inputs | cheap to check, costly to skip |

## Signs you are wasting context

- Reading a file whose path you learned from a search hit without needing it.
- Opening five files to find a symbol that a targeted search locates directly.
- Explaining the plan in prose, then repeating it in the summary.
- Loading a second skill when the first already answers the question.
- Re-running a command because the earlier output scrolled away — keep the
  evidence you already have.
- Producing a long report for a one-line change.

## Measurement

When the project or host exposes it, report the cost of the work in the terms
available (files read, tool calls, elapsed time). Do not invent token counts;
if the host does not expose usage, do not estimate one.

## Failure conditions

Fall back to completeness, and say so, when:

- the task is genuinely cross-cutting and partial reading would mislead;
- a search result is ambiguous and only reading resolves it;
- correctness depends on data you have not opened.
