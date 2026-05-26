---
name: migrate-prepare-project
description: "[Internal sub-skill of `migrate-orchestrator` (phase 3 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Clean up the project subfolder and consolidate dependencies after extracting application code into bases."
---

# Skill: migrate-prepare-project

## Goal
Clean up the project subfolder (`projects/<PROJECT>/`) and consolidate dependencies. After this step, the project subfolder should contain only:
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

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### 1. Verify Project Subfolder
- Run `directory_tree` on `projects/<PROJECT>/` to confirm only infra and config files remain.

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
- List runtime dependencies **without version numbers** in the project `pyproject.toml`.
- Run `uv sync` (or equivalent for your package manager) to update the virtual environment.
- Verify dependencies with:
  ```bash
  uv run pip list  # Confirm all dependencies are installed
  uv run python -c "import <dependency>"  # Verify key dependencies are available
  ```

## Verify
- `RUN_TEST_CMD` succeeds against the **new** test location.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX info` to inspect the workspace and confirm the project is correctly registered.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| `RUN_TEST_CMD` collects 0 tests after step 3 | The command in `state.md` still references the old `projects/<PROJECT>/tests` path. | Update `RUN_TEST_CMD` to the new `test/<sanitized_project_name>/` location. Also check `[tool.pytest.ini_options].testpaths` / `rootdir` / `conftest.py` discovery. |
| Tests fail with `ModuleNotFoundError` on internal imports | Tests use `from tests.fixtures import …` and the `tests` package name changed. | Update test imports to the new test root path. If many tests reference the old name, consider keeping `tests` as the leaf directory and only renaming the parent. |
| `mock.patch("<old.path>")` fails with `AttributeError` | Mock patch strings reference moved modules. | Update patch strings to the new module paths. Use `grep -r 'patch("' test/` to find them all. |
| Infra folder move breaks deploy scripts that hardcoded paths (e.g., `helm/<chart>/values.yaml`) | Deploy scripts haven't been updated to the new `infra/<folder>/<project-name>/` location. | Either update the scripts, or symlink the new location from the old one as a transitional step (record the symlink in `migration/<PROJECT>/state.md`). |
| `poly check` complains about brick references after dependency consolidation | A runtime dependency was moved to the workspace root but the project's `pyproject.toml` doesn't declare it. | Add the dependency name (no version) back to the project's `[project.dependencies]`. The version stays only at the workspace root. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase 3 — prepare-project"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
