"""Command-line interface for help-tree."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from help_tree.crawler import CrawlOptions, HelpCrawler
from help_tree.parsers import parse_help
from help_tree.renderers.json_renderer import render_json
from help_tree.renderers.markdown import render_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="help-tree")
    subparsers = parser.add_subparsers(dest="command", required=True)

    parse_parser = subparsers.add_parser("parse", help="parse a captured help file")
    parse_parser.add_argument("file", type=Path)
    parse_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    crawl_parser = subparsers.add_parser("crawl", help="crawl a live CLI command")
    crawl_parser.add_argument("root", help="root command, e.g. 'gh' or 'docker compose'")
    crawl_parser.add_argument("--max-depth", type=int, default=3)
    crawl_parser.add_argument("--max-nodes", type=int, default=250)
    crawl_parser.add_argument("--timeout", type=float, default=3.0)
    crawl_parser.add_argument("--format", choices=("json", "markdown"), default="json")
    crawl_parser.add_argument("--include-raw", action="store_true")
    crawl_parser.add_argument("--out", type=Path)
    crawl_parser.add_argument("--debug-out", type=Path)

    args = parser.parse_args(argv)

    if args.command == "parse":
        text = args.file.read_text(encoding="utf-8")
        parsed = parse_help(text)
        if args.format == "json":
            output = json.dumps(
                {
                    "usage": parsed.usage,
                    "description": parsed.description,
                    "candidates": [candidate.to_dict() for candidate in parsed.candidates],
                    "flags": parsed.flags,
                },
                indent=2,
                sort_keys=True,
            )
            output += "\n"
        else:
            output = _render_parsed_markdown(args.file.name, parsed)
        sys.stdout.write(output)
        return 0

    options = CrawlOptions(
        max_depth=args.max_depth,
        max_nodes=args.max_nodes,
        timeout_seconds=args.timeout,
        include_raw=args.include_raw,
    )
    crawler = HelpCrawler(options=options)
    node = crawler.crawl(args.root)
    output = render_markdown(node) if args.format == "markdown" else render_json(node, include_raw=args.include_raw)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    if args.debug_out:
        args.debug_out.parent.mkdir(parents=True, exist_ok=True)
        args.debug_out.write_text(
            json.dumps(_debug_payload(node, crawler.debug_events, options), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    return 0


def _render_parsed_markdown(name: str, parsed) -> str:
    lines = [f"# {name}", ""]
    if parsed.usage:
        lines.extend(["```text", parsed.usage, "```", ""])
    lines.append("```text")
    for candidate in parsed.candidates:
        line = candidate.name
        description = " ".join(candidate.description.split())
        if description:
            line = f"{line} # {description}"
        lines.append(line)
    lines.append("```")
    return "\n".join(lines) + "\n"


def _debug_payload(node, events, options):
    accepted = [event for event in events if event["status"] == "accepted"]
    rejected = [event for event in events if event["status"] == "rejected"]
    nodes = _count_nodes(node)
    return {
        "root": node.command,
        "nodes": nodes,
        "max_depth": options.max_depth,
        "max_nodes": options.max_nodes,
        "truncated_by_node_cap": nodes >= options.max_nodes,
        "candidate_events": len(events),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "events": events,
    }


def _count_nodes(node) -> int:
    return 1 + sum(_count_nodes(child) for child in node.children)


if __name__ == "__main__":
    raise SystemExit(main())
