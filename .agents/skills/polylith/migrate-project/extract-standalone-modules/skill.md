---
name: extract-standalone-modules
description: Extract foundational modules (e.g., `consts.py`, `exceptions.py`) from the residual component into standalone components.
---

# Skill: extract-standalone-modules

## Goal
Extract **foundational modules** (e.g., `consts.py`, `exceptions.py`, `models.py`) from the residual component into standalone components. This skill is for zero-dependency or low-dependency modules that serve as building blocks for other components.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `BRICK_NAME`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Current module map, including what remains in the residual component.

## Steps

### 1. Analyze the Residual Component
- Use `directory_tree` and `grep` to list modules remaining in the residual component.
- Classify each module:
  - **Zero internal deps**: Modules with only stdlib/third-party imports (e.g., `exceptions.py`, `consts.py`).
  - **Low internal deps**: Modules that depend on already extracted or zero-dep modules (e.g., `models.py`).
  - **App-wiring**: Modules that compose infrastructure setup. These stay in the residual.

### 2. Extract Modules in Dependency Order
- Extract zero-dep modules first, followed by modules that depend on them.

### 3. For Each Extraction
1. Check for naming collisions.
2. Create the component directory with `__init__.py` and `core.py`.
3. Update imports in all consumers.
4. Add the new brick to `pyproject.toml`.
5. Run verification.
6. Delete the original module from the residual component.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX sync` to synchronize the `[tool.polylith.bricks]` table with actual imports.