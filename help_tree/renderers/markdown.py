"""Markdown renderer."""

from __future__ import annotations

from help_tree.models import CommandNode


def render_markdown(node: CommandNode) -> str:
    lines: list[str] = [f"# `{node.command}`", ""]
    if node.description:
        lines.extend([node.description, ""])
    lines.extend(["```text"])
    lines.extend(_command_lines(node))
    lines.extend(["```"])
    return "\n".join(lines).rstrip() + "\n"


def _command_lines(node: CommandNode) -> list[str]:
    nodes = node.children or [node]
    lines: list[str] = []
    for child in nodes:
        lines.extend(_command_lines_from_node(child))
    return lines


def _command_lines_from_node(node: CommandNode) -> list[str]:
    line = node.command
    description = _inline_text(node.description)
    if description:
        line = f"{line} # {description}"

    lines = [line]
    for child in node.children:
        lines.extend(_command_lines_from_node(child))
    return lines


def _inline_text(value: str) -> str:
    return " ".join(value.split())
