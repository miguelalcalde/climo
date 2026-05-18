"""Capture root help fixtures for installed CLI tools."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FixtureSpec:
    name: str
    argv: tuple[str, ...]
    output: str


FIXTURES = (
    FixtureSpec("python3-root", ("python3", "--help"), "fixtures/python3-root.txt"),
    FixtureSpec("pip3-root", ("pip3", "--help"), "fixtures/pip3-root.txt"),
    FixtureSpec("cargo-root", ("cargo", "--help"), "fixtures/cargo-root.txt"),
    FixtureSpec("rg-root", ("rg", "--help"), "fixtures/rg-root.txt"),
    FixtureSpec("pnpm-root", ("pnpm", "--help"), "fixtures/pnpm-root.txt"),
    FixtureSpec("openssl-root", ("openssl", "help"), "fixtures/openssl-root.txt"),
    FixtureSpec("ssh-root", ("ssh", "-h"), "fixtures/ssh-root.txt"),
    FixtureSpec("tar-root", ("tar", "--help"), "fixtures/tar-root.txt"),
    FixtureSpec("rsync-root", ("rsync", "--help"), "fixtures/rsync-root.txt"),
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="fixtures/manifest.json")
    parser.add_argument("--timeout", type=float, default=5.0)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = []

    for spec in FIXTURES:
        executable = shutil.which(spec.argv[0])
        record = {
            "name": spec.name,
            "argv": list(spec.argv),
            "output": spec.output,
            "available": bool(executable),
            "executable": executable,
        }
        if not executable:
            manifest.append(record)
            continue

        result = run(spec.argv, timeout=args.timeout)
        output_path = Path(spec.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.stdout + result.stderr, encoding="utf-8")
        record.update(
            {
                "returncode": result.returncode,
                "bytes": output_path.stat().st_size,
            }
        )
        manifest.append(record)

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {manifest_path}")
    for record in manifest:
        status = "ok" if record["available"] else "missing"
        argv = " ".join(shlex.quote(part) for part in record["argv"])
        print(f"{status:7} {record['name']:16} {argv}")
    return 0


def run(argv: tuple[str, ...], timeout: float) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env.update({"NO_COLOR": "1", "CLICOLOR": "0", "TERM": "dumb", "PAGER": "cat"})
    return subprocess.run(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=timeout,
        env=env,
        check=False,
    )


if __name__ == "__main__":
    raise SystemExit(main())

