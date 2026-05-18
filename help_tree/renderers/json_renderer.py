"""JSON renderer."""

from __future__ import annotations

import json

from help_tree.models import CommandNode


def render_json(node: CommandNode, include_raw: bool = False) -> str:
    return json.dumps(node.to_dict(include_raw=include_raw), indent=2, sort_keys=True) + "\n"

