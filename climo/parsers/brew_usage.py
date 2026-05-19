"""Parses Homebrew's terse example-usage help output."""

from __future__ import annotations

import re

from climo.models import CommandCandidate
from climo.parsers.base import is_probable_command_name


BREW_ROW_RE = re.compile(r"^\s{2,}brew\s+(?P<name>[a-z][a-z0-9_.-]*)(?P<suffix>.*?)$")
BREW_HELP_RE = re.compile(r"^\s{2,}brew\s+help\s+\[COMMAND\]")
ROOT_HELP_SECTIONS = {"Example usage", "Troubleshooting", "Contributing", "Further help"}


class BrewUsageParser:
    source = "brew_usage"

    def parse(self, text: str) -> list[CommandCandidate]:
        candidates: dict[str, CommandCandidate] = {}
        active_section = ""

        for line in text.splitlines():
            stripped = line.strip()
            if stripped.endswith(":") and not line.startswith((" ", "\t")):
                section = stripped.rstrip(":")
                active_section = section if section in ROOT_HELP_SECTIONS else ""
                continue
            if BREW_HELP_RE.match(line):
                continue
            if not active_section:
                continue

            match = BREW_ROW_RE.match(line)
            if not match:
                continue
            name = match.group("name")
            if not is_probable_command_name(name):
                continue
            candidates.setdefault(
                name,
                CommandCandidate(
                    name=name,
                    description=stripped,
                    section=active_section,
                    source=self.source,
                    confidence=0.72,
                    raw=stripped,
                ),
            )

        return list(candidates.values())
