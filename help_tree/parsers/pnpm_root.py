"""Parses pnpm's root help category sections."""

from __future__ import annotations

import re

from help_tree.models import CommandCandidate
from help_tree.parsers.base import is_probable_command_name


CATEGORY_SECTIONS = {
    "Manage your dependencies",
    "Review your dependencies",
    "Run your scripts",
    "Other",
    "Manage your store",
}
ROW_RE = re.compile(r"^\s{2,}(?P<spec>[a-z][a-z0-9_.-]*(?:\s*,\s*[a-z][a-z0-9_.-]*)?(?:\s+[a-z][a-z0-9_.-]*)?)\s{2,}(?P<desc>.+?)\s*$")


class PnpmRootParser:
    source = "pnpm_root"

    def parse(self, text: str) -> list[CommandCandidate]:
        candidates: dict[str, CommandCandidate] = {}
        active_section = ""

        for line in text.splitlines():
            stripped = line.strip()
            if stripped.endswith(":") and not line.startswith((" ", "\t")):
                section = stripped.rstrip(":")
                active_section = section if section in CATEGORY_SECTIONS else ""
                continue
            if not active_section or not stripped:
                continue

            match = ROW_RE.match(line)
            if not match:
                continue

            name = _canonical_name(match.group("spec"))
            if not is_probable_command_name(name):
                continue
            candidates.setdefault(
                name,
                CommandCandidate(
                    name=name,
                    description=match.group("desc").strip(),
                    section=active_section,
                    source=self.source,
                    subcommand_signal=" " in match.group("spec"),
                    confidence=0.76,
                    raw=stripped,
                ),
            )

        return list(candidates.values())


def _canonical_name(spec: str) -> str:
    pieces = [piece.strip() for piece in spec.split(",")]
    if len(pieces) > 1:
        first, second = pieces[0], pieces[1].split()[0]
        return second if len(first) <= 3 and len(second) > len(first) else first
    return pieces[0].split()[0]

