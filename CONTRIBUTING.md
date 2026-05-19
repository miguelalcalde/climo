# Contributing

Climo turns CLI help output into deterministic Markdown, JSON, and Codex
skill files. Contributions are welcome in two forms:

- generated skills under `skills/<name>/SKILL.md`
- parser and fixture improvements that make generated trees more accurate

## Local Setup

Run the tool from a checkout:

```sh
python3 -m climo --help
```

Or install it locally:

```sh
uv tool install --editable .
```

## Generate a Skill

Use `generate --skill` with the required skill frontmatter fields:

```sh
climo generate td \
  --out skills/td/SKILL.md \
  --skill \
  --name td \
  --description "A compact skill for Todoist CLI, use this when you want to find out how to use the CLI with simple examples"
```

The output file must live at:

```text
skills/<name>/SKILL.md
```

Review generated skills before opening a PR. CLI help varies a lot, and a
generated tree may expose parser misses, truncated descriptions, or false
positives that should be fixed with fixture coverage.

## Add Parser Coverage

When generation is wrong for a CLI:

1. Capture root help into `fixtures/<tool>-root.txt`.
2. Add include and exclude expectations in `tests/test_fixture_precision.py`.
3. Run the tests.
4. Tighten or add a parser under `climo/parsers/`.
5. Run a bounded live generation with `--debug-out` and inspect rejections.

## Validate

Run this before opening a PR:

```sh
python3 -m unittest discover -v
python3 -m compileall -q climo tests scripts
python3 scripts/validate_skills.py
```

## Skill PR Checklist

- The skill lives at `skills/<name>/SKILL.md`.
- The file has YAML frontmatter with `name` and `description`.
- The body contains a useful command tree.
- The generation command is included in the PR description.
- Tests and skill validation pass.
- Parser changes include fixture expectations when behavior changes.
