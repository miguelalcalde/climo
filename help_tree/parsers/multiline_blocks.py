"""Parses command blocks where the description is on the next indented line."""

from __future__ import annotations

import re

from help_tree.models import CommandCandidate
from help_tree.parsers.base import clean_command_name, is_probable_command_name, looks_like_heading, section_name


FIRST_LINE_RE = re.compile(
    r"^\s{2,}(?P<name>[A-Za-z][A-Za-z0-9_.-]*)(?:\s+\((?P<aliases>[^)]+)\))?(?P<suffix>.*?)$"
)


class MultilineBlockParser:
    source = "multiline_blocks"

    def parse(self, text: str) -> list[CommandCandidate]:
        lines = text.splitlines()
        candidates: list[CommandCandidate] = []
        active_section = ""
        in_commands = False
        index = 0

        while index < len(lines):
            line = lines[index]
            heading = section_name(line)
            if heading:
                active_section = heading
                in_commands = heading.lower() == "commands"
                index += 1
                continue
            if looks_like_heading(line):
                in_commands = False
                active_section = ""
                index += 1
                continue

            if not in_commands or not line.strip():
                index += 1
                continue

            match = FIRST_LINE_RE.match(line)
            if not match:
                index += 1
                continue

            name = clean_command_name(match.group("name"))
            suffix = match.group("suffix").strip()
            if not _looks_like_command_signature(suffix, match.group("aliases")):
                index += 1
                continue
            if not is_probable_command_name(name):
                index += 1
                continue

            description = ""
            if index + 1 < len(lines):
                next_line = lines[index + 1]
                if next_line.startswith("    ") and next_line.strip():
                    description = next_line.strip()

            aliases = tuple(
                alias.strip()
                for alias in (match.group("aliases") or "").split(",")
                if alias.strip()
            )
            candidates.append(
                CommandCandidate(
                    name=name,
                    aliases=aliases,
                    description=description,
                    section=active_section,
                    source=self.source,
                    subcommand_signal="<command>" in suffix.lower(),
                    confidence=0.9,
                    raw=line.strip(),
                )
            )
            index += 2 if description else 1

        return candidates


def _looks_like_command_signature(suffix: str, aliases: str | None) -> bool:
    if aliases:
        return True
    return any(marker in suffix for marker in ("[", "<", "..."))
