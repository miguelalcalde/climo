"""Markdown renderer."""

from __future__ import annotations

from help_tree.models import CommandNode


def render_markdown(node: CommandNode) -> str:
    lines: list[str] = [f"# `{node.command}`", ""]
    if node.description:
        lines.extend([node.description, ""])
    lines.extend(["## Command Tree", "", "```text"])
    lines.extend(_tree_lines(node))
    lines.extend(["```", ""])
    _append_sections(lines, node)
    return "\n".join(lines).rstrip() + "\n"


def _tree_lines(node: CommandNode, prefix: str = "", is_last: bool = True) -> list[str]:
    label = node.path[-1]
    lines = [label] if not prefix else [f"{prefix}{'└── ' if is_last else '├── '}{label}"]
    child_prefix = "" if not prefix else prefix + ("    " if is_last else "│   ")
    for index, child in enumerate(node.children):
        if not prefix:
            child_connector = "└── " if index == len(node.children) - 1 else "├── "
            lines.append(f"{child_connector}{child.path[-1]}")
            grandchild_prefix = "    " if index == len(node.children) - 1 else "│   "
            for grandchild_index, grandchild in enumerate(child.children):
                lines.extend(
                    _tree_lines(
                        grandchild,
                        grandchild_prefix,
                        grandchild_index == len(child.children) - 1,
                    )
                )
        else:
            lines.extend(_tree_lines(child, child_prefix, index == len(node.children) - 1))
    return lines


def _append_sections(lines: list[str], node: CommandNode) -> None:
    lines.extend([f"## `{node.command}`", ""])
    if node.usage:
        lines.extend(["Usage:", "", "```text", node.usage, "```", ""])
    if node.description:
        lines.extend([node.description, ""])
    if node.candidates:
        lines.extend(["Candidates:", "", "| Command | Section | Description | Source |", "|---|---|---|---|"])
        for candidate in node.candidates:
            lines.append(
                f"| `{candidate.name}` | {candidate.section} | {candidate.description} | {candidate.source} |"
            )
        lines.append("")
    for child in node.children:
        _append_sections(lines, child)
