"""Validate generated Codex skill files."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
REQUIRED_FIELDS = {"name", "description"}


def main() -> int:
    errors: list[str] = []
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        errors.append("no skills found under skills/*/SKILL.md")

    for path in skill_files:
        errors.extend(validate_skill(path))

    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return [f"{path}: missing YAML frontmatter"]

    try:
        _, frontmatter, body = text.split("---", 2)
    except ValueError:
        return [f"{path}: malformed YAML frontmatter"]

    fields = parse_frontmatter(frontmatter)
    missing = REQUIRED_FIELDS - fields.keys()
    for field in sorted(missing):
        errors.append(f"{path}: missing frontmatter field {field!r}")
    for field in REQUIRED_FIELDS & fields.keys():
        if not fields[field].strip():
            errors.append(f"{path}: empty frontmatter field {field!r}")
    if not body.strip():
        errors.append(f"{path}: empty skill body")
    if path.parent.name != fields.get("name", path.parent.name):
        errors.append(f"{path}: frontmatter name does not match folder name")
    return errors


def parse_frontmatter(frontmatter: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            value = value[1:-1]
        fields[key.strip()] = value
    return fields


if __name__ == "__main__":
    raise SystemExit(main())
