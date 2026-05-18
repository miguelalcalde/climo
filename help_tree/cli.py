"""Command-line interface for climo."""

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
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "crawl":
        argv[0] = "generate"

    parser = argparse.ArgumentParser(prog="climo")
    subparsers = parser.add_subparsers(dest="command", required=True, metavar="{parse,generate}")

    parse_parser = subparsers.add_parser("parse", help="parse a captured help file")
    parse_parser.add_argument("file", type=Path)
    parse_parser.add_argument("--format", choices=("json", "markdown"), default="json")

    generate_parser = subparsers.add_parser("generate", help="generate a CLI command tree")
    _add_generate_arguments(generate_parser)

    args = parser.parse_args(argv)

    if args.command == "parse":
        text = args.file.read_text(encoding="utf-8")
        parsed = parse_help(text)
        if args.format == "json":
            output = json.dumps(
                {
                    "header": parsed.header,
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
    output_format = "markdown" if args.description else args.format
    output = render_markdown(node) if output_format == "markdown" else render_json(node, include_raw=args.include_raw)
    if args.description:
        output = _render_skill_markdown(output, args.name or args.root.split()[0], args.description)
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


def _add_generate_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root", help="root command, e.g. 'gh' or 'docker compose'")
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--max-nodes", type=int, default=250)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--out", type=Path)
    parser.add_argument("--debug-out", type=Path)
    parser.add_argument("--name", help="skill name when writing a SKILL.md file")
    parser.add_argument("--description", help="skill description; writes Markdown output with SKILL.md frontmatter")


def _render_parsed_markdown(name: str, parsed) -> str:
    lines = [f"# {name}", ""]
    if parsed.header:
        lines.extend([parsed.header, ""])
    if parsed.description and parsed.description != parsed.header:
        lines.extend([parsed.description, ""])
    if parsed.usage:
        lines.extend([parsed.usage, ""])
    for candidate in parsed.candidates:
        line = candidate.name
        description = " ".join(candidate.description.split())
        if description:
            line = f"{line} # {description}"
        lines.append(line)
    return "\n".join(lines) + "\n"


def _render_skill_markdown(markdown: str, name: str, description: str) -> str:
    lines = [
        "---",
        f"name: {_quote_yaml_scalar(name)}",
        f"description: {_quote_yaml_scalar(description)}",
        "---",
        "",
        markdown.rstrip(),
        "",
    ]
    return "\n".join(lines)


def _quote_yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


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
