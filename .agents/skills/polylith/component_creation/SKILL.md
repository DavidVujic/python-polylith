---
name: polylith-component-creation
description: Create a Polylith component with `poly create component` — a reusable, isolated brick implementing business logic, a feature, a domain module, or a capability. Use when adding non-entry-point code that bases or other components will import.
---

# Component Creation Skill

> 💡 **Terminology:** this skill uses Polylith terms like *brick*, *component*, *namespace*, and *theme*. If they're unfamiliar, load `polylith-concepts` first.

## Quick command

```bash
uv run poly create component --name user_service
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> A **component** is reusable, non-entry-point code (business logic, domain features, capabilities). For entry points (HTTP API, CLI, Lambda handler), use `polylith-base-creation` instead.

## Command reference

| Option          | Required | Default | Description                                       |
|-----------------|----------|---------|---------------------------------------------------|
| `--name`        | yes      | —       | Name of the component (also the package name).    |
| `--description` | no       | `""`    | Optional human-readable description.              |

## What gets created (loose theme)

```
components/<namespace>/user_service/
├── __init__.py     # Public interface — empty; add re-exports here
└── core.py         # Implementation — empty; user fills it in
```

If `[tool.polylith.test].enabled = true` in `workspace.toml`, the CLI also creates `test/components/<namespace>/user_service/test_core.py`.

For the `tdd` theme layout (`components/user_service/{src,test}/<namespace>/user_service/...`), load `polylith-workspace-setup`.

## Examples

```bash
# Minimal
uv run poly create component --name user_service

# With description
uv run poly create component --name greeting --description "Greeting domain"
```

## Notes for the agent
- Both `core.py` and `__init__.py` are **empty boilerplate**. The component is not "ready" — the user fills in `core.py`, then re-exports its public API from `__init__.py`:
  ```python
  # components/<namespace>/user_service/__init__.py
  from <namespace>.user_service.core import create_user, get_user
  ```
- Consumers import via the public interface (`from <namespace>.user_service import create_user`), never via `core.py` directly. `poly deps --interface` (load `polylith-dependency-visualization`) flags violations.
- A new component is **not** automatically used by any project. It is registered in a project once a base (or another component already in the project) imports it — then run `poly sync` (load `polylith-sync`).

## Verification
After creation, verify the component exists using your file tools (e.g., check `components/<namespace>/<name>/__init__.py`). Then, you will likely need to populate `core.py` and `__init__.py` using your file writing tools since they are created empty.
