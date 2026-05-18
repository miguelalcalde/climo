"""Markdown renderer."""

from __future__ import annotations

from help_tree.models import CommandNode


def render_markdown(node: CommandNode) -> str:
    lines: list[str] = [f"# `{node.command}`", ""]
    if node.header:
        lines.extend([node.header, ""])
    if node.description and node.description != node.header:
        lines.extend([node.description, ""])
    lines.extend(_command_lines(node))
    return "\n".join(lines).rstrip() + "\n"


def _command_lines(node: CommandNode) -> list[str]:
    line = _node_line(node)
    lines = [line]
    for index, child in enumerate(node.children):
        lines.extend(_command_lines_from_node(child, "", index == len(node.children) - 1))
    return lines


def _command_lines_from_node(node: CommandNode, prefix: str, is_last: bool) -> list[str]:
    line = _node_line(node)
    lines = [f"{prefix}{'└── ' if is_last else '├── '}{line}"]
    child_prefix = prefix + ("    " if is_last else "│   ")
    for index, child in enumerate(node.children):
        lines.extend(_command_lines_from_node(child, child_prefix, index == len(node.children) - 1))
    return lines


def _node_line(node: CommandNode) -> str:
    line = node.command
    if node.flags:
        line = f"{line} [{','.join(node.flags)}]"
    description = _inline_text(node.description)
    if description:
        line = f"{line} # {description}"
    return line


def _inline_text(value: str) -> str:
    return " ".join(value.split())
