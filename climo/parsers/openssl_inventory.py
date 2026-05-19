"""Parses OpenSSL's columnar command inventory."""

from __future__ import annotations

import re

from climo.models import CommandCandidate
from climo.parsers.base import is_probable_command_name


OPENSSL_SECTIONS = (
    "Standard commands",
    "Message Digest commands",
    "Cipher commands",
)
TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")


class OpenSSLInventoryParser:
    source = "openssl_inventory"

    def parse(self, text: str) -> list[CommandCandidate]:
        candidates: list[CommandCandidate] = []
        active_section = ""

        for line in text.splitlines():
            stripped = line.strip()
            matched_section = next(
                (section for section in OPENSSL_SECTIONS if stripped.startswith(section)),
                None,
            )
            if matched_section:
                active_section = matched_section
                continue
            if not stripped:
                active_section = ""
                continue
            if not active_section:
                continue

            for token in TOKEN_RE.findall(stripped):
                if is_probable_command_name(token):
                    candidates.append(
                        CommandCandidate(
                            name=token,
                            section=active_section,
                            source=self.source,
                            confidence=0.72,
                            raw=token,
                        )
                    )

        return candidates

