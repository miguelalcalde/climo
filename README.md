# Climo

Generate Markdown, JSON, or Codex skill files for CLI command trees from
recursive help output.

Most CLI tools expose help one command at a time:

```sh
gh --help
gh auth --help
gh auth login --help
```

`climo` experiments with turning that scattered help output into one
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

This is an early package prepared for PyPI distribution. The public source repo
is `https://github.com/miguelalcalde/climo`.

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
- The CLI you want to inspect installed on `PATH`

No third-party Python dependencies are required.

## Install

Run without a persistent install:

```sh
uvx climo --help
```

Install the PyPI package as a uv tool:

```sh
uv tool install climo
```

Or install it with `pipx`:

```sh
pipx install climo
```

After installation, run:

```sh
climo --help
```

Until the first PyPI release is available, use the GitHub source URL:

```sh
uvx --from git+https://github.com/miguelalcalde/climo.git climo --help
uv tool install git+https://github.com/miguelalcalde/climo.git
pipx install git+https://github.com/miguelalcalde/climo.git
```

For local development from a checkout:

```sh
uv tool install --editable .
```

or run the module directly:

```sh
python3 -m climo --help
```

## Usage

Show the command help:

```sh
climo --help
```

Parse a captured help file:

```sh
climo parse example-gh.txt --format markdown
climo parse fixtures/cargo-root.txt --format json
```

Generate a tree from a live command:

```sh
climo generate gh --max-depth 3 --max-nodes 100 --format markdown --out out/gh.md
```

Generate with a debug manifest:

```sh
climo generate docker \
  --max-depth 2 \
  --max-nodes 100 \
  --format markdown \
  --out out/docker.md \
  --debug-out out/docker-debug.json
```

The debug manifest records accepted and rejected candidates, the argv used for
validation, return codes, timeouts, parser source, and rejection reason.

## Skill Output

The repo can also generate Codex-compatible skill files. A valid skill requires
a `SKILL.md` file with delimited YAML frontmatter, so `--skill` wraps the
generated Markdown tree with the required metadata. The required frontmatter
fields are `name` and `description`.

Generate the current Todoist CLI skill:

```sh
climo generate td \
  --out skills/td/SKILL.md \
  --skill \
  --name td \
  --description "A compact skill for Todoist CLI, use this when you want to find out how to use the CLI with simple examples"
```

This writes:

```text
skills/td/SKILL.md
```

The generated folder can be pulled into a Codex skills directory as a pure skill
tool. Use `npm run skills:td` to rebuild the checked-in Todoist skill.

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
climo generate gh \
  --max-depth 3 \
  --max-nodes 120 \
  --format markdown \
  --out out/gh-depth3.md \
  --debug-out out/gh-depth3-debug.json
```

Generate a Cargo tree:

```sh
climo generate cargo \
  --max-depth 1 \
  --format markdown \
  --out out/cargo-depth1.md
```

Generate PNPM documentation:

```sh
climo generate pnpm \
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
env PYTHONPYCACHEPREFIX=.pycache python3 -m compileall -q climo tests scripts
```

Validate generated skills:

```sh
python3 scripts/validate_skills.py
```

The fixture precision tests assert both:

- expected commands are extracted
- known non-command tokens are not extracted

That second point is important. For this project, avoiding hallucinated commands
from option lists and prose is as important as finding real subcommands.

## Contributing Skills

Skill contributions live under `skills/<name>/SKILL.md`. See
`CONTRIBUTING.md` for the PR checklist and the expected validation commands.

## Publishing

Releases are configured for PyPI Trusted Publishing through GitHub Actions. In
PyPI, create the `climo` project and add a trusted publisher with:

- owner: `miguelalcalde`
- repository: `climo`
- workflow: `publish.yml`
- environment: `pypi`

Then publish a release by pushing a version tag that matches the version in
`pyproject.toml`:

```sh
git tag v0.1.0
git push origin v0.1.0
```

After the release is on PyPI, one-shot execution works with:

```sh
uvx climo --help
```

## Output Formats

Markdown is intended for humans:

```sh
climo generate uv --format markdown --out out/uv.md
```

JSON is intended for downstream tooling:

```sh
climo generate uv --format json --out out/uv.json
```

Use `--include-raw` if you want raw help text embedded in the JSON tree.

## Profiles

Most CLIs work with the default help strategy:

```text
{command} --help
{command} -h
```

Some tools need custom help strategies. Profiles live in
`climo/profiles.py`. Current custom profiles include `npm`, `pnpm`, and
`openssl`.

## Adding Parser Coverage

The preferred workflow for a new CLI is:

1. Capture root help into `fixtures/<tool>-root.txt`.
2. Add include/exclude expectations in `tests/test_fixture_precision.py`.
3. Run the tests and inspect parser misses.
4. Add or tighten a parser under `climo/parsers/`.
5. Add a bounded live generation with `--debug-out` to check validation behavior.

Good next candidates include `vercel`, `go`, `curl`, `jq`, `ffmpeg`, and any
niche CLIs with unusual help layouts.

## Known Limits

- Validation is serial, so very large trees can take time.
- Some tools expose help topics rather than executable subcommands; the model
  does not yet distinguish all topic types.
- Parser precision depends on fixture coverage. Add fixtures before broadening
  parser heuristics.
- Generated skills should be reviewed before PR. If output looks wrong, add
  fixture coverage and fix the parser rather than hand-editing large trees.

## License

MIT
