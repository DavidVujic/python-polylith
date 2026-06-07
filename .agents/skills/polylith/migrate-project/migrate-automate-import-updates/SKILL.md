---
name: migrate-automate-import-updates
description: "[Internal sub-skill of `migrate-orchestrator`. Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Update imports in the new base location to reference the new namespace instead of the original namespace."
---

# Skill: migrate-automate-import-updates

## Goal
Update imports to reference the new namespace instead of the original namespace, ensuring that the codebase remains functional after the namespace migration.

> **Scope depends on `SHIM_STRATEGY`** (set by `migrate-analyze-imports`):
> - `shim`: rewrite imports **in the new base location only** — external consumers keep
>   using the original namespace via the shim (phase 4b).
> - `shimless`: rewrite **every** reference to the original namespace — base internals,
>   entrypoints / run-scripts, infra (e.g. `alembic/env.py`), and tests — so nothing
>   imports the old namespace and no shim is needed.
>
> Cover **all three reference forms** (see `migrate-analyze-imports`): dotted
> `from <ns>.<sub> import …`, bare-submodule `from <ns> import <sub>` (incl. multi-name
> and **mixed** lines), and quoted string paths (`mock.patch("<ns>.x.Y")`, logging
> dict-config). A naive "`from <ns>.`" replace silently misses the bare and quoted forms.
>
> 💡 **Script the rewrite for anything non-trivial.** A small text-in → text-out helper
> (a pure function: file text + an `{old → new}` mapping → rewritten text) handles all
> three forms — including splitting a mixed bare-import line into moved vs. not-moved
> names — far more reliably than ad-hoc edits across dozens of files. Keep it as plain
> functions (no classes), run it over `bases/`, `components/`, `test/`, and the project
> dir, then verify by grepping for any residual `<ns>` reference. The same helper is
> reusable for the component-extraction rewrites in `migrate-split-big-component`.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)
- New namespace (from `migration/<project-name>/state.md`)
- Import analysis report (from `migration/<project-name>/import_analysis.md`)

## Steps

### 1. Identify files in the new base location importing from the original namespace
1. Review the import analysis report to identify files in the new base location (at `bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/`) that import from the original namespace.

### 2. Update imports to reference the new namespace
1. For each file in the new base location that imports from the original namespace:
   - Replace `from ${ORIG_TOP_NS} import ...` with `from ${TARGET_TOP_NS}.${INITIAL_BASE_NAME}.<module> import ...`
   - Replace `import ${ORIG_TOP_NS}` with `import ${TARGET_TOP_NS}.${INITIAL_BASE_NAME}`

Example:
```python
# Before
from myproject.core import MyClass
import myproject.utils

# After
from mynamespace.mybase.core import MyClass
import mynamespace.mybase.utils
```

### 3. Record updated files
1. Record all updated files in `migration/${PROJECT}/import_updates.md`.

## Output
- Updated files in the new base location
- A report file: `migration/<project-name>/import_updates.md` listing all updated files

## Verify
1. Confirm that all files listed in `migration/<project-name>/import_updates.md` have been updated.
2. Check that no files in the new base location import from the original namespace.
3. Verify that the codebase remains functional by running the test command from `migration/<project-name>/state.md`.

## Commit
```bash
git add bases/${TARGET_TOP_NS}/${INITIAL_BASE_NAME}/
git add migration/${PROJECT}/import_updates.md
git commit -m "migrate(${PROJECT}): phase <N> — automate-import-updates"
```
> `<N>` is this phase's number from the `migrate-orchestrator` table (the single source of truth) — do not hardcode it.