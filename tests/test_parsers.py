from __future__ import annotations

import unittest
from pathlib import Path

from help_tree.parsers import parse_help


ROOT = Path(__file__).resolve().parents[1]


def parse_fixture(name: str):
    return parse_help((ROOT / name).read_text(encoding="utf-8"))


class ParserFixtureTests(unittest.TestCase):
    def test_gh_section_tables(self) -> None:
        parsed = parse_fixture("example-gh.txt")
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertEqual(parsed.header, "Work seamlessly with GitHub from the command line.")
        self.assertEqual(parsed.usage, "gh <command> <subcommand> [flags]")
        self.assertIn("auth", commands)
        self.assertIn("repo", commands)
        self.assertIn("workflow", commands)
        self.assertIn("co", commands)
        self.assertNotIn("actions", commands, "help topics should not be command candidates")
        self.assertEqual(commands["auth"].section, "CORE COMMANDS")
        self.assertEqual(commands["auth"].source, "section_table")

    def test_docker_fixed_width_sections(self) -> None:
        parsed = parse_fixture("example-docker.txt")
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertEqual(parsed.usage, "Usage:  docker [OPTIONS] COMMAND")
        self.assertIn("run", commands)
        self.assertIn("compose", commands)
        self.assertIn("container", commands)
        self.assertIn("swarm", commands)
        self.assertIn("attach", commands)
        self.assertNotIn("config string", commands)
        self.assertEqual(commands["compose"].description, "Docker Compose")
        self.assertEqual(commands["compose"].section, "Management Commands")

    def test_npm_comma_inventory(self) -> None:
        parsed = parse_fixture("example-npm.txt")
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertIn("install", commands)
        self.assertIn("install-ci-test", commands)
        self.assertIn("help-search", commands)
        self.assertIn("whoami", commands)
        self.assertEqual(commands["install"].section, "All commands")
        self.assertEqual(commands["install"].source, "comma_inventory")

    def test_gog_multiline_blocks(self) -> None:
        parsed = parse_fixture("example-gog.txt")
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertEqual(parsed.usage, "Usage: gog <command> [flags]")
        self.assertIn("send", commands)
        self.assertIn("drive", commands)
        self.assertIn("schema", commands)
        self.assertIn("completion", commands)
        self.assertNotIn("Send", commands)
        self.assertNotIn("Google", commands)
        self.assertEqual(commands["drive"].aliases, ("drv",))
        self.assertTrue(commands["drive"].subcommand_signal)
        self.assertEqual(commands["schema"].aliases, ("help-json", "helpjson"))
        self.assertEqual(commands["send"].description, "Send an email (alias for 'gmail send')")

    def test_git_common_command_groups(self) -> None:
        parsed = parse_help(
            """
usage: git <command> [<args>]

These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone      Clone a repository into a new directory
   init       Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add        Add file contents to the index
   restore    Restore working tree files

'git help -a' and 'git help -g' list available subcommands and some
"""
        )
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertIn("clone", commands)
        self.assertIn("restore", commands)
        self.assertEqual(commands["clone"].section, "start a working area (see also: git help tutorial)")
        self.assertEqual(commands["clone"].source, "git_common")

    def test_brew_usage_examples(self) -> None:
        parsed = parse_help(
            """
Example usage:
  brew search TEXT|/REGEX/
  brew info [FORMULA|CASK...]
  brew install FORMULA|CASK...

Further help:
  brew commands
  brew help [COMMAND]
"""
        )
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertIn("search", commands)
        self.assertIn("install", commands)
        self.assertIn("commands", commands)
        self.assertNotIn("help", commands)
        self.assertEqual(commands["search"].source, "brew_usage")

    def test_brew_usage_ignores_child_help_prose(self) -> None:
        parsed = parse_help(
            """
Usage: brew install [options] formula|cask [...]

Install a formula or cask.

Examples:
  You can run brew test formula after installing.
"""
        )

        self.assertEqual(parsed.candidates, [])

    def test_command_section_stops_before_options(self) -> None:
        parsed = parse_help(
            """
Usage: uv [OPTIONS] <COMMAND>

Commands:
  auth     Manage authentication
  run      Run a command or script

Global options:
  -q, --quiet
          Use quiet output
      --color <COLOR_CHOICE>
          Control color
"""
        )
        commands = {candidate.name: candidate for candidate in parsed.candidates}

        self.assertIn("auth", commands)
        self.assertIn("run", commands)
        self.assertNotIn("Use", commands)
        self.assertNotIn("Control", commands)

    def test_options_are_extracted_as_canonical_flags(self) -> None:
        parsed = parse_help(
            """
tool 1.2.3

Usage: td task view [options] [ref]

View task details

Options:
  --json      Output as JSON
  --full      Include all fields in output
  --raw       Disable markdown rendering
  -h, --help  display help for command
"""
        )

        self.assertEqual(parsed.header, "tool 1.2.3")
        self.assertEqual(parsed.flags, ["--json", "--full", "--raw"])

    def test_long_option_alias_is_preferred_over_short_alias(self) -> None:
        parsed = parse_help(
            """
Usage: tool [options]

Options:
  -v, --verbose  Use verbose output
  -q             Suppress output
"""
        )

        self.assertEqual(parsed.flags, ["--verbose", "-q"])


if __name__ == "__main__":
    unittest.main()
