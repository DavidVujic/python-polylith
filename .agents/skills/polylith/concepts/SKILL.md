---
name: polylith-concepts
description: Provides foundational knowledge about Polylith architecture, including the glossary (bases, components, projects, workspaces), theme layouts, and package manager mapping. Use this when you need to understand Polylith terminology or how the repository is structured conceptually before taking action.
---

# Polylith Concepts & Glossary

## Glossary

### Bricks
The fundamental units of code in Polylith — **components** and **bases**. Bricks are reusable, isolated, and organized under a single **namespace**.

### Components
Reusable, isolated bricks that implement business logic or capabilities. Components are consumed by bases and by other components, never the other way around.

### Bases
Bricks that serve as the **entry point** of a deployable application — for example HTTP APIs, CLIs, message-queue consumers, AWS Lambda handlers, GCP Cloud Functions, or scheduled jobs. A base wires together components and exposes the application to its runtime.

### Namespace
The top-level Python package name under which all bricks live (e.g. `mycompany`). Defined once in `[tool.polylith].namespace` in `workspace.toml`; shared by every brick.

### Workspace
The root directory of a Polylith repository. Contains `workspace.toml`, the root `pyproject.toml` (which **is** the development project), the `bases/`, `components/`, `projects/`, and `development/` directories, and a single shared lock file.

### Projects
Lightweight `pyproject.toml` configurations under `projects/<name>/` that **reference bricks** to produce deployable artifacts (Docker images, wheels, Lambda packages). Projects contain no Python source code of their own.

### Development Project
The root `pyproject.toml` itself — a single, unified Python environment that includes **every** brick and **every** dependency (production and dev). Used for local development, REPL sessions, and notebooks under `development/`.

### Dependencies
- The **development project** (root `pyproject.toml`) holds **all** dependencies, including dev-only ones.
- Each **project** under `projects/` holds only its **production** dependencies.
- With **uv workspaces**, individual projects don't need to pin third-party versions — the root `pyproject.toml` and the shared lock file pin versions centrally.

## Package & Dependency Management mapping

The `poly` CLI is package-manager-agnostic — only the **command prefix** changes. Each SKILL.md repeats the prefix detection rule inline so the agent doesn't need this README to act. The full table:

| Tool                          | Detection signal                                                       | Command prefix    |
|-------------------------------|------------------------------------------------------------------------|-------------------|
| **uv** (recommended)          | `uv.lock` present, or `[tool.uv]` in `pyproject.toml`                  | `uv run poly …`   |
| **Poetry**                    | `[tool.poetry]` in `pyproject.toml`, `poetry.lock`                     | `poetry poly …` (via `poetry-polylith-plugin`) |
| **PDM**                       | `[tool.pdm]` in `pyproject.toml`, `pdm.lock`                           | `pdm run poly …`  |
| **Hatch**                     | `[tool.hatch]` in `pyproject.toml`                                     | `hatch run poly …`|
| **Rye**                       | `requirements.lock` + `[tool.rye]`                                     | `rye run poly …`  |
| **Activated virtualenv**      | `$VIRTUAL_ENV` set, or none of the above                               | `poly …`          |

If multiple signals are present, prefer the lock file that exists, then `[tool.<x>]` markers, then plain `poly`.

## Themes

`[tool.polylith.structure].theme` controls the on-disk brick layout:

- **`loose`** (recommended) — flat `<bricks_dir>/<namespace>/<brick>/` directories with tests in a top-level `test/` folder. Used by `python-polylith` itself and by most public examples.
- **`tdd`** — each brick is its own directory with `src/` and `test/` siblings.

> The CLI default for `poly create workspace --theme` is **`tdd`**. Always pass `--theme loose` explicitly when loose is wanted.
