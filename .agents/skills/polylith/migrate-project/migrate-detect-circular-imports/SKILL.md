---
name: migrate-detect-circular-imports
description: Detect and report circular imports introduced by the namespace migration.
---

# Skill: migrate-detect-circular-imports

> ⛓ **Conditional phase (4b).** Runs **only when `SHIM_STRATEGY=shim`** (chosen in `migrate-analyze-imports`). On the **shimless** path this phase is **skipped** — a pure namespace rename introduces no base↔shim cycles. See the `migrate-orchestrator` workflow.

## Goal
Detect and report circular imports introduced by the namespace migration, particularly between the new base location and the compatibility shim.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- New namespace (from `migration/<project-name>/state.md`)
- Import updates report (from `migration/<project-name>/import_updates.md`)

## Steps

### 1. Analyze the import graph
1. Manually inspect the import graph to identify circular dependencies:
   - Between the new base location (`bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/`) and the compatibility shim (`projects/${PROJECT}/${ORIG_TOP_NS}/__init__.py`)
   - Within the new base location itself

### 2. Report circular imports
1. Record all circular import chains in `migration/${PROJECT}/circular_imports.md`.
2. For each circular import chain, document:
   - The files involved (use full paths like `bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/module.py`)
   - The import statements causing the circularity
   - Suggested resolution steps

## Output
- A report file: `migration/<project-name>/circular_imports.md` listing all circular import chains

## Verify
1. Confirm that `migration/<project-name>/circular_imports.md` exists.
2. Verify that the report includes:
   - A list of circular import chains
   - The files involved in each chain
   - Suggested resolution steps

## Commit
```bash
git add migration/${PROJECT}/circular_imports.md
git commit -m "migrate(${PROJECT}): phase <N> — detect-circular-imports"
```
> `<N>` is this phase's number from the `migrate-orchestrator` table (the single source of truth) — do not hardcode it.