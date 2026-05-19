"""Parses Git's grouped common-command help format."""

from __future__ import annotations

import re

from climo.models import CommandCandidate
from climo.parsers.base import is_probable_command_name


ROW_RE = re.compile(r"^\s{3,}(?P<name>[a-z][a-z0-9_.-]*)\s{2,}(?P<desc>.+?)\s*$")


class GitCommonParser:
    source = "git_common"

    def parse(self, text: str) -> list[CommandCandidate]:
        candidates: list[CommandCandidate] = []
        active_section = ""
        in_git_common = False

        for line in text.splitlines():
            stripped = line.strip()
            if stripped == "These are common Git commands used in various situations:":
                in_git_common = True
                continue
            if not in_git_common:
                continue
            if stripped.startswith("'git help"):
                break
            if not stripped:
                continue

            match = ROW_RE.match(line)
            if match:
                name = match.group("name")
                if is_probable_command_name(name):
                    candidates.append(
                        CommandCandidate(
                            name=name,
                            description=match.group("desc"),
                            section=active_section,
                            source=self.source,
                            confidence=0.8,
                            raw=stripped,
                        )
                    )
                continue

            if not line.startswith((" ", "\t")):
                active_section = stripped

        return candidates

