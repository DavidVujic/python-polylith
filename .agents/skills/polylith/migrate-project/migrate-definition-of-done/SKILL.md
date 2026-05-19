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

## End-to-end checks

These checks go beyond per-phase verification and exercise the migrated project as a whole. **All three must pass.**

### 1. Entrypoint smoke test

For **each base** in the project, smoke-test its entrypoint:

- **HTTP API base** → start the server and curl a health endpoint (or any GET that doesn't require auth). Verify it returns 200.
- **CLI base** → run `<cli> --help` and a no-op subcommand. Verify exit code 0.
- **Worker/consumer base** → start the process and observe one cycle of its main loop in the logs. Stop it cleanly.
- **Lambda / Cloud Function base** → invoke the handler with a representative event payload (mocked or recorded). Verify it returns without exception.

If any base fails to start, the migration is **not done** — return to `migrate-distribute-wiring` and check entrypoint wiring.

### 2. Baseline test count restored

Compare collected test count to the baseline recorded by `migrate-discover`:

```bash
<RUN_TEST_CMD_with --collect-only -q | tail -1>
```

The count must **equal** the baseline. A lower count means `pytest` discovery is misconfigured (see `migrate-refactor-tests` failure modes). A higher count means tests were inadvertently duplicated during the move.

### 3. No undocumented shims remain

Inspect `migration/<PROJECT>/shims.md` (if it exists):

- **Empty or absent** → ✅ proceed.
- **Lists active shims** → either remove them now (rewrite imports to the new namespace and delete the shim modules) or schedule their removal as a follow-up PR and reference that PR in the migration branch description. Do **not** merge with undocumented shims.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX info` to inspect the workspace and confirm all projects and bricks are correctly registered.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| `RUN_TEST_CMD` passes but collected test count is lower than the baseline from `migrate-discover` | `pytest` discovery is misconfigured after the test reorganisation. | Update `[tool.pytest.ini_options].testpaths` (or pass paths explicitly in `RUN_TEST_CMD`). Run `pytest --collect-only` and diff against baseline collection. See `migrate-refactor-tests` for details. |
| `poly check` is green and tests pass, but the application doesn't start | Entrypoint wiring regression — a base imports something that no longer exists at the expected path, but no test exercises the boot path. | Smoke-test each base's entrypoint manually (run the FastAPI server, invoke the CLI, send a test event to the consumer). Revisit `migrate-distribute-wiring`. |
| `migration/shims.md` still lists active shims | Shims from `migrate-extract-to-base` (namespace change) were never removed. | Either rewrite imports to the new namespace and delete the shims, or schedule shim removal as a follow-up PR and note it in the migration branch description. Do not merge with undocumented shims. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase 11 — definition-of-done"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.