---
name: polylith-migrate-resolve-circular-imports
description: "[Internal sub-skill of `polylith-migrate-orchestrator`. Do not load directly — load `polylith-migrate-orchestrator` first, which drives all phases.] Resolve circular imports by updating imports in the new base location to avoid referencing the compatibility shim."
---

# Skill: polylith-migrate-resolve-circular-imports

> ⛓ **Conditional phase (4b).** Runs **only when `SHIM_STRATEGY=shim`** (chosen in `polylith-migrate-analyze-imports`) and only if `polylith-migrate-detect-circular-imports` found cycles. **Skipped** on the shimless path. See the `polylith-migrate-orchestrator` workflow.

## Goal
Resolve circular imports by updating imports in the new base location to avoid referencing the compatibility shim, ensuring a clean dependency graph.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- New namespace (from `migration/<project-name>/state.md`)
- Circular imports report (from `migration/<project-name>/circular_imports.md`)

## Steps

### 1. Review the circular imports report
1. Review the circular imports report to identify all circular import chains.

### 2. Resolve circular imports
1. For each circular import chain:
   - Update imports in the new base location (`bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/`) to avoid referencing the compatibility shim
   - Use direct imports from the new namespace instead
   - Consider using forward references or dependency injection where necessary

Example:
```python
# Before (circular import with shim)
from myproject.core import MyClass

# After (direct import from new namespace)
from mynamespace.mybase.core import MyClass
```

### 3. Record resolved circular imports
1. Record all resolved circular imports in `migration/${PROJECT}/circular_imports_resolved.md`.

## Output
- Updated files in the new base location
- A report file: `migration/<project-name>/circular_imports_resolved.md` listing resolved circular imports

## Verify
1. Confirm that all circular imports listed in `migration/<project-name>/circular_imports.md` have been resolved.
2. Verify that no circular imports remain by re-running the circular import detection.
3. Ensure the codebase remains functional by running the test command from `migration/<project-name>/state.md`.

## Commit
```bash
git add bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/
git add migration/${PROJECT}/circular_imports_resolved.md
git commit -m "migrate(${PROJECT}): phase <N> — resolve-circular-imports"
```
> `<N>` is this phase's number from the `polylith-migrate-orchestrator` table (the single source of truth) — do not hardcode it.