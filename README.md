# Help Tree

Generate Markdown or JSON documentation for CLI command trees by crawling help
output recursively.

Most CLI tools expose help one command at a time:

```sh
gh --help
gh auth --help
gh auth login --help
```

`help-tree` experiments with turning that scattered help output into one
structured artifact:

```text
gh
├── auth
│   ├── login
│   ├── logout
│   └── status
├── repo
└── pr
```

The goal is precision first: parse command candidates from inconsistent help
formats, validate candidates by invoking child help, and render a deterministic
document.

## Status

This is an early local experiment. It is not packaged yet; run it directly with
Python from this repository.

Current parser coverage includes:

- section tables used by tools like `gh`, `docker`, `kubectl`, `pip`, `cargo`,
  and `uv`
- comma inventories like `npm`
- multiline command blocks like `gog`
- Git's grouped common-command help
- Homebrew's terse example-style root help
- PNPM's category-based root help
- OpenSSL's columnar command inventory

The project also keeps negative fixtures for tools that mostly expose options
instead of subcommands, such as `python3`, `rg`, `ssh`, `tar`, and `rsync`.

## Requirements

- Python 3
- The CLI you want to crawl installed on `PATH`

No third-party Python dependencies are required.

## Usage

Show the local command help:

```sh
python3 -m help_tree --help
```

Parse a captured help file:

```sh
python3 -m help_tree parse example-gh.txt --format markdown
python3 -m help_tree parse fixtures/cargo-root.txt --format json
```

Crawl a live command:

```sh
python3 -m help_tree crawl gh --max-depth 3 --max-nodes 100 --format markdown --out out/gh.md
```

Crawl with a debug manifest:

```sh
python3 -m help_tree crawl docker \
  --max-depth 2 \
  --max-nodes 100 \
  --format markdown \
  --out out/docker.md \
  --debug-out out/docker-debug.json
```

The debug manifest records accepted and rejected candidates, the argv used for
validation, return codes, timeouts, parser source, and rejection reason.

## How It Works

The crawler is intentionally validation-driven.

1. Run help for the current command path.
2. Normalize ANSI and whitespace.
3. Extract candidate subcommands using multiple parser families.
4. Validate every candidate by invoking its child help.
5. Recurse into validated children until the depth or node limit is reached.
6. Render Markdown or JSON.

This means parsers can be broad, while validation prevents many false positives
from entering the final tree.

## Examples

Generate a GitHub CLI tree:

```sh
python3 -m help_tree crawl gh \
  --max-depth 3 \
  --max-nodes 120 \
  --format markdown \
  --out out/gh-depth3.md \
  --debug-out out/gh-depth3-debug.json
```

Generate a Cargo tree:

```sh
python3 -m help_tree crawl cargo \
  --max-depth 1 \
  --format markdown \
  --out out/cargo-depth1.md
```

Generate PNPM documentation:

```sh
python3 -m help_tree crawl pnpm \
  --max-depth 1 \
  --format markdown \
  --out out/pnpm-depth1.md \
  --debug-out out/pnpm-depth1-debug.json
```

## Fixtures

Fixtures are captured help outputs used to test parser precision without relying
on live commands during every test run.

Capture the currently configured fixtures:

```sh
python3 scripts/capture_fixtures.py
```

This writes files under `fixtures/` and updates `fixtures/manifest.json`.

Current fixture corpus:

- `cargo-root.txt`
- `openssl-root.txt`
- `pip3-root.txt`
- `pnpm-root.txt`
- `python3-root.txt`
- `rg-root.txt`
- `rsync-root.txt`
- `ssh-root.txt`
- `tar-root.txt`

## Validation

Run the parser and fixture precision tests:

```sh
python3 -m unittest discover -v
```

Run a syntax check without writing bytecode outside the repo:

```sh
env PYTHONPYCACHEPREFIX=.pycache python3 -m compileall -q help_tree tests scripts
```

The fixture precision tests assert both:

- expected commands are extracted
- known non-command tokens are not extracted

That second point is important. For this project, avoiding hallucinated commands
from option lists and prose is as important as finding real subcommands.

## Output Formats

Markdown is intended for humans:

```sh
python3 -m help_tree crawl uv --format markdown --out out/uv.md
```

JSON is intended for downstream tooling:

```sh
python3 -m help_tree crawl uv --format json --out out/uv.json
```

Use `--include-raw` if you want raw help text embedded in the JSON tree.

## Profiles

Most CLIs work with the default help strategy:

```text
{command} --help
{command} -h
```

Some tools need custom help strategies. Profiles live in
`help_tree/profiles.py`. Current custom profiles include `npm`, `pnpm`, and
`openssl`.

## Adding Parser Coverage

The preferred workflow for a new CLI is:

1. Capture root help into `fixtures/<tool>-root.txt`.
2. Add include/exclude expectations in `tests/test_fixture_precision.py`.
3. Run the tests and inspect parser misses.
4. Add or tighten a parser under `help_tree/parsers/`.
5. Add a bounded live crawl with `--debug-out` to check validation behavior.

Good next candidates include `vercel`, `go`, `curl`, `jq`, `ffmpeg`, and any
niche CLIs with unusual help layouts.

## Known Limits

- There is no package metadata or installable console script yet.
- Validation is serial, so very large trees can take time.
- Some tools expose help topics rather than executable subcommands; the model
  does not yet distinguish all topic types.
- Parser precision depends on fixture coverage. Add fixtures before broadening
  parser heuristics.

