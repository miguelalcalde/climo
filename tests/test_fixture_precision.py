from __future__ import annotations

import unittest
from pathlib import Path

from help_tree.parsers import parse_help


ROOT = Path(__file__).resolve().parents[1]


FIXTURE_EXPECTATIONS = {
    "cargo-root.txt": {
        "include": {"build", "check", "clean", "doc", "new", "init", "add", "remove", "run", "test", "bench", "update", "search", "publish", "install", "uninstall"},
        "exclude": {"options", "list", "explain", "details"},
    },
    "openssl-root.txt": {
        "include": {"asn1parse", "ca", "ciphers", "cms", "dgst", "enc", "passwd", "rand", "req", "rsa", "s_client", "s_server", "sha256", "x509"},
        "exclude": {"Standard", "commands", "Message", "Digest", "Cipher"},
    },
    "pip3-root.txt": {
        "include": {"install", "download", "uninstall", "freeze", "list", "show", "check", "config", "cache", "wheel", "completion", "debug", "help"},
        "exclude": {"isolated", "verbose", "proxy", "timeout"},
    },
    "pnpm-root.txt": {
        "include": {"add", "import", "install", "install-test", "link", "prune", "rebuild", "remove", "update", "audit", "licenses", "list", "outdated", "exec", "run", "start", "test", "store"},
        "exclude": {"recursive", "prod", "dependency", "Options"},
    },
    "python3-root.txt": {
        "include": set(),
        "exclude": {"cmd", "mod", "file", "Options", "PYTHONPATH"},
    },
    "rg-root.txt": {
        "include": set(),
        "exclude": {"regexp", "file", "pre", "PATTERN", "PATH"},
    },
    "rsync-root.txt": {
        "include": set(),
        "exclude": {"source", "directory", "program", "filter"},
    },
    "ssh-root.txt": {
        "include": set(),
        "exclude": {"destination", "command", "argument", "query_option"},
    },
    "tar-root.txt": {
        "include": set(),
        "exclude": {"Create", "List", "Extract", "filename", "patterns"},
    },
}


class FixturePrecisionTests(unittest.TestCase):
    def test_fixture_command_sets(self) -> None:
        for fixture_name, expectation in FIXTURE_EXPECTATIONS.items():
            with self.subTest(fixture=fixture_name):
                path = ROOT / "fixtures" / fixture_name
                parsed = parse_help(path.read_text(encoding="utf-8"))
                names = {candidate.name for candidate in parsed.candidates}

                self.assertTrue(
                    expectation["include"].issubset(names),
                    f"missing {sorted(expectation['include'] - names)} from {fixture_name}; got {sorted(names)}",
                )
                self.assertFalse(
                    expectation["exclude"] & names,
                    f"unexpected {sorted(expectation['exclude'] & names)} in {fixture_name}; got {sorted(names)}",
                )


if __name__ == "__main__":
    unittest.main()

