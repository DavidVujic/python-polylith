---
name: isolate-shared-and-project-logic
description: Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`).
---

# Skill: isolate-shared-and-project-logic

## Goal
Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`). Extract shared logic into reusable components and isolate project-specific logic into project-specific components.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `BRICK_NAME`
- Verification commands (`RUN_TEST_CMD`, `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`).

From `migration/<PROJECT>/manifest.md`:
- Module map of components.

## Steps

### 1. Identify Monolithic Components
- Scan the workspace for monolithic components (e.g., `models`, `schemas`).
- Focus on components with large `core.py` files or mixed domain logic.

### 2. Analyze Usage
- Use `grep` to trace imports of each definition in the component.
- Classify definitions as:
  - **Shared**: Used by multiple projects.
  - **Project-Specific**: Used by only one or a few projects.
  - **Similar**: Definitions that could reuse shared logic (e.g., similar models).

### 3. Extract Shared Logic
- Create a new shared component (e.g., `models_shared`, `schemas_shared`).
- Move shared definitions into the new component.
- Update imports in all projects to reference the shared component.

### 4. Isolate Project-Specific Logic
- Create project-specific components (e.g., `models_project_a`, `schemas_project_b`).
- Move project-specific definitions into the appropriate component.
- Update imports in the relevant projects.

### 5. Refactor Similar Models
- For similar models, extract shared logic into the shared component.
- Update the project-specific models to reuse the shared logic.

### 6. Update `pyproject.toml`
- Add the new shared and project-specific components to the workspace's `pyproject.toml`.
- Update the project's `pyproject.toml` to reference the new components.

### 7. Verify Changes
- Run `RUN_TEST_CMD` to ensure no regressions.
- Run `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` if set.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.

## Verify
- All tests pass (`RUN_TEST_CMD`).
- Linting and type-checking pass (if set).
- The workspace structure is valid (`POLY_CMD_PREFIX check`).

## Done When
- Shared logic is extracted into reusable components.
- Project-specific logic is isolated into project-specific components.
- Similar models reuse shared logic where possible.
- All tests and checks pass.
- The workspace structure is valid.