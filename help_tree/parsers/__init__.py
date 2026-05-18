"""Parser orchestration for CLI help text."""

from __future__ import annotations

from help_tree.ansi import normalize_help
from help_tree.models import CommandCandidate, ParsedHelp
from help_tree.parsers.brew_usage import BrewUsageParser
from help_tree.parsers.comma_inventory import CommaInventoryParser
from help_tree.parsers.git_common import GitCommonParser
from help_tree.parsers.multiline_blocks import MultilineBlockParser
from help_tree.parsers.openssl_inventory import OpenSSLInventoryParser
from help_tree.parsers.pnpm_root import PnpmRootParser
from help_tree.parsers.section_table import SectionTableParser


PARSERS = (
    SectionTableParser(),
    CommaInventoryParser(),
    MultilineBlockParser(),
    GitCommonParser(),
    BrewUsageParser(),
    PnpmRootParser(),
    OpenSSLInventoryParser(),
)


def parse_help(text: str) -> ParsedHelp:
    normalized = normalize_help(text)
    parsed = ParsedHelp(
        usage=_extract_usage(normalized),
        description=_extract_description(normalized),
    )
    merged: dict[str, CommandCandidate] = {}
    for parser in PARSERS:
        for candidate in parser.parse(normalized):
            existing = merged.get(candidate.name)
            if existing is None or candidate.confidence > existing.confidence:
                merged[candidate.name] = candidate
    parsed.candidates = list(merged.values())
    return parsed


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
