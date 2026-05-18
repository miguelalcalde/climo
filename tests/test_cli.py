from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from help_tree import cli
from help_tree.models import CommandNode


class FakeCrawler:
    instances: list["FakeCrawler"] = []

    def __init__(self, options) -> None:
        self.options = options
        self.debug_events = [
            {"status": "accepted", "candidate": "add"},
            {"status": "rejected", "candidate": "bad"},
        ]
        FakeCrawler.instances.append(self)

    def crawl(self, root: str) -> CommandNode:
        return CommandNode(
            path=[root],
            header="Tool CLI",
            description="Tool CLI",
            children=[CommandNode(path=[root, "add"], description="Add a document")],
            raw_help="raw help",
        )


class CliTests(unittest.TestCase):
    def test_help_uses_skill_tree_program_name(self) -> None:
        stdout = io.StringIO()

        with self.assertRaises(SystemExit) as raised:
            with contextlib.redirect_stdout(stdout):
                cli.main(["--help"])

        self.assertEqual(raised.exception.code, 0)
        self.assertIn("usage: skill-tree", stdout.getvalue())

    def test_parse_json_writes_header_usage_candidates_and_flags(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            help_file = Path(tmpdir) / "tool.txt"
            help_file.write_text(
                """Tool CLI

Usage: tool <command>

Commands:
  add      Add a document

Options:
  --json   Output JSON
""",
                encoding="utf-8",
            )
            stdout = io.StringIO()

            with contextlib.redirect_stdout(stdout):
                exit_code = cli.main(["parse", str(help_file), "--format", "json"])

        payload = json.loads(stdout.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertEqual(payload["header"], "Tool CLI")
        self.assertEqual(payload["usage"], "Usage: tool <command>")
        self.assertEqual(payload["flags"], ["--json"])
        self.assertEqual(payload["candidates"][0]["name"], "add")

    def test_crawl_writes_output_and_debug_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "tree.json"
            debug_path = Path(tmpdir) / "debug.json"
            FakeCrawler.instances = []

            with patch.object(cli, "HelpCrawler", FakeCrawler):
                exit_code = cli.main(
                    [
                        "crawl",
                        "tool",
                        "--max-depth",
                        "4",
                        "--max-nodes",
                        "12",
                        "--include-raw",
                        "--out",
                        str(out_path),
                        "--debug-out",
                        str(debug_path),
                    ]
                )

            output = json.loads(out_path.read_text(encoding="utf-8"))
            debug = json.loads(debug_path.read_text(encoding="utf-8"))

        self.assertEqual(exit_code, 0)
        self.assertEqual(FakeCrawler.instances[0].options.max_depth, 4)
        self.assertTrue(FakeCrawler.instances[0].options.include_raw)
        self.assertEqual(output["raw_help"], "raw help")
        self.assertEqual(debug["nodes"], 2)
        self.assertEqual(debug["accepted"], 1)
        self.assertEqual(debug["rejected"], 1)


if __name__ == "__main__":
    unittest.main()
