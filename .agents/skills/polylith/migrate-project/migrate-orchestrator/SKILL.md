---
name: migrate-orchestrator
description: "[ENTRY POINT] Load this skill first when the user asks to migrate a non-Polylith Python project to Polylith (e.g. \"migrate `projects/<name>` to Polylith\"). Drives all 11 migration phases plus optional tooling conversions; do not load any other `migrate-*` skill directly — they are sub-skills this orchestrator invokes."
---

# Skill: migrate-orchestrator

> 🧭 **You are in the right place.** This is the **entry point** for migrating a non-Polylith Python project into a Polylith workspace. If you arrived here from a fuzzy match on a sub-skill name (e.g., `migrate-discover`, `migrate-extract-to-base`), **stay here** — those sub-skills depend on state and a git safety net that only this orchestrator sets up. Loading them in isolation is undefined behaviour. Execute the phases below in order.

## Goal
Define and execute the workflow for migrating a non-Polylith Python project to a Polylith workspace.
**This skill must be explicitly invoked by a human with the project name/path.**

## Usage
To migrate a project, load the `migrate-orchestrator` skill and provide the project name (the subdirectory under `projects/`):

```
Load the `migrate-orchestrator` skill and migrate `projects/<project-name>`.
```

> 💡 **How sub-skills are loaded.** Each phase points to another skill named `migrate-<phase>` (e.g., `migrate-discover`, `migrate-extract-to-base`). Load each via your skill loader before executing the phase. Do not interleave phases — finish and verify one before starting the next.

## Pre-flight

### 0. User Confirmation
Ask the user to confirm the project path and migration intent before doing anything else:

```
You are about to migrate `projects/<project-name>` to Polylith. This will refactor
the project into bases and components and move files. Proceed? (yes/no)
```

If the user declines, abort:
```
Migration aborted by user.
```

### Phase 0. Safety Net (git checkpoint)
Migration is destructive — files move, directories are deleted, `pyproject.toml`s are rewritten. **Before loading `migrate-discover`, establish rollback points:**

1. Confirm the working tree is clean:
   ```bash
   git status
   ```
   If there are uncommitted changes, ask the user to commit/stash before proceeding. Do not start a migration on top of a dirty tree.
2. Create a dedicated migration branch:
   ```bash
   git checkout -b migrate/<project-name>
   ```
3. After each completed phase, commit per that phase's `## Commit` section. The commit message follows the pattern `migrate(<project-name>): phase <N> — <phase-name>` so phases can be located in `git log` later.
   ```bash
   git add -A && git commit -m "migrate(<project-name>): phase <N> — <phase-name>"
   ```
   This gives the user (and the agent) a discrete, named rollback point per phase. If a later phase fails verification, the agent can `git reset --hard HEAD~1` to back out exactly one phase without losing earlier progress.
4. Record the branch name and starting commit SHA in `migration/<project-name>/state.md` (the `migrate-discover` skill defines that file).

> ⚠ Never `git reset --hard` past the start of the migration branch without explicit user approval — the user's pre-migration work lives there.

## Workflow

Execute the phases in this order. **Verify each phase's `Verify` section succeeds before starting the next.** Commit between phases (see Phase 0 step 3).

