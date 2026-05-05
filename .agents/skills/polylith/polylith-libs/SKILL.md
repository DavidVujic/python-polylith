---
name: polylith-libs
description: Inspect third-party libraries used per Polylith project with `poly libs`. Use when the user wants to see dependency usage, audit version drift across projects, find which projects use a given library, or compare library declarations vs. the lock file. Read-only — for a CI gate use `polylith-check` instead.
---

# Libs Skill

## Quick command

```bash
uv run poly libs
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> `poly libs` **reports**; `poly check` **fails the build**. Use `libs` for inspection, `check` for CI (load `polylith-check`).

## Prerequisites
- A Polylith workspace with at least one project.
- A lock file at the root (`uv.lock`, `poetry.lock`, or `pdm.lock`).

## Command reference

| Option         | Default | Description                                                                                            |
|----------------|---------|--------------------------------------------------------------------------------------------------------|
| `--strict`     | `false` | Stricter matching of names and versions across projects.                                               |
| `--directory`  | cwd     | Limit output to projects whose path matches this directory.                                            |
| `--alias`      | —       | Comma-separated `import_name=package_name` aliases.                                                    |
| `--short`      | `false` | Compact view — useful for wide workspaces.                                                             |
| `--save`       | `false` | Persist the report to a file under the workspace's output dir.                                         |

## Examples

```bash
# Full library × project matrix
uv run poly libs

# Strict version-drift detection
uv run poly libs --strict

# Compact view for many projects
uv run poly libs --short
```

## How to read it
- Rows are third-party libraries; columns are projects.
- `✔` = the library is used by that project.
- A library used by multiple projects with **different versions** = version drift. Fix by aligning versions in the relevant project `pyproject.toml`s, or by relying on a central lock file (uv workspaces).

## Notes for the agent
- `poly libs` is **read-only** — it never modifies `pyproject.toml` or the lock file.
