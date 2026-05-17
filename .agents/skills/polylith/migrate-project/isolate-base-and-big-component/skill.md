---
name: isolate-base-and-big-component
description: Shrink the temporary migration base into thin base(s) + one big component. Bases contain only entrypoints/wiring, while the big component contains everything else.
---

# Skill: isolate-base-and-big-component

## Goal
Shrink the temporary migration base into thin base(s) + one big component:
- **Bases**: Contain only entrypoints/wiring (e.g., FastAPI endpoints, CLI wiring, consumer wiring).
- **Big Component**: Contains all other code.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `BRICK_NAME`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Entrypoints list.

## Steps

### 1. Create the Big Component
- Create `components/<TARGET_TOP_NS>/<BRICK_NAME>/`.

### 2. Move Non-Entrypoint Code
- Move non-entrypoint code from the base(s) to the big component.

### 3. Define Public API
- Define a minimal public API in `components/<TARGET_TOP_NS>/<BRICK_NAME>/__init__.py`.

### 4. Update Bases
- Update bases to import only from component APIs:
  ```python
  from <TARGET_TOP_NS>.<BRICK_NAME> import ...
  ```

### 5. Update `pyproject.toml`
- Add the new component to `[tool.polylith.bricks]`:
  ```toml
  [tool.polylith.bricks]
  "../../bases/<TARGET_TOP_NS>/<base>" = "<TARGET_TOP_NS>/<base>"
  "../../components/<TARGET_TOP_NS>/<BRICK_NAME>" = "<TARGET_TOP_NS>/<BRICK_NAME>"
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
