---
name: convert-linter
description: Remove project-specific linting and formatting configurations and consolidate them into the workspace root. Align the project with the workspace's linting and formatting standards.
---

# Skill: convert-linter

## Goal
Remove project-specific linting and formatting configurations and consolidate them into the workspace root. Align the project with the workspace's linting and formatting standards.

## When to Skip
Skip this step if the project's `LINTER` and `FORMATTER` in `migration/<PROJECT>/state.md` match the workspace's tools.

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `LINTER`, `FORMATTER`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

## Steps

### 1. Remove Project-Specific Configs and Dependencies
- Remove the following sections from the project's `pyproject.toml`:
  - `[tool.black]`, `[tool.isort]`, `[tool.flake8]`, `[tool.pylint.*]`, `[tool.autopep8]`, `[tool.pycodestyle]`
- Remove standalone config files: `.flake8`, `.pylintrc`, `.isort.cfg`, and lint sections in `setup.cfg` or `tox.ini`.
- Remove old linter/formatter dependencies from the project's `pyproject.toml`:
  - `flake8`, `flake8-*` plugins, `pylint`, `pylint-*` plugins, `black`, `isort`, `autopep8`, `pyflakes`, `pycodestyle`, `bandit`

### 2. Assess Workspace Linting Config
- Review the workspace root's linting and formatting configuration.
- Identify any project-specific rules or ignores that differ from the workspace's standards.

### 3. Merge Project-Specific Rules
- If the project has unique linting rules or ignores, merge them into the workspace root's linting configuration (e.g., `[tool.ruff]`).
- For conflicts (e.g., stricter rules in the project), ask the user to provide guidance on whether to:
  - Adopt the project's rules in the workspace.
  - Suppress the project's rules in favor of the workspace's.
  - Defer the decision and document the conflict in `migration/<PROJECT>/state.md`.

### 4. Run Workspace Linting and Formatting Tools
- Run the workspace's linting tool to assess violations:
  - **Few new violations**: Fix them now.
  - **Many new violations**: Ask the user whether to fix, suppress, or defer.
- Run the workspace's formatting tool to reformat the code.

### 5. Update `state.md`
- Set `LINTER` and `FORMATTER` to the workspace's tool(s).
- Update `RUN_LINT_CMD` to use the workspace's linting and formatting commands.

## Verify
- The workspace's linting tool passes (or remaining violations are user-approved).
- The workspace's formatting tool passes.
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_TYPECHECK_CMD` succeeds.

## Done When
- No project-specific linter/formatter config files or dependencies remain.
- Project-specific linting rules are merged into the workspace root's configuration.
- `LINTER` and `FORMATTER` in `migration/<PROJECT>/state.md` match the workspace's tools.
- Tests pass via the workspace's tooling.
