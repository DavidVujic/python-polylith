---
name: migrate-update-tests
description: Update test files to import from the compatibility shim or the new namespace, ensuring test stability after namespace migration.
---

# Skill: migrate-update-tests

## Goal
Update test files to import from the compatibility shim or the new namespace, ensuring that tests remain functional after the namespace migration.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- Import analysis report (from `migration/<project-name>/import_analysis.md`)

## Steps

### 1. Identify test files importing from the original namespace
1. Review the import analysis report to identify test files that import from the original namespace.

### 2. Update imports in test files
1. For each test file importing from the original namespace:
   - Replace `from <original_namespace> import ...` with `from <original_namespace> import ...` (using the compatibility shim)
   - Replace `import <original_namespace>` with `import <original_namespace>` (using the compatibility shim)

Example:
```python
# Before
from myproject.core import MyClass

# After (using the compatibility shim)
from myproject import MyClass
```

### 3. Verify test discovery
1. Run test discovery to ensure the test count matches the baseline from `migration/<project-name>/state.md`.
2. Record any discrepancies in `migration/<project-name>/test_updates.md`.

### 4. Record updated test files
1. Record all updated test files in `migration/<project-name>/test_updates.md`.

## Output
- Updated test files
- A report file: `migration/<project-name>/test_updates.md` listing all updated test files

## Verify
1. Confirm that all test files listed in `migration/<project-name>/test_updates.md` have been updated.
2. Verify that test discovery produces the expected number of tests (as recorded in `migration/<project-name>/state.md`).
3. Ensure that a representative subset of tests passes by running the test command from `migration/<project-name>/state.md`.

## Commit
```bash
git add projects/<project-name>/tests/ migration/<project-name>/test_updates.md
git commit -m "migrate(<project-name>): phase 8 — update-tests"
```