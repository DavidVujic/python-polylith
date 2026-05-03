---
name: polylith-diff
description: List Polylith bricks whose **implementation** changed since a git tag using `poly diff`. Use for release notes, selective deploys ("which projects need rebuilding?"), and PR scope review. For TEST-code diffs, use `polylith-testing` instead.
---

# Diff Skill

## Quick command

```bash
# Human-readable (default)
uv run poly diff

# Pipe-friendly: comma-separated list of changed bricks (use this in scripts)
uv run poly diff --bricks --short
```

> **Agent rule of thumb:** when the goal is to *do something* with the result (run pytest, drive a deploy script, render a list), reach for `--bricks --short` first. The default output is for human readers.

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> **`poly diff` vs `poly test diff`:**
> - `poly diff` → brick **implementation** changes since a tag (drives releases/deploys).
> - `poly test diff` → **test-code** changes since a tag (drives selective test runs). Load `polylith-testing`.

## Tag selection
- Default: latest git tag matching `[tool.polylith.tag.patterns].stable` from `workspace.toml` (e.g. `stable-*`).
- `--since <ref>` — pin a specific tag, branch, or commit-ish. The CLI tries to resolve `<ref>` as a configured pattern key first, then falls through to using it literally with `git diff <ref>`.

## Command reference

| Option       | Default             | Description                                                                                                |
|--------------|---------------------|------------------------------------------------------------------------------------------------------------|
| `--since`    | latest matching tag | Reference tag (or branch/commit) to diff against.                                                          |
| `--short`    | `false`             | Compact output. Combined with `--bricks`, emits a comma-separated list of brick names — pipe-friendly.     |
| `--bricks`   | `false`             | Print the list of bricks that changed (human-readable on its own; CSV when paired with `--short`).         |
| `--deps`     | `false`             | With `--bricks`, also print bricks that **depend on** the changed bricks (transitive impact).              |

## Examples

```bash
# Default: against latest stable-* tag
uv run poly diff

# Selective deploy: every brick changed (incl. transitive consumers) since a release tag
uv run poly diff --since stable-4 --bricks --deps

# Pipe-friendly: comma-separated names of bricks changed vs. main
uv run poly diff --since main --bricks --short
```

## Running tests for changed bricks

The established Polylith pattern is to feed `--bricks --short` straight into `pytest -k`: brick names become an `or`-expression that pytest matches against test IDs, so the agent doesn't need to resolve namespace / theme / base-vs-component.

```bash
changes="$(uv run poly diff --bricks --short)"
[ -n "$changes" ] && uv run pytest -k "${changes//,/ or }"
```

Example: `--bricks --short` outputs `log,message` → pytest runs as `pytest -k "log or message"`, collecting every test whose ID contains `log` or `message` (matches `test/components/<ns>/log/...` and `test/bases/<ns>/log/...` alike).

> ⚠ `pytest -k` does **substring** matching, so a brick named `log` will also match tests whose name contains `log` (e.g. an unrelated `logger` brick or a `test_login` function). For short/generic brick names, fall back to passing explicit test directories.

## Notes for the agent
- Operates on git's view of the working tree — uncommitted changes since the tag count as changed.
- If no matching tag exists and `--since` isn't passed, the command prints `No matching tags or commits found in repository.` and exits 0. Guard scripts so they don't run `pytest -k ""` (which would collect nothing or, worse, every test depending on the version).
- Map changed bricks → projects with `poly info` (load `polylith-workspace-inspection`) to drive selective deploys.
