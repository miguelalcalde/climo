"""Data models for parsed and crawled CLI help."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CommandCandidate:
    name: str
    description: str = ""
    aliases: tuple[str, ...] = ()
    section: str = ""
    source: str = ""
    subcommand_signal: bool = False
    confidence: float = 0.0
    raw: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "aliases": list(self.aliases),
            "section": self.section,
            "source": self.source,
            "subcommand_signal": self.subcommand_signal,
            "confidence": self.confidence,
            "raw": self.raw,
        }


@dataclass
class ParsedHelp:
    usage: str = ""
    description: str = ""
    candidates: list[CommandCandidate] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)


@dataclass
class CommandNode:
    path: list[str]
    usage: str = ""
    description: str = ""
    candidates: list[CommandCandidate] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    children: list["CommandNode"] = field(default_factory=list)
    raw_help: str = ""
    validation: dict[str, Any] = field(default_factory=dict)

    @property
    def command(self) -> str:
        return " ".join(self.path)

    def to_dict(self, include_raw: bool = False) -> dict[str, Any]:
        data: dict[str, Any] = {
            "command": self.command,
            "path": self.path,
            "usage": self.usage,
            "description": self.description,
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "flags": self.flags,
            "children": [child.to_dict(include_raw=include_raw) for child in self.children],
            "validation": self.validation,
        }
        if include_raw:
            data["raw_help"] = self.raw_help
        return data
