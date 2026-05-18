"""ANSI and whitespace normalization helpers."""

from __future__ import annotations

import re


ANSI_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text)


def normalize_help(text: str) -> str:
    """Return help text normalized for line-oriented parsing."""
    text = strip_ansi(text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join(lines)

