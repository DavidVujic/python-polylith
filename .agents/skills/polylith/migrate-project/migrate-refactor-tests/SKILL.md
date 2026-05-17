---
name: migrate-refactor-tests
description: "[Internal sub-skill of `migrate-orchestrator` (phase 10 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Restructure unit tests to align with the workspace's Polylith theme."
---

# Skill: migrate-refactor-tests

## Goal
Restructure unit tests so they live next to the brick they test, following the workspace's Polylith theme (`loose` or `tdd`).

## Scope
- **Unit tests only.** Integration tests typically stay in a shared location (e.g., `test/integration/` or `test/<project>/integration/`). Do not redistribute them across bricks.
- **Structure only.** Reorganize test files and update imports/mock patch strings. Do not rewrite test logic or fixtures unless an import/path change makes it strictly necessary.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `RUN_TEST_CMD` (will be updated by this skill)
- `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD` (optional)

From `migration/<PROJECT>/manifest.md`:
- List of all bricks (bases and components) with their module maps.

From `workspace.toml`:
- `[tool.polylith.structure].theme` (`loose` or `tdd`).

From `test/`:
- Current test directory structure.

## Target layout

| Theme    | Test path for a base   | Test path for a component  |
|----------|------------------------|-----------------------------|
| `loose`  | `test/bases/<TARGET_TOP_NS>/<base>/test_*.py` | `test/components/<TARGET_TOP_NS>/<component>/test_*.py` |
| `tdd`    | `bases/<base>/test/<TARGET_TOP_NS>/<base>/test_*.py` | `components/<component>/test/<TARGET_TOP_NS>/<component>/test_*.py` |

## Steps

### 1. Classify each unit test file
For each `test_*.py` under the current test root:
1. Read its `import` statements and `mock.patch("...")` strings.
2. Identify the *primary* brick under test — usually the one most imported or the one mock-patched. Tie-break by file name (`test_user_handler.py` → `<user_handler base or component>`).
3. Record the classification in a table you keep in scratch (do **not** commit a separate file for this — it's transient):

| Test file | Primary brick | Target path |
|-----------|---------------|-------------|

If a test exercises 2+ bricks at integration level, classify it as integration and move it to `test/integration/` instead.

### 2. Move test files
- Create the target directories per the theme matrix above.
- Move each `test_*.py` to its brick's test directory.
- For each `conftest.py`:
  - **Brick-scoped fixtures** (referenced only by tests under one brick) → move to that brick's test directory.
  - **Workspace-shared fixtures** (cross-brick) → keep one `test/<TARGET_TOP_NS>/conftest.py` or `test/conftest.py`.

### 3. Update imports and mock patch strings
- Update any `from tests.<x>` imports that survived to the new layout.
- Update `mock.patch("<old.path>")` strings. Brick reshuffling earlier in the migration may have changed where the patched symbol now lives — use `grep` to locate the target symbol's new path and align the patch string. Patching a wrong path silently succeeds and the test will pass for the wrong reason — verify by intentionally breaking the target function and checking that the test fails.

### 4. Update `RUN_TEST_CMD`
- Set `RUN_TEST_CMD` in `state.md` to a command that collects from the **new** test root (typically `<POLY_CMD_PREFIX_RUN> pytest test/` for `loose`, or per-brick collection for `tdd`).
- Verify the test count after the move equals the baseline recorded in `migrate-discover`. **A drop in collected tests means files were lost or pytest discovery is misconfigured.**

## Verify
- `RUN_TEST_CMD` succeeds and **collects the same number of tests** as the baseline from `migrate-discover`.
- If set, `RUN_LINT_CMD` succeeds.
- `POLY_CMD_PREFIX check` is still green.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| `pytest` collects fewer tests than before | The old test root is no longer on `pytest`'s path; or duplicate `conftest.py` files silently shadow each other. | Update `[tool.pytest.ini_options].testpaths` (or pass paths explicitly in `RUN_TEST_CMD`). Run `pytest --collect-only` and diff against baseline collection. |
| `fixture '<name>' not found` | The fixture was in a `conftest.py` you moved into a brick's test dir; tests in another brick can no longer see it. | Either move the fixture up to a higher-scope `conftest.py`, or duplicate it (only if cheap). Don't import fixtures across `conftest.py` files. |
| Tests pass but assert nothing useful (`mock.patch` no longer hits anything) | Patch string still points at the pre-migration module path. | Re-derive the patch path: `<TARGET_TOP_NS>.<brick_name>.<module>.<symbol>`. Validate by deliberately breaking the patched function and confirming the test fails. |
| `ImportError: cannot import name 'fixture_<x>'` from `conftest.py` | A `conftest.py` `import`s a moved test helper module that didn't follow it. | Move the helper next to the new `conftest.py`, or import it from its new brick path. |
| Tests for moved code suddenly find themselves under a brick name that doesn't match their content | Misclassification in step 1. | Re-read the test's imports — the brick most imported is the one that owns the test. Move and update. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |
