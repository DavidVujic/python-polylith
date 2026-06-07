---
name: polylith-migrate-analyze-imports
description: "[Internal sub-skill of `polylith-migrate-orchestrator`. Do not load directly — load `polylith-migrate-orchestrator` first, which drives all phases.] Analyze the project's import graph to find how the original namespace is referenced, choose the namespace-rewrite strategy (shim vs shimless), detect circular imports, and list symbols exported by the original namespace."
---

# Skill: polylith-migrate-analyze-imports

## Goal
Analyze the project's import graph to:
1. Find **every** reference to the original namespace (in all three forms — see below).
2. Choose the namespace-rewrite strategy: `SHIM_STRATEGY=shim|shimless`.
3. List symbols exported by the original namespace's `__init__.py`.
4. Detect potential circular imports.

This drives the namespace rewrite (phase 4) and, when `SHIM_STRATEGY=shim`, the
shim sub-track (phase 4b). See the `polylith-migrate-orchestrator` table for phase numbers.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace `ORIG_TOP_NS` (from `migration/<project-name>/state.md`)

## The three reference forms (cover all of them)
A namespace rewrite is **incomplete** unless it covers every form below. A naive
"replace `from <ns>.` " misses forms 2 and 3:

1. **Dotted import** — `from ${ORIG_TOP_NS}.<sub> import …`, `import ${ORIG_TOP_NS}.<sub>`.
2. **Bare submodule import** — `from ${ORIG_TOP_NS} import <sub>` — single, multi-name
   (`a, b, c`), and **mixed** lines where only some names move. Easy to miss: there is
   no dot after the namespace.
3. **Quoted string module paths** — `mock.patch("${ORIG_TOP_NS}.x.Y")`, logging
   dict-config `"${ORIG_TOP_NS}.logging.HealthFilter"`, `importlib` / `getattr`
   targets. Not import statements, but they must be rewritten too.

> ⚠ Do **not** rewrite unquoted local variables that merely share a name with the
> namespace (e.g. a FastAPI `app = FastAPI()` instance's `app.include_router(...)`).
> Target import statements and quoted module paths only.

## Steps

### 1. Identify references to the original namespace
1. Search for all three forms above across **all** `.py` files in the project (and
   `pyproject.toml` / config files for string paths).
2. Record the paths and statements in `migration/${PROJECT}/import_analysis.md`,
   grouped as: **internal** (inside `${ORIG_TOP_NS}/`), **external consumers**
   (entrypoints, `alembic`, scripts), and **tests**. The external + test groups are
   what the strategy decision below hinges on.

### 2. List symbols exported by the original namespace
1. Inspect `${ORIG_TOP_NS}/__init__.py` (typically `projects/${PROJECT}/src/${ORIG_TOP_NS}/__init__.py`
   or `projects/${PROJECT}/${ORIG_TOP_NS}/__init__.py`) and list public symbols
   (not starting with `_`).
2. Record them, and **note whether `__init__.py` is effectively empty** (docstring only).

### 3. Decide the rewrite strategy (`SHIM_STRATEGY`)
Choose based on the findings and record it in `state.md`:

- **`shimless`** — when imports are predominantly **submodule-qualified**
  (`from ${ORIG_TOP_NS}.<sub> import …` / `from ${ORIG_TOP_NS} import <sub>`) and
  `${ORIG_TOP_NS}/__init__.py` exports little or nothing. A single top-level
  re-export shim would resolve **none** of those submodule paths, and a full package
  shim mirroring every module is high-effort/high-risk. Phase 4 rewrites **all**
  references (internal + external + tests) directly to the new namespace, and the
  **phase 4b sub-track is skipped**.
- **`shim`** — when consumers import top-level symbols (`from ${ORIG_TOP_NS} import X`)
  that a single `${ORIG_TOP_NS}/__init__.py` re-export can satisfy, and you want to
  defer rewriting external consumers. Run the phase 4b sub-track after phase 4.
- **When in doubt, prefer `shimless`** — it leaves no transitional shim to remove
  later (the definition-of-done forbids undocumented shims), at the cost of a wider
  but mechanical rewrite. Confirm with the user if the consumer surface is large.

Record:
```
SHIM_STRATEGY=<shim|shimless>
```

### 4. Detect potential circular imports
1. Inspect the import graph for cycles — especially base ↔ shim once a shim is in
   place (`shim` strategy only).
2. Record any chains in `import_analysis.md`. A pure namespace rename (shimless)
   preserves the original graph, so cycles there usually mean the project already had
   them.

## Output
- `migration/<project-name>/import_analysis.md` with: references by form & group,
  exported symbols, the chosen strategy + rationale, and circular-import chains (if any).
- `SHIM_STRATEGY` set in `migration/<project-name>/state.md`.

## Verify
1. `migration/<project-name>/import_analysis.md` exists and is not empty.
2. It records all three reference forms, the exported symbols, and any cycles.
3. `SHIM_STRATEGY` is set in `state.md` (`shim` or `shimless`) with a recorded rationale.

## Commit
```bash
git add migration/${PROJECT}/import_analysis.md migration/${PROJECT}/state.md
git commit -m "migrate(${PROJECT}): phase <N> — analyze-imports"
```
> `<N>` is this phase's number from the `polylith-migrate-orchestrator` table (the single
> source of truth) — do not hardcode it.
