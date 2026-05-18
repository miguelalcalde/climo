"""Recursive help crawler."""

from __future__ import annotations

import shlex
from dataclasses import dataclass, field
from typing import Any

from help_tree.ansi import normalize_help
from help_tree.models import CommandCandidate, CommandNode
from help_tree.parsers import parse_help
from help_tree.profiles import Profile, profile_for
from help_tree.runner import CommandResult, CommandRunner, split_command


HELP_MARKERS = ("usage", "commands", "options", "flags", "help")
UNKNOWN_MARKERS = (
    "unknown command",
    "unknown subcommand",
    "not a command",
    "invalid command",
    "command not found",
)


@dataclass
class CrawlOptions:
    max_depth: int = 3
    max_nodes: int = 250
    timeout_seconds: float = 3.0
    include_raw: bool = False


@dataclass
class CrawlState:
    visited: set[str] = field(default_factory=set)
    node_count: int = 0
    events: list[dict[str, Any]] = field(default_factory=list)


class HelpCrawler:
    def __init__(self, options: CrawlOptions | None = None, runner: CommandRunner | None = None) -> None:
        self.options = options or CrawlOptions()
        self.runner = runner or CommandRunner(timeout_seconds=self.options.timeout_seconds)
        self.debug_events: list[dict[str, Any]] = []
        self._help_cache: dict[tuple[str, ...], CommandResult] = {}

    def crawl(self, root_command: str) -> CommandNode:
        profile = profile_for(root_command)
        state = CrawlState()
        self._help_cache = {}
        node = self._crawl_path(split_command(root_command), profile, state, depth=0, parent_output="")
        self.debug_events = state.events
        return node

    def _crawl_path(
        self,
        path: list[str],
        profile: Profile,
        state: CrawlState,
        depth: int,
        parent_output: str,
    ) -> CommandNode:
        command = " ".join(path)
        state.visited.add(command)
        state.node_count += 1

        result = self._run_help(path, profile)
        output = normalize_help(result.output)
        parsed = parse_help(output)
        node = CommandNode(
            path=path,
            header=parsed.header,
            usage=parsed.usage,
            description=parsed.description,
            candidates=parsed.candidates,
            flags=parsed.flags,
            raw_help=output if self.options.include_raw else "",
            validation=self._validation_metadata(result, output, parent_output),
        )

        if depth >= self.options.max_depth or state.node_count >= self.options.max_nodes:
            return node

        for candidate in parsed.candidates:
            if state.node_count >= self.options.max_nodes:
                break
            child_path = path + [candidate.name]
            child_command = " ".join(child_path)
            if child_command in state.visited:
                state.events.append(self._candidate_event(command, candidate, [], "rejected", "already visited"))
                continue
            if not self._candidate_name_is_safe(candidate):
                state.events.append(self._candidate_event(command, candidate, [], "rejected", "unsafe candidate name"))
                continue
            child_result = self._run_help(child_path, profile)
            child_output = normalize_help(child_result.output)
            rejection_reason = self._child_rejection_reason(child_result, child_output, output)
            if rejection_reason:
                state.events.append(
                    self._candidate_event(
                        command,
                        candidate,
                        child_result.argv,
                        "rejected",
                        rejection_reason,
                        child_result,
                    )
                )
                continue
            state.events.append(
                self._candidate_event(command, candidate, child_result.argv, "accepted", "", child_result)
            )
            child = self._crawl_path(child_path, profile, state, depth + 1, output)
            node.children.append(child)

        return node

    def _run_help(self, path: list[str], profile: Profile) -> CommandResult:
        cache_key = tuple(path)
        if cache_key in self._help_cache:
            return self._help_cache[cache_key]
        command = " ".join(shlex.quote(part) for part in path)
        path_without_root = " ".join(shlex.quote(part) for part in path[1:])
        for template in profile.help_templates:
            rendered = template.format(command=command, path=path_without_root)
            argv = split_command(rendered)
            result = self.runner.run(argv)
            output = normalize_help(result.output)
            if self._looks_like_help(output) and not self._looks_unknown(output):
                self._help_cache[cache_key] = result
                return result
        self._help_cache[cache_key] = result
        return result

    def _validation_metadata(self, result: CommandResult, output: str, parent_output: str) -> dict[str, object]:
        return {
            "argv": result.argv,
            "returncode": result.returncode,
            "timed_out": result.timed_out,
            "duration_seconds": round(result.duration_seconds, 4),
            "looks_like_help": self._looks_like_help(output),
            "same_as_parent": bool(parent_output and output == parent_output),
        }

    def _child_rejection_reason(self, result: CommandResult, output: str, parent_output: str) -> str:
        if result.timed_out or not output.strip():
            return "timed out" if result.timed_out else "empty output"
        if self._looks_unknown(output):
            return "unknown command output"
        if parent_output and output == parent_output:
            return "same output as parent"
        if not self._looks_like_help(output):
            return "output does not look like help"
        return ""

    def _looks_like_help(self, output: str) -> bool:
        lowered = output.lower()
        return any(marker in lowered for marker in HELP_MARKERS)

    def _looks_unknown(self, output: str) -> bool:
        lowered = output.lower()
        if "standard commands" in lowered and "cipher commands" in lowered:
            return False
        return any(marker in lowered for marker in UNKNOWN_MARKERS)

    def _candidate_name_is_safe(self, candidate: CommandCandidate) -> bool:
        name = candidate.name
        return bool(name) and not name.startswith("-") and "/" not in name and "\x00" not in name

    def _candidate_event(
        self,
        parent_command: str,
        candidate: CommandCandidate,
        argv: list[str],
        status: str,
        reason: str,
        result: CommandResult | None = None,
    ) -> dict[str, Any]:
        return {
            "parent": parent_command,
            "candidate": candidate.name,
            "child": f"{parent_command} {candidate.name}",
            "status": status,
            "reason": reason,
            "argv": argv,
            "returncode": result.returncode if result else None,
            "timed_out": result.timed_out if result else False,
            "duration_seconds": round(result.duration_seconds, 4) if result else 0.0,
            "source": candidate.source,
            "section": candidate.section,
        }
