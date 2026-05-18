from __future__ import annotations

import unittest

from help_tree.models import CommandNode
from help_tree.renderers.markdown import render_markdown


class MarkdownRendererTests(unittest.TestCase):
    def test_render_markdown_uses_compact_inline_command_list(self) -> None:
        node = CommandNode(
            path=["td"],
            header="td 1.0.0",
            description="Top-level help",
            flags=["--version"],
            children=[
                CommandNode(path=["td", "add"], description="Add a document"),
                CommandNode(path=["td", "changelog"], description="Show changes"),
                CommandNode(
                    path=["td", "hc"],
                    description="Help center commands",
                    children=[
                        CommandNode(
                            path=["td", "hc", "locales"],
                            description="List locales",
                            flags=["--json", "--raw"],
                        ),
                        CommandNode(path=["td", "hc", "view"]),
                    ],
                ),
            ],
        )

        self.assertEqual(
            render_markdown(node),
            """# `td`

td 1.0.0

Top-level help

td [--version] # Top-level help
├── td add # Add a document
├── td changelog # Show changes
└── td hc # Help center commands
    ├── td hc locales [--json,--raw] # List locales
    └── td hc view
""",
        )

    def test_render_markdown_includes_root_when_it_has_no_children(self) -> None:
        node = CommandNode(path=["td"], header="Top-level help", description="Top-level help")

        self.assertEqual(
            render_markdown(node),
            """# `td`

Top-level help

td # Top-level help
""",
        )


if __name__ == "__main__":
    unittest.main()
