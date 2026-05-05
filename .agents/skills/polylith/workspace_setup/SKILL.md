---
name: polylith-workspace-setup
description: Scaffold a new Polylith workspace with `poly create workspace`. Use when the user wants to initialize / set up / start / bootstrap Polylith from scratch in a directory (creates `workspace.toml` and the `bases/`, `components/`, `projects/`, `development/` directories).
---

# Workspace Setup Skill

> 💡 **Terminology:** this skill uses Polylith terms like *namespace*, *brick*, *theme*, and *development project*. If they're unfamiliar, load `polylith-concepts` first.

## Quick command

```bash
uv run poly create workspace --name mycompany --theme loose
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> ⚠ **Always pass `--theme loose`.** The CLI default is `tdd`; loose is the recommended layout used by `python-polylith` itself and almost every public example.
> ⚠ **`--name` sets the namespace**, not just a workspace label — it becomes the top-level Python package for every brick.
> ⚠ **`pyproject.toml` is NOT created.** Polylith layers on top of an existing Python project. The user must create the root `pyproject.toml` separately (`uv init`, `poetry init`, etc.).

## Command reference

| Option     | Required | Default | Description                                                |
|------------|----------|---------|------------------------------------------------------------|
| `--name`   | yes      | —       | The **namespace** for all bricks (e.g. `mycompany`).       |
| `--theme`  | no       | `tdd`   | Brick directory layout: `loose` (recommended) or `tdd`.    |

## What gets created

```
<cwd>/
├── workspace.toml      # Polylith config (generated, see below)
├── README.md           # Workspace README (generated)
├── bases/              # Empty; populate with `poly create base`
├── components/         # Empty; populate with `poly create component`
├── projects/           # Empty; populate with `poly create project`
└── development/        # Scratch space for REPL/notebooks
    └── __init__.py
```

The CLI does **not** create: `pyproject.toml`, lock files, or any brick subdirectories.

### Generated `workspace.toml`

```toml
[tool.polylith]
namespace = "mycompany"
git_tag_pattern = "stable-*"

[tool.polylith.structure]
theme = "loose"

[tool.polylith.tag.patterns]
stable = "stable-*"
release = "v[0-9]*"

[tool.polylith.resources]
brick_docs_enabled = false

[tool.polylith.test]
enabled = true
```

### Optional advanced config (added by hand)

```toml
# Short aliases for verbose project names — used in `poly info` / `poly deps` tables.
[tool.polylith.projects.alias]
my-very-long-project-name = "api"

# Group projects for filtered views: `poly info --group hooks`.
[tool.polylith.projects.groups]
hooks = ["project-a", "project-c"]

# Library aliases when import name ≠ package name (NOTE: `libs.alias`, not `projects.alias`).
[tool.polylith.libs.alias]
cv2 = "opencv-python"
```

> Polylith has **two `alias` tables**: `projects.alias` (display names for projects) and `libs.alias` (third-party library import-name → package-name).

## Themes

`[tool.polylith.structure].theme` controls only the on-disk layout of bricks.

### `loose` (recommended)
Flat directories: `<bricks_dir>/<namespace>/<brick>/{__init__.py,core.py}`. Tests live at `test/<bricks_dir>/<namespace>/<brick>/test_<modulename>.py`.

```
components/mycompany/greeting/{__init__.py,core.py}
test/components/mycompany/greeting/test_core.py
```

### `tdd`
Each brick is its own distributable with sibling `src/` and `test/`: `<bricks_dir>/<brick>/src/<namespace>/<brick>/...` and `<bricks_dir>/<brick>/test/<namespace>/<brick>/...`. Useful when bricks ship as standalone packages.

## After setup
1. Create the root `pyproject.toml` if it doesn't exist (with the user's chosen package manager).
2. Add `polylith-cli` and the matching build hook (`hatch-polylith-bricks`, `pdm-polylith-bricks`) as dev dependencies.
3. Load `polylith-base-creation` / `polylith-component-creation` to start adding bricks.

## Verification
After setup, check that `workspace.toml` and the top-level directories (`bases/`, `components/`, `projects/`, `development/`) were created. Since `poly create workspace` does not create a `pyproject.toml`, verify if the root `pyproject.toml` exists and create/initialize it if missing.
