---
name: convert-type-checker
description: Replace the project's existing type checker with the workspace's configured type-checking tool to align with the workspace's standards.
---

# Skill: convert-type-checker

## Goal
Replace the project's existing type checker with the workspace's configured type-checking tool to align with the workspace's standards.

## When to Skip
Skip this step if the project's `TYPE_CHECKER` in `migration/<PROJECT>/state.md` matches the workspace's type-checking tool.

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `TYPE_CHECKER`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

## Steps

### 1. Remove Old Configs and Dependencies
- Remove the following sections from `pyproject.toml`:
  - `[tool.mypy]`, `[[tool.mypy.overrides]]`, `[mypy-*]`, `[tool.pyright]`, `[tool.pytype]`
- Remove standalone config files: `mypy.ini`, `.mypy.ini`, `pyrightconfig.json`.
- Remove old type checker dependencies from `pyproject.toml`:
  - `mypy`, `mypy-extensions`, `types-*` stub packages, `pyright`, `pytype`, `sqlalchemy-stubs`, `django-stubs`.

### 2. Clean Up Type Ignore Comments
- Remove `# type: ignore[<mypy-code>]` comments that reference mypy-specific error codes.
- Leave comments that suppress real issues and document them in `state.md`.

### 3. Adopt Workspace Type-Checking Config
- The workspace root `pyproject.toml` may define the type-checking configuration. The project inherits this config.
- Add project-specific overrides if needed.

### 4. Run the Workspace's Type-Checking Tool
- Run the workspace's type-checking tool to assess errors:
  - **Same or fewer errors**: No action needed.
  - **New errors**: Ask the user whether to fix, suppress, or adjust the config.
  - **Missing stub errors**: Silence with per-module ignores in the workspace's type-checking config.

### 5. Update `state.md`
- Set `TYPE_CHECKER` to the workspace's type-checking tool.
- Update `RUN_TYPECHECK_CMD` to use the workspace's type-checking command.

## Verify
- The workspace's type-checking tool runs cleanly (or remaining errors are user-approved).
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` succeeds.

## Done When
- No old type checker config files remain.
- Old type checker dependencies are removed from `pyproject.toml`.
- Stale `# type: ignore` comments referencing tool-specific codes are removed (or documented if intentionally kept).
- `TYPE_CHECKER` in `migration/<PROJECT>/state.md` matches the workspace's type-checking tool.
- The workspace's type-checking tool runs cleanly or known issues are documented in `state.md`.
- Tests pass via the workspace's tooling.
