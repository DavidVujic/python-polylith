---
name: dedupe
description: Identify and execute controlled deduplication of code during migration (if the user opts in).
---

# Skill: dedupe

## Goal
Identify duplication candidates during the migration process and execute controlled deduplication for user-approved candidates.

## When to Use
- After splitting the big component or extracting standalone modules.
- When potential duplication between components is suspected.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- Verification commands (`RUN_TEST_CMD`, `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`).

From `migration/<PROJECT>/manifest.md`:
- Module map of components.

## Steps

### 1. Identify Duplication Candidates
- Use `directory_tree` and `grep` to scan for overlapping logic between components.
- Classify candidates by type:
  - **Identical**: Code that is exactly the same.
  - **Similar**: Code that serves the same purpose but with minor differences.
  - **Coincidental**: Code that looks similar but serves unrelated purposes.

### 2. Present Candidates to the User
- Provide a list of duplication candidates, including:
  - Component names.
  - File paths.
  - Type of duplication (identical, similar, coincidental).
  - Risk assessment (low, medium, high).
- Ask the user to approve or reject each candidate for deduplication.

### 3. Execute Deduplication for Approved Candidates
- For each approved candidate:
  - **Identical Code**: Extract the shared logic into a new component and update imports.
  - **Similar Code**: Refactor to use shared logic or parameterize differences.
  - **Coincidental Code**: Leave as-is.
- Update `pyproject.toml` to include any new components.
- Run `POLY_CMD_PREFIX sync` to synchronize the workspace.

### 4. Verify Changes
- Run `RUN_TEST_CMD` to ensure no regressions.
- Run `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` if set.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.

## Verify
- All tests pass (`RUN_TEST_CMD`).
- Linting and type-checking pass (if set).
- The workspace structure is valid (`POLY_CMD_PREFIX check`).

## Done When
- Duplication candidates are identified and presented to the user.
- User-approved candidates are deduplicated.
- All tests and checks pass.
- The workspace structure is valid.