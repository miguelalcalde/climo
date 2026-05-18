from __future__ import annotations

import unittest

from help_tree.crawler import CrawlOptions, HelpCrawler
from help_tree.models import CommandCandidate
from help_tree.runner import CommandResult


ROOT_HELP = """Tool CLI

Usage: tool <command>

Commands:
  add      Add a document
  ghost    Missing child
  repeat   Repeats parent help
"""

ADD_HELP = """Add a document

Usage: tool add [options]

Options:
  --json    Output JSON
"""

UNKNOWN_HELP = "unknown command: ghost"


class FakeRunner:
    def __init__(self, outputs: dict[tuple[str, ...], str]) -> None:
        self.outputs = outputs
        self.calls: list[list[str]] = []

    def run(self, argv: list[str]) -> CommandResult:
        self.calls.append(argv)
        output = self.outputs.get(tuple(argv), "")
        return CommandResult(argv=argv, returncode=0 if output else 1, stdout=output, stderr="", duration_seconds=0.01)


class HelpCrawlerTests(unittest.TestCase):
    def test_crawl_accepts_valid_children_and_records_rejections(self) -> None:
        runner = FakeRunner(
            {
                ("tool", "--help"): ROOT_HELP,
                ("tool", "add", "--help"): ADD_HELP,
                ("tool", "ghost", "--help"): UNKNOWN_HELP,
                ("tool", "ghost", "-h"): UNKNOWN_HELP,
                ("tool", "repeat", "--help"): ROOT_HELP,
            }
        )

        crawler = HelpCrawler(options=CrawlOptions(max_depth=2), runner=runner)
        node = crawler.crawl("tool")

        self.assertEqual([child.command for child in node.children], ["tool add"])
        self.assertEqual(node.header, "Tool CLI")
        self.assertEqual(node.children[0].flags, ["--json"])
        events = {event["candidate"]: event for event in crawler.debug_events}
        self.assertEqual(events["add"]["status"], "accepted")
        self.assertEqual(events["ghost"]["reason"], "unknown command output")
        self.assertEqual(events["repeat"]["reason"], "same output as parent")

    def test_crawl_respects_max_depth(self) -> None:
        runner = FakeRunner(
            {
                ("tool", "--help"): ROOT_HELP,
                ("tool", "add", "--help"): ADD_HELP,
            }
        )

        node = HelpCrawler(options=CrawlOptions(max_depth=0), runner=runner).crawl("tool")

        self.assertEqual(node.children, [])
        self.assertEqual(runner.calls, [["tool", "--help"]])

    def test_crawl_respects_max_nodes(self) -> None:
        runner = FakeRunner(
            {
                ("tool", "--help"): ROOT_HELP,
                ("tool", "add", "--help"): ADD_HELP,
                ("tool", "ghost", "--help"): ADD_HELP,
            }
        )

        crawler = HelpCrawler(options=CrawlOptions(max_depth=2, max_nodes=2), runner=runner)
        node = crawler.crawl("tool")

        self.assertEqual([child.command for child in node.children], ["tool add"])
        self.assertEqual(len([event for event in crawler.debug_events if event["status"] == "accepted"]), 1)

    def test_rejects_unsafe_candidate_names_before_running_child_help(self) -> None:
        runner = FakeRunner({("tool", "--help"): ROOT_HELP})
        crawler = HelpCrawler(runner=runner)

        self.assertFalse(crawler._candidate_name_is_safe(CommandCandidate(name="bad/name")))
        self.assertFalse(crawler._candidate_name_is_safe(CommandCandidate(name="--flag")))
        self.assertFalse(crawler._candidate_name_is_safe(CommandCandidate(name="bad\x00name")))


if __name__ == "__main__":
    unittest.main()
