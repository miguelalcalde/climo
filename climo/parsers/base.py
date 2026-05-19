"""Parser protocol and shared parser helpers."""

from __future__ import annotations

import re
from typing import Protocol

from climo.models import CommandCandidate


COMMAND_NAME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9_.-]*\*?:?$")
SECTION_RE = re.compile(r"^[A-Z][A-Za-z0-9 /_-]*:?$")
ANY_HEADING_RE = re.compile(r"^[A-Za-z][A-Za-z0-9 /_-]*:?$")


class HelpParser(Protocol):
    source: str

    def parse(self, text: str) -> list[CommandCandidate]:
        ...


def clean_command_name(token: str) -> str:
    return token.strip().rstrip(":").rstrip("*")


def is_probable_command_name(token: str) -> bool:
    token = token.strip()
    if token.startswith("-"):
        return False
    if token.upper() == token and len(token) > 1:
        return False
    return bool(COMMAND_NAME_RE.match(token))


def section_name(line: str) -> str | None:
    stripped = line.strip()
    if not SECTION_RE.match(stripped):
        return None
    name = stripped.rstrip(":")
    lowered = name.lower()
    if lowered == "all commands" or lowered == "commands" or lowered.endswith(" commands"):
        return name
    return None


def looks_like_heading(line: str) -> bool:
    if line.startswith((" ", "\t")):
        return False
    stripped = line.strip()
    return bool(ANY_HEADING_RE.match(stripped))
