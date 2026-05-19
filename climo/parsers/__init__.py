"""Parser orchestration for CLI help text."""

from __future__ import annotations

import re

from climo.ansi import normalize_help
from climo.models import CommandCandidate, ParsedHelp
from climo.parsers.brew_usage import BrewUsageParser
from climo.parsers.comma_inventory import CommaInventoryParser
from climo.parsers.git_common import GitCommonParser
from climo.parsers.multiline_blocks import MultilineBlockParser
from climo.parsers.openssl_inventory import OpenSSLInventoryParser
from climo.parsers.pnpm_root import PnpmRootParser
from climo.parsers.section_table import SectionTableParser


PARSERS = (
    SectionTableParser(),
    CommaInventoryParser(),
    MultilineBlockParser(),
    GitCommonParser(),
    BrewUsageParser(),
    PnpmRootParser(),
    OpenSSLInventoryParser(),
)

FLAG_RE = re.compile(r"(?<!\S)-{1,2}[A-Za-z0-9][A-Za-z0-9-]*")
FLAG_SECTION_NAMES = {"options", "flags", "global options", "global flags"}
HELP_FLAGS = {"-h", "--help", "-help"}


def parse_help(text: str) -> ParsedHelp:
    normalized = normalize_help(text)
    parsed = ParsedHelp(
        header=_extract_header(normalized),
        usage=_extract_usage(normalized),
        description=_extract_description(normalized),
        flags=_extract_flags(normalized),
    )
    merged: dict[str, CommandCandidate] = {}
    for parser in PARSERS:
        for candidate in parser.parse(normalized):
            existing = merged.get(candidate.name)
            if existing is None or candidate.confidence > existing.confidence:
                merged[candidate.name] = candidate
    parsed.candidates = list(merged.values())
    return parsed


def _extract_header(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _extract_usage(text: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.lower() == "usage" and index + 1 < len(lines):
            return lines[index + 1].strip()
        if stripped.lower().startswith("usage:"):
            return stripped
    return ""


def _extract_description(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        lowered = stripped.lower()
        if lowered.startswith(("usage", "flags:", "options:", "commands:")):
            continue
        return stripped
    return ""


def _extract_flags(text: str) -> list[str]:
    flags: list[str] = []
    seen: set[str] = set()
    in_flag_section = False

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue

        lowered = stripped.rstrip(":").lower()
        if lowered in FLAG_SECTION_NAMES:
            in_flag_section = True
            continue

        if in_flag_section and _is_non_flag_section_heading(stripped):
            in_flag_section = False

        if not in_flag_section or not stripped.startswith("-"):
            continue

        names = [name for name in FLAG_RE.findall(stripped) if name not in HELP_FLAGS]
        if not names:
            continue
        flag = _canonical_flag_name(names)
        if flag not in seen:
            flags.append(flag)
            seen.add(flag)

    return flags


def _is_non_flag_section_heading(stripped: str) -> bool:
    if stripped.startswith("-"):
        return False
    lowered = stripped.rstrip(":").lower()
    if lowered in FLAG_SECTION_NAMES:
        return False
    return stripped.endswith(":") or lowered in {"commands", "examples", "usage", "arguments"}


def _canonical_flag_name(names: list[str]) -> str:
    long_names = [name for name in names if name.startswith("--")]
    if long_names:
        return long_names[0]
    return names[0]
