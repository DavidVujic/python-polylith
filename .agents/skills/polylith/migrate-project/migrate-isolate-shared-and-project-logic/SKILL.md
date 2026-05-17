---
name: migrate-isolate-shared-and-project-logic
description: "[Internal sub-skill of `migrate-orchestrator` (phase 7 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`, or similar)."
---

# Skill: migrate-isolate-shared-and-project-logic

> 📐 **Scope vs sibling skills.** This skill is **cross-project**: it separates code used by **two or more projects** (shared) from code used by **a single project** (project-specific), potentially creating new shared *and* project-specific components. Don't confuse with:
> - `migrate-split-big-component` — within one project; splits one component into multiple components.
> - `migrate-split-component-internals` — within one component; splits one `core.py` into multiple files.
> - `migrate-dedupe` — opportunistic deduplication, broader than just shared-vs-project-specific.
>
> 💡 **When to skip this skill.** On the **first** project migration there is usually no second project to compare against. Skip this skill until at least one prior project has been migrated. The orchestrator still calls it after `migrate-extract-standalone-modules` — that's the right place when overlap exists.

## Goal
Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`). Extract shared logic into reusable components and isolate project-specific logic into project-specific components.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `INITIAL_BASE_NAME`
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