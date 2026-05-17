---
name: distribute-wiring
description: Distribute app-wiring code from the residual component into the appropriate bases and shared components.
---

# Skill: distribute-wiring

## Goal
Distribute app-wiring code from the residual component into the appropriate bases and shared components.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `BRICK_NAME`
- Verification commands.
- Base names.

From `migration/<PROJECT>/manifest.md`:
- Current module map, including what remains in the residual component.

## Steps

### 1. Read the Residual Component
- List every public function remaining in the residual module.
- Confirm it contains only app-wiring code.

### 2. Identify the Split
- Trace callers of each function (use `grep`).
- Group callers by base or runner script.
- Map each function to its natural base:

| Function Pattern | Belongs In | Rationale |
|------------------|------------|-----------|
| `init_consumer`, `close_consumer` | Handler/consumer base | Kafka consumer lifecycle is handler-specific |
| `init_job` | Jobs base | Job bootstrap is jobs-specific |
| `init_api` / app factory | API base | HTTP server setup is API-specific |

### 3. Extract Shared Helpers
- Identify shared init functions (e.g., `init_logging`, `init_db`).
- Move shared helpers to a `bootstrap` component if needed.

### 4. Move Composite Functions
- Move composite functions to their respective bases.
- Update runner scripts to import from the base directly.

### 5. Update Tests
- Update integration tests to monkeypatch the correct module.

### 6. Clean Up
- Delete the residual component directory.
- Update `pyproject.toml` to remove the residual brick.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX sync` to synchronize the `[tool.polylith.bricks]` table with actual imports.