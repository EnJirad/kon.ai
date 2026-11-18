# Security

## What a skill is, from a security standpoint

A skill is **untrusted instructional text that an AI agent may follow**. It is
closer to a script than to documentation: activating it can change what the agent
does next. Treat a skill you did not write the way you would treat a script you
did not write.

Skills are also **inert**. A repository containing a skill cannot execute
anything by itself. Execution requires the host agent to decide to run a command,
under that host's permission and approval rules. KonAI ships no auto-run hooks,
no install scripts, and no background services.

## Threat model

| Threat | How it happens | Mitigation in this repository |
| --- | --- | --- |
| Prompt injection inside a skill | instructions that redirect the agent away from the user's task, or tell it to ignore its own rules | skills are reviewed for scope; skills never override host rules; read the diff before installing an update |
| Destructive procedure | a skill that normalizes deleting, force-pushing, or rewriting history | no such procedure is shipped; approval stays with the host agent |
| Data exfiltration | a skill that tells the agent to send repository content somewhere | no network instructions in core skills; no bundled telemetry |
| Malicious script | executable code that does more than documented | no scripts are bundled in v1.0.0; any future script must be inspectable and opt-in |
| Secret leakage | keys committed in examples or fixtures | `scripts/validate.py` scans for common credential patterns; contributions are reviewed |
| Supply-chain drift | an upstream skill changes after you installed it | pinned tags/SHAs, CHANGELOG, review the diff on update |
| False confidence | a skill that claims verification it did not perform | skills require evidence and classify results; they forbid fabricated results |

Not in scope: model-level jailbreaks, host-agent vulnerabilities, and anything the
host agent is permitted to do regardless of skill content. A skill cannot expand
the agent's permissions, and this document does not claim otherwise.

## Safe usage

- **Install from this repository or a fork you trust.** Do not install a skill
  from a link that merely claims to be KonAI.
- **Read `SKILL.md` before installing.** It is short by design; that is one
  reason for the 500-line budget.
- **Pin a version** when a skill affects real work: a tag or commit SHA, not a
  moving branch.
- **Review updates like code.** `git diff v1.0.0..v1.1.0 -- skills/<name>`.
- **Prefer project scope** for team workflows, so the skill is reviewed in the
  same pull request as the code it governs.
- **Remove what you do not use.** An unused skill is unused attack surface and
  unused context.

## Script execution

KonAI v1.0.0 contains **no executable files**. If a future skill ships one:

1. Read it in full before running it. If you cannot read it, do not run it.
2. Check what it reads, what it writes, and whether it reaches the network.
3. Run it on a throwaway copy first when it mutates anything.
4. Never pipe a remote script into a shell.
5. Keep the agent's approval prompts enabled for writes and command execution.

A skill describing a command is not authorization to run it. The host agent's
permission rules and yours govern.

## Secrets

- Do not put credentials, tokens, keys, or customer data in a skill, an example,
  or a fixture. Use placeholder names: `API_TOKEN`, `<your-key>`.
- Skills must never instruct an agent to read `.env`, keystores, or credential
  files, or to print their contents.
- If a secret is committed by mistake, rotate it first, then remove it from
  history. Deleting the file in a new commit does not revoke the credential.
- `scripts/validate.py` flags common credential shapes. It is a heuristic, not a
  guarantee; review still matters.

## Dependency and permission expectations

The core skills assume only that the agent can read files, search, and run
commands. They do not require network access, package installation, or elevated
permissions. Any future skill with a heavier requirement must declare it in its
`compatibility` field and in its documentation.

## Reporting a vulnerability

Report privately through GitHub's **Report a vulnerability** flow on
<https://github.com/EnJirad/kon.ai/security/advisories/new>. If that is
unavailable, open an issue that describes the impact **without** a working
exploit and ask for a private channel.

Include: the skill and line, what an agent would do wrong, the conditions needed,
and a suggested fix. Expect an acknowledgement when the maintainer is available;
this is a volunteer project and no response-time guarantee is offered.

Please do not publish a working exploit before a fix is available.

## Limitations of this policy

- Validation checks structure and common credential shapes, not intent. A
  well-formatted skill can still contain bad advice.
- Review is human. Reviewers can miss things.
- Nothing here protects you from a host agent that ignores its own permission
  model.
