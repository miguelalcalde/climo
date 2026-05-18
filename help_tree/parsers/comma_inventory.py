"""Parses wrapped comma-separated command inventories."""

from __future__ import annotations

import re

from help_tree.models import CommandCandidate
from help_tree.parsers.base import is_probable_command_name


TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_.-]*")


class CommaInventoryParser:
    source = "comma_inventory"

    def parse(self, text: str) -> list[CommandCandidate]:
        lines = text.splitlines()
        candidates: list[CommandCandidate] = []
        collecting = False
        buffer: list[str] = []

        for line in lines:
            stripped = line.strip()
            if stripped.lower() == "all commands:":
                collecting = True
                buffer = []
                continue

            if not collecting:
                continue

            if not stripped:
                if buffer:
                    break
                continue

            if "," not in stripped and buffer:
                break
            if not line.startswith((" ", "\t")):
                break

            buffer.append(stripped)

        for token in TOKEN_RE.findall(" ".join(buffer)):
            if is_probable_command_name(token):
                candidates.append(
                    CommandCandidate(
                        name=token,
                        section="All commands",
                        source=self.source,
                        confidence=0.82,
                        raw=token,
                    )
                )
        return candidates

