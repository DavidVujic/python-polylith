---
name: migrate-prepare-project
description: "[Internal sub-skill of `migrate-orchestrator`. Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Clean up the project subfolder and consolidate dependencies after extracting application code into bases."
---

# Skill: migrate-prepare-project

## Goal
Clean up the project subfolder (`projects/<PROJECT>/`) and consolidate dependencies. After this step, the project subfolder should contain only:
- Project `pyproject.toml` (with brick references).
- Task runners (`Makefile`, `Justfile`).
- Project-specific config (e.g., `alembic.ini` **and** its `alembic/` directory).
- Compatibility shim (only when `SHIM_STRATEGY=shim`).

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
- Run `directory_tree` on `projects/${PROJECT}/` to confirm only infra and config files remain.

### 2. Update `pyproject.toml`
- Add brick references to `[tool.polylith.bricks]`:
  ```toml
  [tool.polylith.bricks]
  "../../bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}" = "${TARGET_TOP_NS}/${INITIAL_BASE_NAME}"
  ```
- Register the project alias and group in `workspace.toml` (if provided):
  ```toml
  [tool.polylith.projects.alias]
  ${PROJECT} = "${ALIAS}"

  [tool.polylith.projects.groups]
  ${GROUP} = ["${PROJECT}"]
  ```

### 3. Move Tests to Workspace Level
- Move `tests/` to `test/<test-dir>/`, where `<test-dir>` is a **valid Python package name**. ⚠ `${PROJECT}` frequently contains hyphens (e.g. `order-management-api`), which are **illegal in a package name** and break pytest's package-style import. Derive an underscore name — the workspace's `<svc>_service` convention is a good default (e.g. `order_management_service`). Record `<test-dir>` in `state.md`.
- If the moved tests import the old package by name (e.g. `from tests.fixtures import …` / `from tests.helpers import …`), rewrite those to the new name (`from <test-dir>.fixtures import …`). Brick imports (`<TARGET_TOP_NS>.*`) are absolute and need no change.
- Update `RUN_TEST_CMD` in `migration/${PROJECT}/state.md` to point to the new location.
- Update mock patch strings in test files if paths changed.
> Per-brick test redistribution (`test/<theme>/<ns>/<brick>/`) is handled later in `migrate-refactor-tests` — this step only lifts tests to the workspace level. See that skill for the shared-helper / namespace-merge caveats before splitting further.

### 4. Move Infrastructure Folders
- Move **deployment** infra folders (e.g., `helm/`, `k8s/`, `kustomize/`, `skaffold/`) to `infra/<folder>/${PROJECT}/`.
- **Keep `alembic/` together with `alembic.ini` in the project** — do **not** split them. `alembic.ini`'s `script_location` points at `alembic/` relatively, and `alembic/env.py` imports the project's bricks; separating them breaks migrations. (Alembic is project-specific config, which the project subfolder is allowed to keep.)
- ⚠ **Deploy-path breakage:** moving infra breaks deploy scripts / `skaffold` / CI that hardcode the old paths. If you **cannot verify the deploy** in the migration environment (no deploy / manifest-diff cycle available), it is acceptable to **defer the infra move and document it** in `state.md` rather than relocate blindly. Otherwise, update the referencing scripts (or add a transitional symlink) and record the change.

### 5. Consolidate Dependencies
- Move third-party dependencies with version constraints to the workspace root `pyproject.toml`.
- Move dev/test/tooling dependencies to the workspace root.
- List runtime dependencies **without version numbers** in the project `pyproject.toml`.
- Sync the virtual environment with the project's package manager (e.g. `uv sync`,
  `pdm install`, `poetry install` — match `PACKAGE_MANAGER` in `state.md`).
- Verify dependencies, substituting your package manager's run prefix (`<RUN>` =
  `uv run` / `pdm run` / `poetry run` / bare in an activated venv):
  ```bash
  <RUN> pip list  # Confirm all dependencies are installed
  <RUN> python -c "import <dependency>"  # Verify key dependencies are available
  ```

## Verify
- `RUN_TEST_CMD` succeeds against the **new** test location.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX info` to inspect the workspace and confirm the project is correctly registered.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| `RUN_TEST_CMD` collects 0 tests after step 3 | The command in `state.md` still references the old `projects/${PROJECT}/tests` path. | Update `RUN_TEST_CMD` to the new `test/${PROJECT}/` location. Also check `[tool.pytest.ini_options].testpaths` / `rootdir` / `conftest.py` discovery. |
| Tests fail with `ModuleNotFoundError` on internal imports | Tests use `from tests.fixtures import …` and the `tests` package name changed. | Update test imports to the new test root path. If many tests reference the old name, consider keeping `tests` as the leaf directory and only renaming the parent. |
| `mock.patch("<old.path>")` fails with `AttributeError` | Mock patch strings reference moved modules. | Update patch strings to the new module paths. Use `grep -r 'patch("' test/` to find them all. |
| Infra folder move breaks deploy scripts that hardcoded paths (e.g., `helm/<chart>/values.yaml`) | Deploy scripts haven't been updated to the new `infra/<folder}/${PROJECT}/` location. | Either update the scripts, or symlink the new location from the old one as a transitional step (record the symlink in `migration/${PROJECT}/state.md`). |
| `poly check` complains about brick references after dependency consolidation | A runtime dependency was moved to the workspace root but the project's `pyproject.toml` doesn't declare it. | Add the dependency name (no version) back to the project's `[project.dependencies]`. The version stays only at the workspace root. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase <N> — prepare-project"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
