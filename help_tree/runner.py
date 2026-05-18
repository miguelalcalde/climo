"""Safe command execution for help crawling."""

from __future__ import annotations

import os
import shlex
import subprocess
import time
from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
    duration_seconds: float = 0.0

    @property
    def output(self) -> str:
        return "\n".join(part for part in (self.stdout, self.stderr) if part)


class CommandRunner:
    def __init__(self, timeout_seconds: float = 3.0) -> None:
        self.timeout_seconds = timeout_seconds

    def run(self, argv: list[str]) -> CommandResult:
        started_at = time.monotonic()
        env = os.environ.copy()
        env.update(
            {
                "CLICOLOR": "0",
                "CLICOLOR_FORCE": "0",
                "NO_COLOR": "1",
                "TERM": "dumb",
                "PAGER": "cat",
                "GIT_PAGER": "cat",
            }
        )
        try:
            completed = subprocess.run(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=self.timeout_seconds,
                env=env,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            duration = time.monotonic() - started_at
            return CommandResult(
                argv=argv,
                returncode=124,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
                timed_out=True,
                duration_seconds=duration,
            )
        except OSError as exc:
            duration = time.monotonic() - started_at
            return CommandResult(
                argv=argv,
                returncode=127,
                stdout="",
                stderr=str(exc),
                duration_seconds=duration,
            )

        duration = time.monotonic() - started_at
        return CommandResult(
            argv=argv,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            duration_seconds=duration,
        )


def split_command(command: str) -> list[str]:
    return shlex.split(command)
