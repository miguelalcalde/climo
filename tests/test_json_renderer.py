from __future__ import annotations

import json
import unittest

from help_tree.models import CommandNode
from help_tree.renderers.json_renderer import render_json


class JsonRendererTests(unittest.TestCase):
    def test_render_json_omits_raw_help_by_default(self) -> None:
        node = CommandNode(path=["tool"], header="Tool CLI", raw_help="raw")

        payload = json.loads(render_json(node))

        self.assertEqual(payload["header"], "Tool CLI")
        self.assertNotIn("raw_help", payload)

    def test_render_json_includes_raw_help_when_requested(self) -> None:
        node = CommandNode(path=["tool"], raw_help="raw")

        payload = json.loads(render_json(node, include_raw=True))

        self.assertEqual(payload["raw_help"], "raw")


if __name__ == "__main__":
    unittest.main()
