---
name: polylith-migrate-update-tests
description: "[Internal sub-skill of `polylith-migrate-orchestrator`. Do not load directly — load `polylith-migrate-orchestrator` first, which drives all phases.] Update test files to import from the compatibility shim or the new namespace, ensuring test stability after namespace migration."
---

# Skill: polylith-migrate-update-tests

> ⛓ **Conditional phase (4b).** Runs **only when `SHIM_STRATEGY=shim`** (chosen in `polylith-migrate-analyze-imports`), to point test imports at the compatibility shim. On the **shimless** path this phase is **skipped** — test imports are rewritten to the new namespace as part of `polylith-migrate-automate-import-updates` (phase 4). (Physical test relocation to the workspace happens later in `polylith-migrate-prepare-project` / `polylith-migrate-refactor-tests`, regardless of strategy.) See the `polylith-migrate-orchestrator` workflow.

## Goal
Update test files to import from the compatibility shim or the new namespace, ensuring that tests remain functional after the namespace migration.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- Import analysis report (from `migration/<project-name>/import_analysis.md`)

## Steps

### 1. Identify test files importing from the original namespace
1. Review the import analysis report to identify test files (typically in `projects/${PROJECT}/tests/`) that import from the original namespace.

### 2. Update imports in test files
The compatibility shim re-exports the original namespace's public symbols at the
**top level** of `${ORIG_TOP_NS}` (from `projects/${PROJECT}/${ORIG_TOP_NS}/__init__.py`).
So test imports keep the `${ORIG_TOP_NS}` prefix — only **submodule-qualified** imports
need collapsing onto that top-level surface:

1. For each test file importing from the original namespace:
   - Collapse submodule-qualified imports onto the shim: rewrite
     `from ${ORIG_TOP_NS}.<submodule> import <symbol>` to `from ${ORIG_TOP_NS} import <symbol>`
     (the symbol is re-exported by the shim).
   - Leave top-level imports (`from ${ORIG_TOP_NS} import <symbol>`, `import ${ORIG_TOP_NS}`)
     unchanged — they already resolve through the shim.
   - If a symbol is **not** re-exported by the shim, either add it to the shim's `__all__`
     (see `polylith-migrate-generate-shim`) or import it from its new namespace path directly.

Example:
```python
# Before
from myproject.core import MyClass

# After (using the compatibility shim)
from myproject import MyClass
```

### 3. Verify test discovery
1. Run test discovery to ensure the test count matches the baseline from `migration/${PROJECT}/state.md`.
2. Record any discrepancies in `migration/${PROJECT}/test_updates.md`.

### 4. Record updated test files
1. Record all updated test files in `migration/${PROJECT}/test_updates.md`.

## Output
- Updated test files
- A report file: `migration/<project-name>/test_updates.md` listing all updated test files

## Verify
1. Confirm that all test files listed in `migration/<project-name>/test_updates.md` have been updated.
2. Verify that test discovery produces the expected number of tests (as recorded in `migration/<project-name>/state.md`).
3. Ensure that a representative subset of tests passes by running the test command from `migration/<project-name>/state.md`.

## Commit
```bash
git add projects/${PROJECT}/tests/
git add migration/${PROJECT}/test_updates.md
git commit -m "migrate(${PROJECT}): phase <N> — update-tests"
```
> `<N>` is this phase's number from the `polylith-migrate-orchestrator` table (the single source of truth) — do not hardcode it.