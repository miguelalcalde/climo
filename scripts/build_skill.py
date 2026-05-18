"""Build a Codex skill from a crawled CLI help tree."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from help_tree.crawler import CrawlOptions, HelpCrawler
from help_tree.renderers.markdown import render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(prog="build_skill")
    parser.add_argument("root", help="root command to crawl, e.g. td")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--name", help="skill name; defaults to the root command")
    parser.add_argument("--description", required=True)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--max-nodes", type=int, default=250)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()

    skill_name = args.name or args.root.split()[0]
    crawler = HelpCrawler(
        options=CrawlOptions(
            max_depth=args.max_depth,
            max_nodes=args.max_nodes,
            timeout_seconds=args.timeout,
        )
    )
    tree = render_markdown(crawler.crawl(args.root))
    body = "\n".join(
        [
            "---",
            f"name: {quote_yaml_scalar(skill_name)}",
            f"description: {quote_yaml_scalar(args.description)}",
            "---",
            "",
            tree.rstrip(),
            "",
        ]
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(body, encoding="utf-8")
    return 0


def quote_yaml_scalar(value: str) -> str:
    escaped = re.sub(r"([\\\"])", r"\\\1", value)
    return f'"{escaped}"'


if __name__ == "__main__":
    raise SystemExit(main())
