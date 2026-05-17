---
name: orchestrator
description: Orchestrates the project migration workflow. **Explicitly invoke this skill to migrate a non-Polylith project in `/projects`.**
---

# Skill: orchestrator

## Goal
Define and execute the workflow for migrating a non-Polylith Python project to a Polylith workspace.
**This skill must be explicitly invoked by a human with the project name/path.**

## Usage
To migrate a project, load the `migrate.orchestrator` skill and provide the project name (e.g., the subdirectory in `/projects`):
```
Load the `migrate.orchestrator` skill and specify the project name (e.g., `my-app`).
```

## Steps

### 1. User Confirmation
- Immediately ask the user to confirm the project path and migration intent:
  ```
  You are about to migrate `/projects/my-app` to Polylith. This will refactor the project into bases and components. Proceed? (yes/no)
  ```
- If the user declines, abort the migration:
  ```
  Migration aborted by user.
  ```

### 2. Execute Migration Workflow
- Proceed with the migration steps (discover, extract, refactor, etc.) if the user confirms.
- Use the project path provided by the user (e.g., `/projects/my-app`) for all operations.

## Workflow
The migration process consists of the following steps, executed in this order:

1. **Discover**: Inspect the project and create `state.md` and `manifest.md`.
   - Skill: `discover`
   - Dependencies: None

2. **Extract to Base**: Extract application code into a temporary migration base.
   - Skill: `extract-to-base`
   - Dependencies: `discover`

3. **Prepare Project**: Clean up the project subfolder and consolidate dependencies.
   - Skill: `prepare-project`
   - Dependencies: `extract-to-base`

4. **Isolate Base and Big Component**: Shrink the temporary migration base into thin bases and a big component.
   - Skill: `isolate-base-and-big-component`
   - Dependencies: `prepare-project`

5. **Split Big Component**: Split the big component into multiple focused components.
   - Skill: `split-big-component`
   - Dependencies: `isolate-base-and-big-component`

6. **Extract Standalone Modules**: Extract zero-dependency and low-dependency modules into standalone components.
   - Skill: `extract-standalone-modules`
   - Dependencies: `split-big-component`

7. **Isolate Shared and Project Logic**: Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`).
   - Skill: `isolate-shared-and-project-logic`
   - Dependencies: `extract-standalone-modules`, `split-big-component`

8. **Distribute Wiring**: Distribute app-wiring code from the residual component into the appropriate bases and shared components.
   - Skill: `distribute-wiring`
   - Dependencies: `isolate-shared-and-project-logic`

9. **Split Component Internals**: Split monolithic `core.py` files in shared components into domain-focused modules.
   - Skill: `split-component-internals`
   - Dependencies: `distribute-wiring`

10. **Refactor Tests**: Restructure unit tests to align with the workspace's Polylith theme.
    - Skill: `refactor-tests`
    - Dependencies: `split-component-internals`

11. **Definition of Done**: Verify that all migration criteria are met.
    - Skill: `definition-of-done`
    - Dependencies: `refactor-tests`

## Optional Skills

- **Convert Linter**: Replace the project's linter with `ruff` (if the user opts in during the `discover` step).
  - Skill: `convert-linter`
  - Dependencies: `discover`
  - Trigger: User opts in during `discover` step.

- **Convert Type Checker**: Replace the project's type checker with `ty` (if the user opts in during the `discover` step).
  - Skill: `convert-type-checker`
  - Dependencies: `discover`
  - Trigger: User opts in during `discover` step.

- **Convert Package Manager**: Convert the project's `pyproject.toml` to PEP 621/uv format and register it as a workspace member (if the user opts in during the `discover` step).
  - Skill: `convert-package-manager`
  - Dependencies: `discover`
  - Trigger: User opts in during `discover` step.

- **Dedupe**: Identify and execute controlled deduplication of code during migration (if the user opts in).
  - Skill: `dedupe`
  - Dependencies: `split-big-component`, `extract-standalone-modules`

## Workflow
The migration process consists of the following steps, executed in this order:

1. **Discover**: Inspect the project and create `state.md` and `manifest.md`.
   - Skill: `discover`
   - Dependencies: None

2. **Extract to Base**: Extract application code into a temporary migration base.
   - Skill: `extract-to-base`
   - Dependencies: `discover`

3. **Prepare Project**: Clean up the project subfolder and consolidate dependencies.
   - Skill: `prepare-project`
   - Dependencies: `extract-to-base`

4. **Isolate Base and Big Component**: Shrink the temporary migration base into thin bases and a big component.
   - Skill: `isolate-base-and-big-component`
   - Dependencies: `prepare-project`

5. **Split Big Component**: Split the big component into multiple focused components.
   - Skill: `split-big-component`
   - Dependencies: `isolate-base-and-big-component`

9. **Extract Standalone Modules**: Extract zero-dependency and low-dependency modules into standalone components.
    - Skill: `extract-standalone-modules`
    - Dependencies: `split-big-component`

10. **Isolate Shared and Project Logic**: Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`).
    - Skill: `isolate-shared-and-project-logic`
    - Dependencies: `extract-standalone-modules`, `split-big-component`

11. **Split Component Internals**: Split monolithic `core.py` files in shared components into domain-focused modules.
    - Skill: `split-component-internals`
    - Dependencies: `distribute-wiring`

12. **Refactor Tests**: Restructure unit tests to align with the workspace's Polylith theme.
    - Skill: `refactor-tests`
    - Dependencies: `split-component-internals`

13. **Definition of Done**: Verify that all migration criteria are met.
    - Skill: `definition-of-done`
    - Dependencies: `refactor-tests`

## Optional Skills

- **Convert Linter**: Replace the project's linter with `ruff` (if the user opts in during the `discover` step).
  - Skill: `convert-linter`
  - Dependencies: `discover`
  - Trigger: User opts in during `discover` step (`CONVERT_LINTER=yes` in `state.md`).

- **Convert Type Checker**: Replace the project's type checker with `ty` (if the user opts in during the `discover` step).
  - Skill: `convert-type-checker`
  - Dependencies: `discover`
  - Trigger: User opts in during `discover` step (`CONVERT_TYPE_CHECKER=yes` in `state.md`).

- **Convert Package Manager**: Convert the project's `pyproject.toml` to PEP 621/uv format and register it as a workspace member (if the user opts in during the `discover` step).
  - Skill: `convert-package-manager`
  - Dependencies: `discover`
  - Trigger: User opts in during `discover` step (`CONVERT_PACKAGE_MANAGER=yes` in `state.md`).

- **Dedupe**: Identify and execute controlled deduplication of code during migration (if the user opts in).
  - Skill: `dedupe`
  - Dependencies: `split-big-component`, `extract-standalone-modules`

## Execution
To execute the migration workflow:
1. Load the `orchestrator` skill.
2. Follow the steps defined in the workflow, ensuring all dependencies are satisfied before executing each skill.
3. Verify the completion of each step before proceeding to the next.

## Validation
- Ensure no circular dependencies exist in the workflow.
- Verify that all dependencies are correctly declared and exist in the `SKILLS.md` index.
- Confirm that the workflow is executable in the order defined by the orchestrator skill.