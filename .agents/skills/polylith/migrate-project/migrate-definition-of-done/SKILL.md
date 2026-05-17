---
name: migrate-definition-of-done
description: "[Internal sub-skill of `migrate-orchestrator` (phase 11 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Define the criteria for completing the migration process."
---

# Skill: migrate-definition-of-done

## Done When

### Structure
- Temporary migration base is gone or thin.
- Bases contain only entrypoints/wiring.
- All non-entrypoint code lives in components.

### Source Project
- `projects/<PROJECT>/` contains only:
  - Packaging config (`pyproject.toml`).
  - Runner scripts and task runners (`Makefile`, `Justfile`).
  - Project-specific config (e.g., `alembic.ini`).
- Project `pyproject.toml` references all required bricks.
- Brick names are meaningful and non-generic.
- Base names are project-prefixed to avoid collisions.

### Tests
- Tests are moved from `projects/<PROJECT>/tests/` to workspace level.
- Unit tests are organized according to the Polylith theme in use:
  - **`loose` theme:** unit tests live under `test/bases/<TARGET_TOP_NS>/<base>/` and `test/components/<TARGET_TOP_NS>/<component>/`.
  - **`tdd` theme:** unit tests live under `bases/<base>/test/<TARGET_TOP_NS>/<base>/` and `components/<component>/test/<TARGET_TOP_NS>/<component>/`.
- Integration tests live in a shared location (e.g., `test/integration/`).
- Shared fixtures live in `test/<TARGET_TOP_NS>/conftest.py` or `test/conftest.py`.
- `RUN_TEST_CMD` points to the test root **and collects the same number of tests as the pre-migration baseline**.

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
- Migration artifacts (`migration/<PROJECT>/state.md`, `migration/<PROJECT>/manifest.md`, and any `migration/shims.md`) are either removed or kept under `migration/<PROJECT>/` for reference (user's choice).
- The migration branch (`GIT_BRANCH` from `state.md`) is ready to be merged or rebased into the main branch. Per-phase commits remain available for review/bisect.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX info` to inspect the workspace and confirm all projects and bricks are correctly registered.