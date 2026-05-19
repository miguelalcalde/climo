"""Parses fixed-width and colon-delimited command sections."""

from __future__ import annotations

import re

from climo.models import CommandCandidate
from climo.parsers.base import clean_command_name, is_probable_command_name, looks_like_heading, section_name


ROW_RE = re.compile(
    r"^\s{2,}(?P<name>[A-Za-z][A-Za-z0-9_.-]*\*?:?(?:,\s*[A-Za-z][A-Za-z0-9_.-]*)?)\s{2,}(?P<desc>.+?)\s*$"
)


class SectionTableParser:
    source = "section_table"

    def parse(self, text: str) -> list[CommandCandidate]:
        candidates: list[CommandCandidate] = []
        active_section = ""
        in_command_section = False
        rows_seen_in_section = False

        for line in text.splitlines():
            heading = section_name(line)
            if heading:
                active_section = heading
                lowered = heading.lower()
                in_command_section = "command" in lowered and not lowered.startswith("all ")
                rows_seen_in_section = False
                continue
            if looks_like_heading(line):
                in_command_section = False
                active_section = ""
                rows_seen_in_section = False
                continue

            if not line.strip():
                if rows_seen_in_section:
                    in_command_section = False
                continue

            if not in_command_section:
                continue

            match = ROW_RE.match(line)
            if not match:
                if line[:1].strip():
                    in_command_section = False
                continue

            raw_name = match.group("name")
            name = _canonical_name(raw_name)
            if name[:1].isupper():
                continue
            if not is_probable_command_name(name):
                continue

            description = match.group("desc").strip()
            rows_seen_in_section = True
            candidates.append(
                CommandCandidate(
                    name=name,
                    description=description,
                    section=active_section,
                    source=self.source,
                    subcommand_signal="<command>" in description.lower(),
                    confidence=0.88,
                    raw=line.strip(),
                )
            )

        return candidates


def _canonical_name(raw_name: str) -> str:
    cleaned = clean_command_name(raw_name)
    pieces = [piece.strip() for piece in cleaned.split(",")]
    if len(pieces) > 1:
        first, second = pieces[0], pieces[1]
        return second if len(first) <= 3 and len(second) > len(first) else first
    return cleaned
