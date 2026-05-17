---
name: migrate-split-component-internals
description: "[Internal sub-skill of `migrate-orchestrator` (phase 9 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Split monolithic `core.py` files in shared components into domain-focused modules."
---

# Skill: migrate-split-component-internals

> 📐 **Scope vs sibling skills.** This skill operates **inside one already-extracted component**, splitting its `core.py` into multiple sibling Python files. **No new components are created** — only the internal file layout changes. Don't confuse with:
> - `migrate-split-big-component` — splits **one component into multiple components**. Use that when the unit being broken up is a component, not a file.
> - `migrate-isolate-shared-and-project-logic` — separates shared vs project-specific code **across components and projects**; may create new components.
> - `migrate-extract-standalone-modules` — pulls foundational modules out of the residual big component into new standalone components.

## Goal
Split monolithic `core.py` files in **shared components** (e.g., `models_shared`, `schemas_shared`, or similar) into domain-focused modules. This skill ensures that shared components remain well-organized and maintainable.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Current component list and structure.

## Steps

### 1. Identify Candidates
- Scan components for large `core.py` files.
- A component is a candidate if:
  - The file contains definitions from multiple domains.
  - The file contains helper/utility functions alongside class definitions.
  - The file exceeds a reasonable size threshold.

### 2. Group Definitions by Domain
- Group definitions by the domain concept they serve.
- Example domains: ORM models, schema/dataclass clusters, helper functions.

### 3. Create New Modules
- Create domain-focused modules (e.g., `merchant.py`, `transaction.py`).
- Move relevant definitions from `core.py` to the new modules.

### 4. Update `__init__.py`
- Re-export public names from the new modules in `__init__.py`.

### 5. Handle `core.py`
- Delete `core.py` if all definitions have been moved.
- Keep `core.py` if it serves as a composition point.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.