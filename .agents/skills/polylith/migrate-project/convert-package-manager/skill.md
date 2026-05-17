---
name: convert-package-manager
description: Convert the project's `pyproject.toml` to PEP 621/uv format and register it as a workspace member (if the user opts in).
---

# Skill: convert-package-manager

## Goal
Convert the project's `pyproject.toml` to PEP 621/uv format and register it as a workspace member. This step ensures the project shares the workspace's single lock file and virtual environment, preventing version skew.

## When to Skip
- If `PACKAGE_MANAGER=uv` in `migration/<PROJECT>/state.md`, skip this step and proceed to the next skill.

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `PACKAGE_MANAGER`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

## Steps

### 1. Ask for User Approval
- Ask the user if they want to convert the project's `pyproject.toml` to PEP 621/uv format.
- Record their choice in `state.md`:
  ```text
  CONVERT_PACKAGE_MANAGER=<yes|no>
  ```

### 2. Rewrite `pyproject.toml` to PEP 621/uv Format
- Move `[tool.poetry.dependencies]` to `[project] dependencies`. Keep only **runtime** (non-dev, non-test) dependencies in the project, listed **without version constraints**.
- Remove Poetry-specific sections: `[tool.poetry]`, `[tool.poetry.group.*]`, `[[tool.poetry.source]]`, and `[build-system]` with `poetry-core`.
- Add a `[build-system]` with `hatchling` (or the workspace's build backend).
- Preserve `[tool.*]` sections for other tools (e.g., pytest, ruff, mypy).
- Add `[tool.uv]` only if project-level uv configuration is needed.

### 3. Register as a Workspace Member
- Add the project path to the workspace root `pyproject.toml` under `[tool.uv.workspace] members`.
  Example:
  ```toml
  members = ["projects/example-service-b"]
  ```

### 4. Consolidate Dependencies
- Add all **third-party runtime dependencies with version constraints** to the workspace root `pyproject.toml` `[project] dependencies`.
- Move all dev/test/tooling dependencies to the workspace root `[dependency-groups]` (e.g., `dev = [...]`, `test = [...]`).
- Ensure the project's `pyproject.toml` lists runtime dependencies **without version numbers**.

### 5. Lock and Sync
- Run `uv lock` from the workspace root to regenerate `uv.lock` with the new member.
- Run `uv sync` to install all dependencies into the shared `.venv`.
- Resolve any version conflicts that arise during `uv lock`.

### 6. Delete Old Lock Files
- Remove `poetry.lock`, `Pipfile.lock`, and generated `requirements*.txt` from the project directory.

### 7. Update Verification Commands
- Replace any `poetry run`, `pipenv run`, or bare commands with `uv run` equivalents in `migration/<PROJECT>/state.md`.
  Example:
  ```text
  RUN_TEST_CMD=uv run pytest <test-dirs>
  RUN_LINT_CMD=uv run ruff check <dirs>
  ```
- Update `PACKAGE_MANAGER=uv` in `state.md`.

## Verify
- Run the updated `RUN_TEST_CMD` and confirm the same pass/fail counts as before the conversion.
- If set, run `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD`.
- Ensure `uv lock` and `uv sync` succeed from the workspace root.

## Done When
- The project is listed as a workspace member in the root `pyproject.toml`.
- `uv lock` and `uv sync` succeed from the workspace root.
- Old lock files (`poetry.lock`, `Pipfile.lock`, generated `requirements*.txt`) are deleted from the project directory.
- `PACKAGE_MANAGER=uv` is recorded in `migration/<PROJECT>/state.md`.
- Verification commands in `state.md` use `uv run`.
- Tests pass via `uv run`.