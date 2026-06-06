---
name: migrate-verify-stability
description: Verify that the migration did not break the project by running test discovery, checking for circular imports, and ensuring the compatibility shim covers all necessary symbols.
---

# Skill: migrate-verify-stability

## Goal
Verify that the migration did not break the project by:
1. Running test discovery and comparing the test count with the baseline
2. Checking for circular imports
3. Ensuring the compatibility shim covers all necessary symbols

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Test command (from `migration/<project-name>/state.md`)
- Baseline test count (from `migration/<project-name>/state.md`)

## Steps

### 1. Run test discovery
1. Run the test discovery command from `migration/${PROJECT}/state.md`.
2. Compare the test count with the baseline from `migration/${PROJECT}/state.md`.
3. Record any discrepancies in `migration/${PROJECT}/stability_report.md`.

### 2. Run a subset of tests
1. Run a representative subset of tests using the test command from `migration/${PROJECT}/state.md`.
2. Record any test failures in `migration/${PROJECT}/stability_report.md`.

### 3. Check for circular imports
1. Verify that no circular imports remain by reviewing `migration/${PROJECT}/circular_imports_resolved.md`.
2. Record any remaining circular imports in `migration/${PROJECT}/stability_report.md`.

### 4. Verify shim coverage
1. Ensure the compatibility shim (`projects/${PROJECT}/${ORIG_TOP_NS}/__init__.py`) covers all necessary symbols by comparing it with the original namespace's exports.
2. Record any missing symbols in `migration/${PROJECT}/stability_report.md`.

## Output
- A report file: `migration/<project-name>/stability_report.md` summarizing:
  - Test count before and after migration
  - Test failures (if any)
  - Circular import status
  - Shim coverage status

## Verify
1. Confirm that `migration/<project-name>/stability_report.md` exists and is not empty.
2. Verify that:
   - The test count matches the baseline
   - No test failures are reported
   - No circular imports remain
   - The shim covers all necessary symbols

## Commit
```bash
git add migration/${PROJECT}/stability_report.md
git commit -m "migrate(${PROJECT}): phase <N> — verify-stability"
```
> `<N>` is this phase's number from the `migrate-orchestrator` table (the single source of truth) — do not hardcode it.