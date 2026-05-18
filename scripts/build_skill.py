"""Build a Codex skill from a generated CLI help tree."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from help_tree.cli import main as cli_main


def main() -> int:
    parser = argparse.ArgumentParser(prog="build_skill")
    parser.add_argument("root", help="root command to generate, e.g. td")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--name", help="skill name; defaults to the root command")
    parser.add_argument("--description", required=True)
    parser.add_argument("--max-depth", type=int, default=3)
    parser.add_argument("--max-nodes", type=int, default=250)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()

    argv = [
        "generate",
        args.root,
        "--out",
        str(args.out),
        "--description",
        args.description,
        "--max-depth",
        str(args.max_depth),
        "--max-nodes",
        str(args.max_nodes),
        "--timeout",
        str(args.timeout),
    ]
    if args.name:
        argv.extend(["--name", args.name])
    return cli_main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
