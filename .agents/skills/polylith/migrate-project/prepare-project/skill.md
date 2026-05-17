---
name: prepare-project
description: Clean up the project subfolder and consolidate dependencies after extracting application code into bases.
---

# Skill: prepare-project

## Goal
Clean up the project subfolder (`projects/<app>/`) and consolidate dependencies. After this step, the project subfolder should contain only:
- Project `pyproject.toml` (with brick references).
- Task runners (`Makefile`, `Justfile`).
- Project-specific config (e.g., `alembic.ini`).

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `TARGET_TOP_NS`
- `ALIAS` (optional: `GROUP`)
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Infra files list.

## Steps

### 1. Verify Project Subfolder
- Run `directory_tree` on `projects/<app>/` to confirm only infra and config files remain.

### 2. Update `pyproject.toml`
- Add brick references to `[tool.polylith.bricks]`:
  ```toml
  [tool.polylith.bricks]
  "../../bases/<TARGET_TOP_NS>/<base>" = "<TARGET_TOP_NS>/<base>"
  ```
- Register the project alias and group in `workspace.toml` (if provided):
  ```toml
  [tool.polylith.projects.alias]
  <project-directory-name> = "<ALIAS>"

  [tool.polylith.projects.groups]
  <group-name> = ["<project-directory-name>"]
  ```

### 3. Move Tests to Workspace Level
- Move `tests/` to `test/<sanitized_project_name>/`.
- Update `RUN_TEST_CMD` in `migration/<PROJECT>/state.md` to point to the new location.
- Update imports and mock patch strings in test files if paths changed.

### 4. Move Infrastructure Folders
- Move infra folders (e.g., `helm/`, `k8s/`, `kustomize`, `alembic/`) to `infra/<folder>/<project-name>/`.

### 5. Consolidate Dependencies
- Move third-party dependencies with version constraints to the workspace root `pyproject.toml`.
- Move dev/test/tooling dependencies to the workspace root.
- List runtime dependencies without version numbers in the project `pyproject.toml`.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX info` to inspect the workspace and confirm the project is correctly registered.
