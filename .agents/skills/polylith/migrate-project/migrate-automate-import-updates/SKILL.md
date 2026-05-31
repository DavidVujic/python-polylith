---
name: migrate-automate-import-updates
description: Update imports in the new base location to reference the new namespace instead of the original namespace.
---

# Skill: migrate-automate-import-updates

## Goal
Update imports in the new base location to reference the new namespace instead of the original namespace, ensuring that the codebase remains functional after the namespace migration.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- New namespace (from `migration/<project-name>/state.md`)
- Import analysis report (from `migration/<project-name>/import_analysis.md`)

## Steps

### 1. Identify files in the new base location importing from the original namespace
1. Review the import analysis report to identify files in the new base location that import from the original namespace.

### 2. Update imports to reference the new namespace
1. For each file in the new base location that imports from the original namespace:
   - Replace `from <original_namespace> import ...` with `from <new_namespace>.<module> import ...`
   - Replace `import <original_namespace>` with `import <new_namespace>`

Example:
```python
# Before
from myproject.core import MyClass
import myproject.utils

# After
from mynamespace.core import MyClass
import mynamespace.utils
```

### 3. Record updated files
1. Record all updated files in `migration/<project-name>/import_updates.md`.

## Output
- Updated files in the new base location
- A report file: `migration/<project-name>/import_updates.md` listing all updated files

## Verify
1. Confirm that all files listed in `migration/<project-name>/import_updates.md` have been updated.
2. Check that no files in the new base location import from the original namespace.
3. Verify that the codebase remains functional by running the test command from `migration/<project-name>/state.md`.

## Commit
```bash
git add bases/<new_namespace>/ migration/<project-name>/import_updates.md
git commit -m "migrate(<project-name>): phase 5 — automate-import-updates"
```
