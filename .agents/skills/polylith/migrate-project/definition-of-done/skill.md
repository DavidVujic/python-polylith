---
name: definition-of-done
description: Define the criteria for completing the migration process.
---

# Skill: definition-of-done

## Done When

### Structure
- Temporary migration base is gone or thin.
- Bases contain only entrypoints/wiring.
- All non-entrypoint code lives in components.

### Source Project
- `projects/<app>/` contains only:
  - Packaging config (`pyproject.toml`).
  - Runner scripts and task runners (`Makefile`, `Justfile`).
  - Project-specific config (e.g., `alembic.ini`).
- Project `pyproject.toml` references all required bricks.
- Brick names are meaningful and non-generic.
- Base names are project-prefixed to avoid collisions.

### Tests
- Tests are moved from `projects/<app>/tests/` to workspace level.
- Unit tests are organized according to the Polylith theme in use:
  - For the **loose theme**, unit tests mirror the brick structure: `test/<TARGET_TOP_NS>/<brick_name>/`.
  - For other themes, follow the workspace's test structure conventions.
- Integration tests live in a shared location (e.g., `test/integration/`).
- Shared fixtures live in `test/<TARGET_TOP_NS>/conftest.py` or `test/conftest.py`.
- `RUN_TEST_CMD` points to the test root.

### Infrastructure
- Infrastructure folders are moved to `infra/<folder>/<project-name>/`.

### Interfaces
- Each component defines its public API via `__init__.py`.
- Bricks import each other via those APIs.

### Linting and Type-Checking
- Linting and formatting use the workspace's configured tool(s).
- Type-checking uses the workspace's configured tool(s) (if applicable).
- `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` pass.

### Dependencies
- Workspace root `pyproject.toml` contains all third-party dependencies with version constraints.
- Project `pyproject.toml` lists runtime dependencies without version numbers.

### Cleanup
- Migration artifacts (e.g., `migration/<PROJECT>/state.md`, `migration/<PROJECT>/manifest.md`) are removed or kept for reference.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX info` to inspect the workspace and confirm all projects and bricks are correctly registered.