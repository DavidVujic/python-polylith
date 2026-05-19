---
name: migrate-isolate-base-and-big-component
description: "[Internal sub-skill of `migrate-orchestrator` (phase 4 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Shrink the temporary migration base into thin base(s) + one big component. Bases contain only entrypoints/wiring, while the big component contains everything else."
---

# Skill: migrate-isolate-base-and-big-component

## Goal
Shrink the temporary migration base into thin base(s) + one big component:
- **Bases**: Contain only entrypoints/wiring (e.g., FastAPI endpoints, CLI wiring, consumer wiring).
- **Big Component**: Contains all other code.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `INITIAL_BASE_NAME`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Entrypoints list.

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### 1. Create the Big Component
- Create `components/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>/`.

### 2. Move Non-Entrypoint Code
- Move non-entrypoint code from the base(s) to the big component.

### 3. Define Public API
- Define a minimal public API in `components/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>/__init__.py`.

### 4. Update Bases
- Update bases to import only from component APIs:
  ```python
  from <TARGET_TOP_NS>.<INITIAL_BASE_NAME> import ...
  ```

### 5. Update `pyproject.toml`
- Add the new component to `[tool.polylith.bricks]`:
  ```toml
  [tool.polylith.bricks]
  "../../bases/<TARGET_TOP_NS>/<base>" = "<TARGET_TOP_NS>/<base>"
  "../../components/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>" = "<TARGET_TOP_NS>/<INITIAL_BASE_NAME>"
  ```

### 6. Update `manifest.md`
- Reflect the new structure in `migration/<PROJECT>/manifest.md`.

### 7. FastAPI Guidance
| Stays in Base | Moves to Big Component |
|---------------|------------------------|
| `app = FastAPI(...)` | Domain/business logic |
| Middleware, router registration | Persistence/repositories |
| Route handlers (endpoints) | External integrations |
| Startup/shutdown/lifespan wiring | Reusable parsing/validation |

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX sync` to synchronize the `[tool.polylith.bricks]` table with actual imports.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| Circular import: base imports from component, component imports back from base | Some "non-entrypoint" code was moved but still references base-only helpers (e.g. the FastAPI `app` instance). | Move the helper down into the component, or invert the dependency by passing the needed value as a function argument. The base's `app` instance must **never** be imported by a component. |
| `ImportError: cannot import name '<x>' from '<TARGET_TOP_NS>.<INITIAL_BASE_NAME>'` | The big component's `__init__.py` doesn't re-export `<x>`. Code that previously reached into submodules now needs the public API. | Add `from <TARGET_TOP_NS>.<INITIAL_BASE_NAME>.<submodule> import <x>` to the component's `__init__.py`, or have the caller import the submodule directly (and accept the brick-interface violation that `poly deps --interface` will flag). |
| Base file becomes near-empty after the split | Good — that's the goal. But check: is there *any* wiring left, or did you accidentally move the entrypoint itself? | If the entrypoint (e.g., `app = FastAPI(...)`) ended up in the component, move it back to the base. The base must own the entrypoint object. |
| `poly check` flags the component as not used by any project | The base's imports go to the wrong namespace (e.g., `from <ORIG_TOP_NS>...`) so the import graph doesn't reach the component. | Update base imports to `from <TARGET_TOP_NS>.<INITIAL_BASE_NAME> import …` and re-run `POLY_CMD_PREFIX sync`. |
| Tests for moved code now fail to find fixtures | `conftest.py` was left in the base or moved to the wrong scope. | Move test fixtures alongside the code they cover; usually that's under `test/components/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>/`. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase 4 — isolate-base-and-big-component"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
