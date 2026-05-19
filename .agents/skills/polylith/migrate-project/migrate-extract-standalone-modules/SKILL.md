---
name: migrate-extract-standalone-modules
description: "[Internal sub-skill of `migrate-orchestrator` (phase 6 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Extract foundational modules (e.g., `consts.py`, `exceptions.py`, or similar) from the residual component into standalone components."
---

# Skill: migrate-extract-standalone-modules

## Goal
Extract **foundational modules** (e.g., `consts.py`, `exceptions.py`, `models.py`) from the residual component into standalone components. This skill is for zero-dependency or low-dependency modules that serve as building blocks for other components.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `INITIAL_BASE_NAME`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Current module map, including what remains in the residual component.

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

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

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| Module classified as zero-dep actually pulls in a transitive runtime dependency (e.g., reads an env var via the residual's config module) | The classification missed an indirect import. | Reclassify as low-dep, extract the config module first, then retry. |
| Two consumers now import the same constant via different paths (e.g., `from <ns>.consts` and `from <ns>.<INITIAL_BASE_NAME>.consts`) | The original module wasn't deleted from the residual after extraction. | Delete the original from the residual (step 3.6), pick one canonical import path, and update every caller. Verify with `grep -r '<ns>.<INITIAL_BASE_NAME>.consts'`. |
| Extracting `exceptions.py` causes `except` clauses elsewhere to stop catching what they used to | Exception classes are identity-based: two definitions are two different classes. | Ensure the new standalone module is the **only** definition. Delete the residual copy and update every `raise`/`except` site. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase 6 — extract-standalone-modules"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.