---
name: migrate-generate-shim
description: Generate a compatibility shim that re-exports all symbols from the new base location to maintain backward compatibility during namespace migration.
---

# Skill: migrate-generate-shim

## Goal
Generate a compatibility shim (`projects/<project-name>/<original_namespace>/__init__.py`) that re-exports all symbols from the new base location to maintain backward compatibility during namespace migration.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- New namespace (from `migration/<project-name>/state.md`)
- Import analysis report (from `migration/<project-name>/import_analysis.md`)

## Steps

### 1. List symbols exported by the new base location
1. Inspect the new base location's `__init__.py` (at `bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/__init__.py`) to list all public symbols.
2. Compare with the symbols exported by the original namespace from the import analysis report.

### 2. Generate the shim
1. Create a shim file at `projects/${PROJECT}/${ORIG_TOP_NS}/__init__.py`.
2. Add re-export statements for all symbols from the new base location using `from ${TARGET_TOP_NS}.${INITIAL_BASE_NAME}.<module> import <symbol>`.
3. Include an `__all__` list with all re-exported symbols.

Example shim content:
```python
# Compatibility shim for the migration from `${ORIG_TOP_NS}` to `${TARGET_TOP_NS}.${INITIAL_BASE_NAME}`.
# This module re-exports all public symbols from the new base location.

from ${TARGET_TOP_NS}.${INITIAL_BASE_NAME}.core import MyClass
from ${TARGET_TOP_NS}.${INITIAL_BASE_NAME}.utils import my_function

__all__ = [
    "MyClass",
    "my_function",
]
```

### 3. Verify the shim
1. Ensure the shim's `__all__` includes all symbols exported by the new base location.
2. Record any missing symbols in `migration/${PROJECT}/shim_report.md`.

## Output
- A shim file: `projects/<project-name>/<original_namespace>/__init__.py`
- A report file: `migration/<project-name>/shim_report.md` listing all re-exported symbols

## Verify
1. Confirm that `projects/<project-name>/<original_namespace>/__init__.py` exists and is not empty.
2. Verify that `migration/<project-name>/shim_report.md` exists and lists all re-exported symbols.
3. Ensure the shim's `__all__` includes all symbols exported by the new base location.

## Commit
```bash
git add projects/${PROJECT}/${ORIG_TOP_NS}/__init__.py
git add migration/${PROJECT}/shim_report.md
git commit -m "migrate(${PROJECT}): phase 3 — generate-shim"
```