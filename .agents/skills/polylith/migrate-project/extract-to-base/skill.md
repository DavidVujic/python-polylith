---
name: extract-to-base
description: Extract all application code from `projects/<app>/` into a temporary migration base.
---

# Skill: extract-to-base

## Goal
Extract all application code from `projects/<app>/` into a temporary migration base (`bases/<TARGET_TOP_NS>/<BRICK_NAME>/`).

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `ORIG_TOP_NS`
- `TARGET_TOP_NS` (default: `ORIG_TOP_NS`)
- `BRICK_NAME`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

From `migration/<PROJECT>/manifest.md`:
- Directory tree and module map.

## Steps

### 1. Create the Base Directory
- Create `bases/<TARGET_TOP_NS>/<BRICK_NAME>/`.

### 2. Move Application Code
- Move application packages/modules from `projects/<app>/` to the base:
  - For `src/` layout: Move `projects/<app>/src/<pkg>/` under the base.
  - For flat layout: Move `projects/<app>/<pkg>/` under the base.
- Leave non-code files (Dockerfiles, k8s manifests, deploy scripts, `pyproject.toml`) in `projects/<app>/`.

### 3. Update `pyproject.toml`
- Add the base to `[tool.polylith.bricks]`:
  ```toml
  [tool.polylith.bricks]
  "../../bases/<TARGET_TOP_NS>/<BRICK_NAME>" = "<TARGET_TOP_NS>/<BRICK_NAME>"
  ```

### 4. Fix Imports
- Update imports minimally to ensure tests and linting pass.

### 5. Update `manifest.md`
- Reflect the new structure in `migration/<PROJECT>/manifest.md`.

### 6. Handle Namespace Changes
If `TARGET_TOP_NS != ORIG_TOP_NS`, choose one of the following options:

| Option | Description | Risk |
|--------|-------------|------|
| **Compatibility Shim** | Keep `ORIG_TOP_NS` as a shim that re-exports from `TARGET_TOP_NS`. | Lower |
| **Rewrite Imports** | Rewrite all imports to the new namespace in one go. | Higher |

### 7. Use Shims if Needed
- If imports break, add temporary shims to re-export names from the new brick API.
- Track shims in `migration/shims.md`.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX sync` to synchronize the `[tool.polylith.bricks]` table with actual imports.
