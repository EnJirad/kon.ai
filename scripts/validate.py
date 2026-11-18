#!/usr/bin/env python3
"""Validate the KonAI skill library.

Spec conformance (frontmatter, naming, directory/name match) is delegated to the
official Agent Skills reference validator, `skills-ref`, when it is installed:

    pip install git+https://github.com/agentskills/agentskills.git#subdirectory=skills-ref

This script adds the repository-level checks the official validator does not
perform:

  * catalog.json stays in sync with the skills on disk (no drift, no duplicates)
  * relative links inside skills resolve and stay inside the skill directory
  * relative links in repository documentation resolve
  * SKILL.md bodies stay within the progressive-disclosure budget
  * resource files are referenced by the skill that ships them
  * no obvious credential material is committed

Usage:
    python3 scripts/validate.py              # whole library
    python3 scripts/validate.py skills/x     # selected skill directories
    python3 scripts/validate.py --strict     # treat warnings as failures

Exit code 0 when no errors, 1 otherwise. Stdlib only.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path

MAX_SKILL_LINES = 500
MAX_SKILL_TOKENS = 5000  # estimated, per the Agent Skills recommendation
VALID_STATUS = {"stable", "beta", "draft", "deprecated"}
CATALOG_REQUIRED = (
    "id",
    "name",
    "description",
    "category",
    "path",
    "version",
    "status",
    "task_types",
)
RESOURCE_DIRS = ("references", "scripts", "assets")
SECRET_PATTERNS = (
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}"), "OpenAI-style API key"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}"), "GitHub token"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key id"),
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"(?i)\b(?:password|passwd|secret|api[_-]?key)\s*[:=]\s*['\"][^'\"\s]{8,}['\"]"), "inline credential"),
)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: Path | str, message: str) -> None:
        self.errors.append(f"ERROR  {where}: {message}")

    def warn(self, where: Path | str, message: str) -> None:
        self.warnings.append(f"WARN   {where}: {message}")


def find_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "catalog.json").exists() and (candidate / "skills").is_dir():
            return candidate
    return start


def official_validator() -> str | None:
    from shutil import which

    return which("skills-ref")


def read_properties(skill_dir: Path) -> dict:
    """Return {name, description} using the official parser, else a fallback."""
    exe = official_validator()
    if exe:
        try:
            out = subprocess.run(
                [exe, "read-properties", str(skill_dir)],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            return json.loads(out)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            pass
    return parse_frontmatter(skill_dir / "SKILL.md")


def parse_frontmatter(path: Path) -> dict:
    """Minimal top-level YAML reader for name/description/license only."""
    props: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return props
    if not text.startswith("---"):
        return props
    end = text.find("\n---", 3)
    if end == -1:
        return props
    for line in text[3:end].splitlines():
        match = re.match(r"^([a-z][a-z0-9-]*):\s*(.*)$", line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        props[key] = value
    return props


def body_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4 :]
    return text


def strip_fences(text: str) -> str:
    """Remove fenced code blocks so example links are not treated as real ones."""
    return re.sub(r"```.*?```", "", text, flags=re.S)


def check_official(skill_dir: Path, report: Report) -> None:
    exe = official_validator()
    if not exe:
        report.warn(
            skill_dir.name,
            "skills-ref not found; spec conformance checks were skipped "
            "(install it to verify the Agent Skills format)",
        )
        return
    proc = subprocess.run(
        [exe, "validate", str(skill_dir)], capture_output=True, text=True
    )
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout).strip().replace("\n", " ")
        report.error(skill_dir.name, f"official validator failed: {detail}")


def check_budget(skill_dir: Path, report: Report) -> None:
    path = skill_dir / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    body = body_text(path)
    tokens = (len(body) + 3) // 4  # rough 4 chars per token
    if lines > MAX_SKILL_LINES:
        report.warn(
            skill_dir.name,
            f"SKILL.md is {lines} lines (> {MAX_SKILL_LINES}); move detail into references/",
        )
    if tokens > MAX_SKILL_TOKENS:
        report.warn(
            skill_dir.name,
            f"SKILL.md body is ~{tokens} tokens (> {MAX_SKILL_TOKENS}); move detail into references/",
        )


def check_links(skill_root: Path, skill_dir: Path, report: Report) -> None:
    for md in sorted(skill_dir.rglob("*.md")):
        rel = md.relative_to(skill_dir)
        text = strip_fences(md.read_text(encoding="utf-8"))
        for raw in LINK_RE.findall(text):
            target = raw.strip().split(" ")[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].strip("`'\"<>")
            if not target:
                continue
            resolved = posixpath.normpath(
                posixpath.join(rel.parent.as_posix(), target)
            )
            if resolved.startswith(".."):
                report.error(
                    f"{skill_dir.name}/{rel}",
                    f"link escapes the skill directory: {raw}",
                )
                continue
            if not (skill_dir / resolved).exists():
                report.error(
                    f"{skill_dir.name}/{rel}",
                    f"broken relative link: {raw}",
                )


def check_doc_links(root: Path, report: Report) -> None:
    """Verify relative links in repository-level docs resolve."""
    docs = [p for p in root.glob("*.md") if p.is_file()]
    docs += [p for p in (root / "docs").rglob("*.md") if p.is_file()]
    for md in sorted(docs):
        text = strip_fences(md.read_text(encoding="utf-8"))
        for raw in LINK_RE.findall(text):
            target = raw.strip().split(" ")[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].strip("`'\"<>")
            if not target:
                continue
            resolved = posixpath.normpath(
                posixpath.join(md.parent.relative_to(root).as_posix(), target)
            )
            if resolved.startswith(".."):
                report.error(
                    md.relative_to(root), f"link escapes the repository: {raw}"
                )
                continue
            if not (root / resolved).exists():
                report.error(md.relative_to(root), f"broken relative link: {raw}")


def check_orphans(skill_dir: Path, report: Report) -> None:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    for sub in RESOURCE_DIRS:
        base = skill_dir / sub
        if not base.is_dir():
            continue
        for item in sorted(base.rglob("*")):
            if item.is_dir() or item.name.startswith("."):
                continue
            rel = item.relative_to(skill_dir).as_posix()
            name = item.name
            if rel not in text and name not in text:
                report.warn(
                    skill_dir.name,
                    f"resource not referenced from SKILL.md: {rel}",
                )


def check_secrets(skill_dir: Path, report: Report) -> None:
    for item in sorted(skill_dir.rglob("*")):
        if not item.is_file() or item.stat().st_size > 512_000:
            continue
        try:
            text = item.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(text):
                report.error(
                    item.relative_to(skill_dir.parent),
                    f"possible committed credential ({label})",
                )


def check_catalog(root: Path, skill_dirs: list[Path], report: Report) -> None:
    path = root / "catalog.json"
    try:
        catalog = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.error("catalog.json", f"unreadable or invalid JSON: {exc}")
        return

    entries = catalog.get("skills")
    if not isinstance(entries, list) or not entries:
        report.error("catalog.json", "'skills' must be a non-empty array")
        return
    if not catalog.get("schema_version"):
        report.error("catalog.json", "missing 'schema_version'")

    by_id: dict[str, dict] = {}
    on_disk = {d.name for d in skill_dirs}

    for entry in entries:
        if not isinstance(entry, dict):
            report.error("catalog.json", "skill entry is not an object")
            continue
        skill_id = entry.get("id", "<missing id>")
        missing = [f for f in CATALOG_REQUIRED if not entry.get(f)]
        if missing:
            report.error("catalog.json", f"{skill_id}: missing fields {missing}")
        if skill_id in by_id:
            report.error("catalog.json", f"duplicate skill id: {skill_id}")
        by_id[skill_id] = entry

        status = entry.get("status")
        if status and status not in VALID_STATUS:
            report.error(
                "catalog.json",
                f"{skill_id}: status '{status}' not in {sorted(VALID_STATUS)}",
            )

        declared = entry.get("path")
        if declared and declared != f"skills/{skill_id}":
            report.error(
                "catalog.json",
                f"{skill_id}: path '{declared}' should be 'skills/{skill_id}'",
            )
        if entry.get("name") and entry["name"] != skill_id:
            report.error(
                "catalog.json",
                f"{skill_id}: name '{entry['name']}' must equal id",
            )

        skill_dir = root / "skills" / skill_id
        if not skill_dir.is_dir():
            report.error("catalog.json", f"{skill_id}: directory missing on disk")
            continue

        props = read_properties(skill_dir)
        if props.get("name") and props["name"] != skill_id:
            report.error(
                skill_id,
                f"frontmatter name '{props['name']}' does not match directory",
            )
        canonical = props.get("description", "")
        declared_desc = entry.get("description", "")
        if canonical and declared_desc != canonical:
            report.error(
                "catalog.json",
                f"{skill_id}: description drift — update it from SKILL.md "
                "(they must be identical)",
            )

    for name in sorted(on_disk - set(by_id)):
        report.error("catalog.json", f"skill on disk missing from catalog: {name}")


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    args = [a for a in argv if a != "--strict"]
    root = find_root(Path(__file__).resolve().parent.parent)
    os.chdir(root)

    all_dirs = sorted(p for p in (root / "skills").iterdir() if p.is_dir())
    if args:
        targets = [Path(a).resolve() for a in args]
        skill_dirs = [d for d in all_dirs if d in targets or d.parent in targets]
        if not skill_dirs:
            print("No skill directories matched.", file=sys.stderr)
            return 1
    else:
        skill_dirs = all_dirs

    report = Report()
    if not skill_dirs:
        report.error("skills/", "no skill directories found")

    for skill_dir in skill_dirs:
        if not (skill_dir / "SKILL.md").is_file():
            report.error(skill_dir.name, "missing SKILL.md")
            continue
        check_official(skill_dir, report)
        check_budget(skill_dir, report)
        check_links(root, skill_dir, report)
        check_orphans(skill_dir, report)
        check_secrets(skill_dir, report)

    if not args or len(skill_dirs) == len(all_dirs):
        check_catalog(root, all_dirs, report)
        check_doc_links(root, report)

    for line in report.errors + report.warnings:
        print(line)
    print(
        f"\n{len(skill_dirs)} skill(s) checked | "
        f"{len(report.errors)} error(s) | {len(report.warnings)} warning(s)"
    )

    if report.errors:
        return 1
    if strict and report.warnings:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
