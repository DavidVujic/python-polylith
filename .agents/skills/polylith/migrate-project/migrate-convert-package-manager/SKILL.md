---
name: migrate-convert-package-manager
description: "[Internal sub-skill of `migrate-orchestrator` (optional, runs only when opted in during `migrate-discover`). Do not load directly — load `migrate-orchestrator` first.] Convert the project's `pyproject.toml` to PEP 621/uv-workspaces format and register it as a uv-workspace member. **Opinionated about uv** — only applies when the workspace itself uses uv. Skip otherwise."
---

# Skill: migrate-convert-package-manager

> ⚠ **Opinionation gate.** This skill is **explicitly opinionated about uv**. It does not generalize to Poetry, PDM, or Hatch workspaces. If your Polylith workspace uses one of those, **do not run this skill** — align the project to the workspace's manager via a manual step instead, and leave `CONVERT_PACKAGE_MANAGER=no` in `state.md`.

## Goal
Convert the project's `pyproject.toml` to PEP 621/uv format and register it as a uv-workspace member. This makes the project share the workspace's single lock file and virtual environment, preventing version skew.

## When to Skip
Skip this skill if **any** of the following holds:
- `PACKAGE_MANAGER=uv` already in `migration/<PROJECT>/state.md` (nothing to convert).
- The workspace root does **not** use uv (this skill does not apply — see the opinionation gate above).
- `CONVERT_PACKAGE_MANAGER=no` in `state.md` (user opted out during `migrate-discover`).

### Verify the workspace uses uv before proceeding
Open the **workspace root** `pyproject.toml` and look for `[tool.uv.workspace]` and/or a sibling `uv.lock`. If neither is present, **stop**: this skill does not apply.

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `PACKAGE_MANAGER`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

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

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| Workspace root does not use uv (no `[tool.uv.workspace]`, no `uv.lock`) | This skill does not apply — the opinionation gate at the top of this file rules it out. | Stop. Set `CONVERT_PACKAGE_MANAGER=no` in `state.md`. Align the project to the workspace's actual manager (Poetry/PDM/Hatch) via a manual step instead. |
| `uv lock` fails with "no version satisfies …" after adding the project as a workspace member | Project's old version constraints conflict with the workspace root's pins. | Relax the workspace root's range, or, if the project legitimately needs a different version, pin it explicitly in the project's `pyproject.toml`. As a last resort, exclude the project from the workspace and use a separate environment. |
| Project depends on a private/internal package that the workspace root doesn't know about | Private index or path-dependency not declared at the root. | Add the dependency (and its source — `[tool.uv.sources]` or `[[tool.uv.index]]`) to the workspace root `pyproject.toml`. |

## Done When
- The project is listed as a workspace member in the root `pyproject.toml`.
- `uv lock` and `uv sync` succeed from the workspace root.
- Old lock files (`poetry.lock`, `Pipfile.lock`, generated `requirements*.txt`) are deleted from the project directory.
- `PACKAGE_MANAGER=uv` is recorded in `migration/<PROJECT>/state.md`.
- Verification commands in `state.md` use `uv run`.
- Tests pass via `uv run`.

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase optional — convert-package-manager"
```

Substitute `<PROJECT>` from `state.md`. This is an **optional** skill off the numbered main line, so the commit uses the literal `phase optional` label (no `<N>`). Do not proceed without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.