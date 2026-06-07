---
name: polylith-migrate-distribute-wiring
description: "[Internal sub-skill of `polylith-migrate-orchestrator`. Do not load directly — load `polylith-migrate-orchestrator` first, which drives all phases.] Distribute app-wiring code from the residual component into the appropriate bases and shared components."
---

# Skill: polylith-migrate-distribute-wiring

## Goal
Distribute app-wiring code from the residual component into the appropriate bases and shared components.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `INITIAL_BASE_NAME`
- Verification commands.
- Base names.

From `migration/<PROJECT>/manifest.md`:
- Current module map, including what remains in the residual component.

> All inputs from `state.md` are assumed to satisfy the validation rules in `polylith-migrate-discover` (`### Validation rules`). Validate before proceeding.

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

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| Two bases now import the same `init_<x>` function and the residual still exists | Step 6 wasn't reached — the function moved into one base but the residual reference wasn't deleted. | Confirm the residual is gone; if `init_<x>` is genuinely shared by 2+ bases, it belongs in a shared `bootstrap` component (step 3), not in either base. |
| `mock.patch("<TARGET_TOP_NS>.<INITIAL_BASE_NAME>.init_api")` fails after the move | The test references the old residual path; the function now lives in a base. | Update mock patch strings to the new location, typically `<TARGET_TOP_NS>.<base_name>.<init_func>`. |
| `poly check` says the residual brick is still declared but its files are gone | `pyproject.toml` `[tool.polylith.bricks]` still lists the deleted brick. | Remove the line from `[tool.polylith.bricks]` and re-run `POLY_CMD_PREFIX sync --quiet`. |
| Application starts but a runtime feature is missing (e.g., logging, DB) | A shared init helper was moved into one base only. The other base never calls it. | Promote the helper to a shared `bootstrap` component and call it from every base's startup path. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase <N> — distribute-wiring"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.