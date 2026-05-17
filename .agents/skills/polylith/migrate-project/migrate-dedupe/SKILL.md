---
name: migrate-dedupe
description: "[Internal sub-skill of `migrate-orchestrator` (optional, runs only when opted in during phase 1). Do not load directly — load `migrate-orchestrator` first.] Identify and execute controlled deduplication of code during migration (if the user opts in)."
---

# Skill: migrate-dedupe

> 📐 **Scope vs sibling skills.** This skill is **opportunistic deduplication** that may be triggered any time during refactoring when duplication candidates surface. It is **not** the canonical place for the structural decompositions:
> - For "split this big component into smaller ones", use `migrate-split-big-component` (it already includes a dedup-analysis subsection — usually sufficient on a first migration).
> - For "this component's `core.py` mixes domains", use `migrate-split-component-internals`.
> - For "two projects have overlapping code, split shared from project-specific", use `migrate-isolate-shared-and-project-logic`.
>
> Use `migrate-dedupe` when none of the above fits cleanly — e.g., duplication discovered across already-extracted components that don't map to a structural split.

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