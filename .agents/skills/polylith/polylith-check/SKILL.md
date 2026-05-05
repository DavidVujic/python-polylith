---
name: polylith-check
description: Validate a Polylith workspace with `poly check` — the canonical CI gate. Verifies brick imports against project `pyproject.toml`s, third-party library declarations vs. the lock file, and (under `--strict`) cross-project version consistency. Exits 1 on failure. Use when the user wants to lint, validate, verify, or CI-gate a Polylith workspace.
---

# Check Skill

## Quick command

```bash
uv run poly check
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> ⚠ **Run `poly sync` first** if bricks have been added/removed since the last commit, otherwise sync-related findings will dominate the report. Load `polylith-sync` if needed.
> ⚠ **Exit code 1 = failure** — this is the right command to wrap in CI.

## Typical CI usage

```bash
uv run poly sync --quiet                          # Make sure brick lists are current (--quiet avoids the interactive prompt)
uv run poly check                                 # Validate; build fails if non-zero

# (Optional) scope test runs to bricks whose implementation changed.
# `poly diff --bricks --short` emits a comma-separated list, which becomes a
# pytest `-k` expression (`log,message` → `pytest -k "log or message"`).
changes="$(uv run poly diff --bricks --short)"
[ -n "$changes" ] && uv run pytest -k "${changes//,/ or }"
```

> Use `poly diff` (implementation diff) for "run tests for what changed". Use `poly test diff --short` if you specifically want to scope on **test-code** changes — load `polylith-testing` for that variant. Both feed the same `pytest -k` recipe.

## What it verifies
- Every brick imported by another brick is listed in the consuming project's `[tool.polylith.bricks]`.
- Every third-party library imported by a project's bricks is declared in that project's `dependencies` and present in the lock file.

## Command reference

| Option         | Default | Description                                                                                             |
|----------------|---------|---------------------------------------------------------------------------------------------------------|
| `--strict`     | `false` | Stricter name/version matching across projects (catches version drift).                                 |
| `--verbose`    | `false` | Print extra context, including lock-file lookups.                                                       |
| `--quiet`      | `false` | Suppress output. Exit code unchanged.                                                                   |
| `--alias`      | —       | Comma-separated `import_name=package_name` aliases.                                                     |
| `--directory`  | cwd     | Limit the check to projects whose path matches this directory.                                          |

## Examples

```bash
# Standard CI gate
uv run poly check

# One project only
uv run poly check --directory projects/user_api
```

## Common failure modes & Auto-Fixes
1. **Missing Brick Error:** If the error says a brick imports another brick that isn't in `[tool.polylith.bricks]` → run `poly sync` (load `polylith-sync`).
2. **Missing Dependency Error:** If the error says a brick imports a third-party library not listed in the project's `dependencies` → load `polylith-dependency-management` and add the library to the project's `pyproject.toml`.
3. **Version Drift Error:** Under `--strict`, if versions of the same library diverge between projects → inspect `pyproject.toml` or load `polylith-libs` to find the drift, then align versions (or rely on a single root lock file).
