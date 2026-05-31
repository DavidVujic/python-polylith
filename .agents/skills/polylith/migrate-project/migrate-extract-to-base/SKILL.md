---
name: migrate-extract-to-base
description: "[Internal sub-skill of `migrate-orchestrator` (phase 2 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Extract all application code from `projects/<PROJECT>/` into a temporary migration base."
---

# Skill: migrate-extract-to-base

## Goal
Extract all application code from `projects/<PROJECT>/` into a temporary migration base (`bases/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>/`).

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `ORIG_TOP_NS`
- `TARGET_TOP_NS` (default: `ORIG_TOP_NS`)
- `INITIAL_BASE_NAME`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

From `migration/<PROJECT>/manifest.md`:
- Directory tree and module map.

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### 1. Create the Base Directory
- Create `bases/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>/`.

### 2. Move Application Code
- Move application packages/modules from `projects/<PROJECT>/` to the base:
  - For `src/` layout: Move `projects/<PROJECT>/src/<pkg>/` under the base.
  - For flat layout: Move `projects/<PROJECT>/<pkg>/` under the base.
- Leave non-code files (Dockerfiles, k8s manifests, deploy scripts, `pyproject.toml`) in `projects/<PROJECT>/`.

### 3. Update `pyproject.toml`
- Add the base to `[tool.polylith.bricks]`:
  ```toml
  [tool.polylith.bricks]
  "../../bases/<TARGET_TOP_NS>/<INITIAL_BASE_NAME>" = "<TARGET_TOP_NS>/<INITIAL_BASE_NAME>"
  ```

### 4. Fix Imports
- Update imports minimally to ensure tests and linting pass.

### 5. Update `manifest.md`
- Reflect the new structure in `migration/<PROJECT>/manifest.md`.

### 6. Handle Namespace Changes
If `TARGET_TOP_NS != ORIG_TOP_NS`, the migration orchestrator will handle this in subsequent phases:

1. `migrate-generate-shim` will create a compatibility shim at `projects/<PROJECT>/<ORIG_TOP_NS>/__init__.py` that re-exports from `<TARGET_TOP_NS>`.
2. `migrate-automate-import-updates` will update imports in the new base location to reference the new namespace.
3. `migrate-update-tests` will update test files to use the compatibility shim.

### 7. Use Shims if Needed
- If imports break during this phase, add minimal temporary shims to re-export names from the new brick API.
- Track shims in `migration/shims.md`.
- Note that comprehensive shim generation will be handled in the `migrate-generate-shim` phase.

## Verify
- `RUN_TEST_CMD` succeeds with the same pass/fail counts as the pre-migration baseline recorded in `migrate-discover`.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX sync` to synchronize the `[tool.polylith.bricks]` table with actual imports.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| `ModuleNotFoundError: No module named '<ORIG_TOP_NS>.<x>'` after move | `TARGET_TOP_NS != ORIG_TOP_NS` and imports weren't rewritten or shimmed. | Either rewrite all imports (step 6 option B) or add a shim under `ORIG_TOP_NS` that re-exports from `TARGET_TOP_NS` (step 6 option A). Record the choice in `migration/shims.md`. |
| `RUN_TEST_CMD` collects 0 tests after the move | Test files moved but `pytest` rootdir / `testpaths` still points at the old `projects/<PROJECT>/tests` location. | Update `pyproject.toml` `[tool.pytest.ini_options].testpaths` or pass explicit dirs in `RUN_TEST_CMD`. (Note: `migrate-prepare-project` moves tests properly — if extract-to-base touched tests at all, consider undoing that part.) |
| `poly check` reports "brick imports another brick that is not in `[tool.polylith.bricks]`" | Step 3 only added the base; imports inside the base may pull in components not yet listed. | Run `POLY_CMD_PREFIX sync --quiet` to populate the rest, then re-run `check`. |
| Editable install / build fails (`error: package directory '<x>' does not exist`) | The base move broke the previous `[tool.setuptools]` or `[tool.hatch.build]` `packages` setting in `projects/<PROJECT>/pyproject.toml`. | Update `packages` to point at the new `<TARGET_TOP_NS>` namespace, or remove the explicit `packages` setting and let Polylith's build hook handle it. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase 2 — extract-to-base"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