| # | Phase                                  | Skill                                          | Depends on                                          |
|---|----------------------------------------|------------------------------------------------|-----------------------------------------------------|
| 1 | Discover                               | `migrate-discover`                             | —                                                   |
| 2 | Analyze imports                        | `migrate-analyze-imports`                      | `migrate-discover`                                  |
| 3 | Generate compatibility shim            | `migrate-generate-shim`                        | `migrate-analyze-imports`                           |
| 4 | Extract to base                        | `migrate-extract-to-base`                      | `migrate-generate-shim`                             |
| 5 | Update imports in new base             | `migrate-automate-import-updates`              | `migrate-extract-to-base`                           |
| 6 | Detect circular imports                | `migrate-detect-circular-imports`              | `migrate-automate-import-updates`                   |
| 7 | Resolve circular imports               | `migrate-resolve-circular-imports`             | `migrate-detect-circular-imports`                  |
| 8 | Update test files                      | `migrate-update-tests`                         | `migrate-resolve-circular-imports`                  |
| 9 | Prepare project                        | `migrate-prepare-project`                      | `migrate-update-tests`                              |
| 10| Verify stability                       | `migrate-verify-stability`                     | `migrate-prepare-project`                           |
| 11| Isolate base and big component         | `migrate-isolate-base-and-big-component`       | `migrate-verify-stability`                          |
| 12| Split big component                    | `migrate-split-big-component`                  | `migrate-isolate-base-and-big-component`            |
| 13| Extract standalone modules             | `migrate-extract-standalone-modules`           | `migrate-split-big-component`                       |
| 14| Isolate shared and project logic       | `migrate-isolate-shared-and-project-logic`     | `migrate-extract-standalone-modules`, `migrate-split-big-component` |
| 15| Distribute wiring                      | `migrate-distribute-wiring`                    | `migrate-isolate-shared-and-project-logic`          |
| 16| Split component internals              | `migrate-split-component-internals`            | `migrate-distribute-wiring`                         |
| 17| Refactor tests                         | `migrate-refactor-tests`                       | `migrate-split-component-internals`                 |
| 18| Definition of done                     | `migrate-definition-of-done`                   | `migrate-refactor-tests`                            |

## Optional Skills

These are not part of the linear flow above. They are triggered when the user opts in during `migrate-discover` (or, for `migrate-dedupe`, when duplication candidates surface). When triggered, **insert them at the indicated point** in the flow.

| Skill                              | When to run                                                        | Trigger                                         |
|------------------------------------|--------------------------------------------------------------------|-------------------------------------------------|
| `migrate-convert-linter`           | After phase 1 (`migrate-discover`), before phase 2.                | User opts in during `migrate-discover`.         |
| `migrate-convert-type-checker`     | After phase 1 (`migrate-discover`), before phase 2.                | User opts in during `migrate-discover`.         |
| `migrate-convert-package-manager`  | After phase 1 (`migrate-discover`), before phase 2.                | User opts in during `migrate-discover` **AND** the workspace itself uses uv. The skill is opinionated about uv — see its header for the gating rule. |
| `migrate-dedupe`                   | After phase 5 (`migrate-split-big-component`) or phase 6 (`migrate-extract-standalone-modules`). | Duplication candidates surfaced and user approves. |

> ⚠ `migrate-convert-package-manager` only converts **to uv**. If the workspace uses Poetry, PDM, or Hatch as its standard, **skip this skill entirely** — the project should be aligned to the workspace's manager via a manual step instead.

### Ordering when multiple converters are opted in

When the user opts into more than one of the optional `migrate-convert-*` skills during `migrate-discover`, run them in **this order** between phase 1 and phase 2:

1. `migrate-convert-package-manager` — runs first because it rewrites `pyproject.toml` wholesale; subsequent skills must operate on the final layout.
2. `migrate-convert-linter` — runs second so workspace-level lint config consolidation happens against the final `pyproject.toml`.
3. `migrate-convert-type-checker` — runs last; type-checker config is the most localized of the three.

`migrate-dedupe` is triggered later (after phase 5 or phase 6 surfaces duplication candidates) and has **no ordering dependency** with the converters.

Commit between each optional skill the same way the main phases commit (see each skill's `## Commit` section).

## Execution checklist

For each phase:
1. **Validate `state.md`** against the rules in `migrate-discover` (`### Validation rules`). Abort the phase if validation fails.
2. Load the skill (`migrate-<phase>`).
3. Execute its `Steps` in order.
4. Run its `Verify` section. **If verification fails, do not commit and do not proceed.** Either fix the issue, or `git reset --hard` to back out the phase and consult the user.
5. On success, commit per the phase's `## Commit` section.

## Validation
- No circular dependencies exist in the phase graph above (verified by the dependency table).
- Every skill referenced above exists as `migrate-<name>/SKILL.md` under `.agents/skills/polylith/migrate-project/`.
- Each phase's `Verify` block uses the commands recorded in `migration/<project-name>/state.md` (`RUN_TEST_CMD`, optionally `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD`, plus `POLY_CMD_PREFIX check`).
