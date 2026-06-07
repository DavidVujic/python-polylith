---
name: polylith-migrate-convert-linter
description: "[Internal sub-skill of `polylith-migrate-orchestrator` (optional, runs only when opted in during `polylith-migrate-discover`). Do not load directly — load `polylith-migrate-orchestrator` first.] Align the project's linter and formatter with the **workspace's** configured tool (whatever it is — ruff, black+isort+flake8, pylint, etc.). Removes project-specific config and consolidates rules into the workspace root."
---

# Skill: polylith-migrate-convert-linter

## Goal
Align the project with the **workspace's** linter and formatter. This skill is **not** opinionated about ruff — it reads the workspace's configured tool from the root `pyproject.toml` and aligns the project to that.

## When to Skip
Skip this step if the project's `LINTER` and `FORMATTER` in `migration/<PROJECT>/state.md` already match the workspace's tools.

## Inputs
From `migration/<PROJECT>/state.md`:
- `PROJECT_DIR`
- `LINTER`, `FORMATTER`
- `RUN_TEST_CMD` (optional: `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`)

> All inputs from `state.md` are assumed to satisfy the validation rules in `polylith-migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### 0. Identify the workspace's tool
Open the **workspace root** `pyproject.toml` and identify the configured linter and formatter using the same detection table as `polylith-migrate-discover` (`[tool.ruff]` → ruff, `[tool.black]` → black, `[tool.flake8]` or `.flake8` → flake8, etc.). Record what you found — every step below refers to "the workspace's linter/formatter" and means **this** tool, not necessarily ruff.

If the workspace has no linter configured at all, stop and ask the user how to proceed (introduce ruff? skip linting alignment? abort the conversion?).

### 1. Remove Project-Specific Configs and Dependencies
- Remove the following sections from the project's `pyproject.toml`:
  - `[tool.black]`, `[tool.isort]`, `[tool.flake8]`, `[tool.pylint.*]`, `[tool.autopep8]`, `[tool.pycodestyle]`
- Remove standalone config files: `.flake8`, `.pylintrc`, `.isort.cfg`, and lint sections in `setup.cfg` or `tox.ini`.
- Remove old linter/formatter dependencies from the project's `pyproject.toml`:
  - `flake8`, `flake8-*` plugins, `pylint`, `pylint-*` plugins, `black`, `isort`, `autopep8`, `pyflakes`, `pycodestyle`, `bandit`

### 2. Assess Workspace Linting Config
- Review the workspace root's linting and formatting configuration.
- Identify any project-specific rules or ignores that differ from the workspace's standards.

### 3. Merge Project-Specific Rules
- If the project has unique linting rules or ignores, merge them into the workspace root's linting configuration (e.g., `[tool.ruff]`).
- For conflicts (e.g., stricter rules in the project), ask the user to provide guidance on whether to:
  - Adopt the project's rules in the workspace.
  - Suppress the project's rules in favor of the workspace's.
  - Defer the decision and document the conflict in `migration/<PROJECT>/state.md`.

### 4. Run Workspace Linting and Formatting Tools
- Run the workspace's linting tool to assess violations:
  - **Few new violations**: Fix them now.
  - **Many new violations**: Ask the user whether to fix, suppress, or defer.
- Run the workspace's formatting tool to reformat the code.

### 5. Update `state.md`
- Set `LINTER` and `FORMATTER` to the workspace's tool(s).
- Update `RUN_LINT_CMD` to use the workspace's linting and formatting commands.

## Verify
- The workspace's linting tool passes (or remaining violations are user-approved).
- The workspace's formatting tool passes.
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_TYPECHECK_CMD` succeeds.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| The workspace's linter surfaces hundreds of violations the project's old linter didn't catch | Stricter ruleset; not a "fix everything now" situation. | Ask the user: fix now, suppress via `[tool.<linter>]` ignores in the project subsection, or defer in a follow-up branch. Do **not** auto-fix silently — record the decision in `state.md`. |
| Project-specific lint rules are stricter than the workspace's standard | Project had higher discipline; lowering it would regress quality. | Add the project's rule as a per-path override in the workspace's lint config (most linters support per-directory rule overrides). Do not weaken the rule globally. |
| Old linter config file (`.flake8`, `.pylintrc`, etc.) lingers and confuses developers' local editors | Step 1 missed a config file. | Delete it; mention in the commit message so reviewers update their editor configs. |

## Done When
- No project-specific linter/formatter config files or dependencies remain.
- Project-specific linting rules are merged into the workspace root's configuration.
- `LINTER` and `FORMATTER` in `migration/<PROJECT>/state.md` match the workspace's tools.
- Tests pass via the workspace's tooling.

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase optional — convert-linter"
```

Substitute `<PROJECT>` from `state.md`. This is an **optional** skill off the numbered main line, so the commit uses the literal `phase optional` label (no `<N>`). Do not proceed without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
