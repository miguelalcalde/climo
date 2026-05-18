from __future__ import annotations

import subprocess
import unittest
from unittest.mock import patch

from help_tree.runner import CommandResult, CommandRunner, split_command


class CommandRunnerTests(unittest.TestCase):
    def test_command_result_output_joins_stdout_and_stderr(self) -> None:
        result = CommandResult(argv=["tool"], returncode=1, stdout="out", stderr="err")

        self.assertEqual(result.output, "out\nerr")

    def test_run_returns_completed_process_output(self) -> None:
        completed = subprocess.CompletedProcess(["tool"], 0, stdout="out", stderr="err")

        with patch("help_tree.runner.subprocess.run", return_value=completed) as run:
            result = CommandRunner(timeout_seconds=1.5).run(["tool", "--help"])

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.output, "out\nerr")
        kwargs = run.call_args.kwargs
        self.assertEqual(kwargs["timeout"], 1.5)
        self.assertEqual(kwargs["env"]["NO_COLOR"], "1")
        self.assertEqual(kwargs["env"]["PAGER"], "cat")

    def test_run_reports_timeout(self) -> None:
        timeout = subprocess.TimeoutExpired(["tool"], 0.01, output="partial", stderr="late")

        with patch("help_tree.runner.subprocess.run", side_effect=timeout):
            result = CommandRunner(timeout_seconds=0.01).run(["tool"])

        self.assertEqual(result.returncode, 124)
        self.assertTrue(result.timed_out)
        self.assertEqual(result.output, "partial\nlate")

    def test_split_command_uses_shell_quoting_rules(self) -> None:
        self.assertEqual(split_command("tool 'two words' --flag"), ["tool", "two words", "--flag"])


if __name__ == "__main__":
    unittest.main()
