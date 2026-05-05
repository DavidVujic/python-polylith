---
name: polylith-base-creation
description: Create a Polylith base with `poly create base` — the entry point of a deployable application (HTTP API, CLI, message-queue consumer, AWS Lambda handler, GCP Cloud Function, scheduled job). Use when the user wants to add a service, API, endpoint, handler, or any new entry point to a Polylith workspace.
---

# Base Creation Skill

> 💡 **Terminology:** this skill uses Polylith terms like *brick*, *base*, *namespace*, and *theme*. If they're unfamiliar, load `polylith-concepts` first.

## Quick command

```bash
uv run poly create base --name api
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> A **base** is the entry point of a deployable application. For non-entry-point reusable code (business logic, capabilities), use `polylith-component-creation` instead.

## Command reference

| Option          | Required | Default | Description                                |
|-----------------|----------|---------|--------------------------------------------|
| `--name`        | yes      | —       | Name of the base (also the package name).  |
| `--description` | no       | `""`    | Optional human-readable description.       |

## What gets created (loose theme)

```
bases/<namespace>/api/
├── __init__.py     # Public interface — empty; add re-exports here
└── core.py         # Implementation — empty; user fills it in
```

If `[tool.polylith.test].enabled = true` in `workspace.toml`, the CLI also creates `test/bases/<namespace>/api/test_core.py`.

For the `tdd` theme layout (`bases/api/{src,test}/<namespace>/api/...`), load the `polylith-workspace-setup` skill.

## Examples

```bash
# Minimal
uv run poly create base --name api

# With description
uv run poly create base --name consumer --description "Kafka order consumer"
```

## Notes for the agent
- `core.py` is **empty boilerplate** — there is no FastAPI/Typer/Lambda scaffolding. Fill it in manually after creation if asked.
- `__init__.py` is also empty. By Polylith convention it should re-export the brick's public symbols, so consumers import `from <namespace>.api import …` rather than reaching into `core.py`.
- A new base is **not** wired into any project. To wire it: load `polylith-sync` and run `poly sync`, or run `poly create project` (the interactive prompt will offer to attach the base).
- The same command works for both `loose` and `tdd` themes — the CLI reads `[tool.polylith.structure].theme` from `workspace.toml`.

## Verification
After creation, verify the base exists using your file tools (e.g., check `bases/<namespace>/<name>/__init__.py`). Then, you will likely need to populate `core.py` and `__init__.py` using your file writing tools since they are created empty.
