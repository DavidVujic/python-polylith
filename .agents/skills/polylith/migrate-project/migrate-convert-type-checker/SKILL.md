---
name: migrate-convert-type-checker
description: "[Internal sub-skill of `migrate-orchestrator` (optional, runs only when opted in during `migrate-discover`). Do not load directly — load `migrate-orchestrator` first.] Align the project's type checker with the **workspace's** configured tool (whatever it is — mypy, pyright, ty, etc.). Removes project-specific config and consolidates settings into the workspace root."
---

# Skill: migrate-convert-type-checker

## Goal
Align the project with the **workspace's** type checker. This skill is **not** opinionated about ty — it reads the workspace's configured tool from the root `pyproject.toml` and aligns the project to that.

## When to Skip
Skip this step if the project's `TYPE_CHECKER` in `migration/<PROJECT>/state.md` already matches the workspace's type-checking tool.

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `TYPE_CHECKER`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### 0. Identify the workspace's tool
Open the **workspace root** `pyproject.toml` and identify the configured type checker using the same detection table as `migrate-discover` (`[tool.mypy]` or `mypy.ini` → mypy, `[tool.pyright]` or `pyrightconfig.json` → pyright, `[tool.ty]` → ty). Record what you found — every step below refers to "the workspace's type checker" and means **this** tool, not necessarily ty.

If the workspace has no type checker configured at all, stop and ask the user how to proceed (introduce one? skip type-check alignment? abort the conversion?).

### 1. Remove Old Configs and Dependencies
- Remove the following sections from `pyproject.toml`:
  - `[tool.mypy]`, `[[tool.mypy.overrides]]`, `[mypy-*]`, `[tool.pyright]`, `[tool.pytype]`
- Remove standalone config files: `mypy.ini`, `.mypy.ini`, `pyrightconfig.json`.
- Remove old type checker dependencies from `pyproject.toml`:
  - `mypy`, `mypy-extensions`, `types-*` stub packages, `pyright`, `pytype`, `sqlalchemy-stubs`, `django-stubs`.

### 2. Clean Up Type Ignore Comments
- Remove `# type: ignore[<mypy-code>]` comments that reference mypy-specific error codes.
- Leave comments that suppress real issues and document them in `state.md`.

### 3. Adopt Workspace Type-Checking Config
- The workspace root `pyproject.toml` may define the type-checking configuration. The project inherits this config.
- Add project-specific overrides if needed.

### 4. Run the Workspace's Type-Checking Tool
- Run the workspace's type-checking tool to assess errors:
  - **Same or fewer errors**: No action needed.
  - **New errors**: Ask the user whether to fix, suppress, or adjust the config.
  - **Missing stub errors**: Silence with per-module ignores in the workspace's type-checking config.

### 5. Update `state.md`
- Set `TYPE_CHECKER` to the workspace's type-checking tool.
- Update `RUN_TYPECHECK_CMD` to use the workspace's type-checking command.

## Verify
- The workspace's type-checking tool runs cleanly (or remaining errors are user-approved).
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` succeeds.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| The workspace's checker surfaces type errors the old checker didn't | Stricter type rules expose real bugs that were always there. | Fix the bugs now where cheap (small handful). For systemic gaps, suppress per-module in the workspace's checker config and document the debt in `state.md`. Do **not** blanket-ignore at file scope. |
| Stub packages (`types-*`, `django-stubs`, `sqlalchemy-stubs`) were required by the old checker but the new one bundles its own | Dependency carryover. | Remove the stub packages from `pyproject.toml`. Re-run the workspace's checker to confirm it picks up its own stubs. |
| `# type: ignore[<old-code>]` comments still reference the old checker's error codes | Step 2 missed some. | Strip the `[<code>]` bracket. If the suppression is still needed, leave a bare `# type: ignore` **with a comment explaining why**; otherwise remove the suppression entirely. |

## Done When
- No old type checker config files remain.
- Old type checker dependencies are removed from `pyproject.toml`.
- Stale `# type: ignore` comments referencing tool-specific codes are removed (or documented if intentionally kept).
- `TYPE_CHECKER` in `migration/<PROJECT>/state.md` matches the workspace's type-checking tool.
- The workspace's type-checking tool runs cleanly or known issues are documented in `state.md`.
- Tests pass via the workspace's tooling.

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase optional — convert-type-checker"
```

Substitute `<PROJECT>` from `state.md`. This is an **optional** skill off the numbered main line, so the commit uses the literal `phase optional` label (no `<N>`). Do not proceed without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
