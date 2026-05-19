"""Command-specific help strategy profiles."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Profile:
    name: str
    help_templates: tuple[str, ...] = ("{command} --help", "{command} -h")


PROFILES: dict[str, Profile] = {
    "npm": Profile(
        name="npm",
        help_templates=(
            "{command} --help",
            "{command} -h",
            "npm help {path}",
        ),
    ),
    "openssl": Profile(
        name="openssl",
        help_templates=(
            "{command} -help",
            "{command} --help",
            "openssl help {path}",
        ),
    ),
    "pnpm": Profile(
        name="pnpm",
        help_templates=(
            "{command} --help",
            "{command} -h",
            "pnpm help {path}",
        ),
    ),
}


def profile_for(root: str) -> Profile:
    root_name = root.split()[0]
    return PROFILES.get(root_name, Profile(name=root_name))
