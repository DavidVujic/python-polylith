---
name: refactor-tests
description: Restructure unit tests to align with the workspace's Polylith theme.
---

# Skill: refactor-tests

## Goal
Restructure unit tests to align with the workspace's Polylith theme. The test directory structure should follow the workspace's conventions for organizing tests.

## Scope
- **Unit tests only**: Integration tests typically stay in a shared location (e.g., `test/integration/` or `test/<project>/integration/`).
- **Structure only**: Reorganize test files and update imports/mocks to align with the workspace's Polylith theme.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- List of all bricks (bases and components) with their module maps.

From `test/`:
- Current test directory structure.

## Steps

### 1. Classify Test Files
- Scan import statements and mock patch strings to determine which brick each test file primarily tests.
- Produce a classification table (e.g., `test_merchant_handler.py` → `app`).

### 2. Reorganize Tests
- Create target directories according to the workspace's Polylith theme.
- Move each test file to its brick's test directory.
- Handle `conftest.py` files:
  - Move brick-specific fixtures to the brick's test directory.
  - Move shared fixtures to `test/<TARGET_TOP_NS>/conftest.py` or `test/conftest.py`.

### 3. Update Imports and Mocks
- Update imports in test files if they reference other test modules or fixtures.
- Update mock patch strings if paths changed.

### 4. Verify
- Update `RUN_TEST_CMD` in `migration/<PROJECT>/state.md` to point to the new test root.
- Run `RUN_TEST_CMD` and `RUN_LINT_CMD`.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` succeeds.