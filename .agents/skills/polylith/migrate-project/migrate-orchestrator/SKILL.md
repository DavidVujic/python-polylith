---
name: migrate-orchestrator
description: "[ENTRY POINT] Load this skill first when the user asks to migrate a non-Polylith Python project to Polylith (e.g. \"migrate `projects/<name>` to Polylith\"). Drives the full migration workflow plus optional tooling conversions; do not load any other `migrate-*` skill directly — they are sub-skills this orchestrator invokes."
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
   If there are uncommitted changes, ask the user to commit/stash before proceeding. Do not start a migration on top of a dirty tree. (If the repo has **no commits yet**, create an initial baseline commit so there is a `GIT_BASE_SHA` to roll back to.)
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

The table below is the **single source of truth** for phase order and numbering.
Execute phases top to bottom. **Verify each phase's `Verify` section before
starting the next, and commit between phases** (see Phase 0 step 3). Where a
sub-skill's own `## Commit` section or `description:` hardcodes a *different*
phase number, **ignore that number** — use the `#` from this table in the
commit message.

### Main line (always run)

| #  | Phase                                  | Skill                                          | Depends on |
|----|----------------------------------------|------------------------------------------------|------------|
| 1  | Discover                               | `migrate-discover`                             | —          |
| 2  | Analyze imports + choose rewrite strategy | `migrate-analyze-imports`                   | 1          |
| 3  | Extract to base                        | `migrate-extract-to-base`                      | 2          |
| 4  | Update imports in the new base         | `migrate-automate-import-updates`              | 3          |
| 5  | Prepare project                        | `migrate-prepare-project`                      | 4 (+ 4b if taken) |
| 6  | Verify stability                       | `migrate-verify-stability`                     | 5          |
| 7  | Isolate base and big component         | `migrate-isolate-base-and-big-component`       | 6          |
| 8  | Split big component                    | `migrate-split-big-component`                  | 7          |
| 9  | Extract standalone modules             | `migrate-extract-standalone-modules`           | 8          |
| 10 | Isolate shared and project logic       | `migrate-isolate-shared-and-project-logic`     | 9          |
| 11 | Distribute wiring                      | `migrate-distribute-wiring`                    | 10         |
| 12 | Split component internals              | `migrate-split-component-internals`            | 11         |
| 13 | Refactor tests                         | `migrate-refactor-tests`                       | 12         |
| 14 | Definition of done                     | `migrate-definition-of-done`                   | 13         |

### Conditional namespace-shim sub-track (phase 4b)

`migrate-analyze-imports` (phase 2) sets a `SHIM_STRATEGY` in `state.md`:

- **`shimless`** (recommended when imports are submodule-qualified — e.g.
  `from <ns>.<sub> import …` — and `<ns>/__init__.py` exports little or nothing;
  a top-level re-export shim would resolve nothing there): **phase 4 rewrites all
  references** — base internals, entrypoints, infra, and tests — directly to the
  new namespace. **Skip the sub-track below.**
- **`shim`** (a top-level re-export shim is viable): after phase 4, run this
  sub-track before phase 5, then continue the main line:

  | #     | Phase                       | Skill                              | Depends on |
  |-------|-----------------------------|------------------------------------|------------|
  | 4b.i  | Generate compatibility shim | `migrate-generate-shim`            | 3, 4       |
  | 4b.ii | Detect circular imports     | `migrate-detect-circular-imports`  | 4b.i       |
  | 4b.iii| Resolve circular imports    | `migrate-resolve-circular-imports` | 4b.ii      |
  | 4b.iv | Update test files           | `migrate-update-tests`             | 4b.iii     |

> **Dependency note (why this is a *post-extraction* sub-track):** the shim
> re-exports the **original** namespace *from the new base location*, so it can
> only be generated **after** `migrate-extract-to-base` (phase 3) and after the
> base's own imports point at the new namespace (`migrate-automate-import-updates`,
> phase 4). A shim generated before extraction would re-export from a location
> that does not exist yet.

### Skippable / mergeable phases

Some phases are no-ops for certain projects. Skip with a one-line rationale
recorded in `state.md`, and still commit the (possibly empty) phase so the
`git log` stays complete:

- **Phase 10 (isolate shared and project logic)** — skip on the **first** project
  migrated into the workspace (there is no second project to compare against).
  Revisit when a 2nd overlapping project is migrated.
- **Phase 12 (split component internals)** — skip when components are already
  cohesive (no monolithic `core.py` mixing multiple domains).
- **Infra relocation / per-brick test layout** — if a step cannot be verified in
  the migration environment (e.g. a deploy cycle is required), it may be
  **deferred with a documented rationale** rather than blocking the migration
  (see `migrate-prepare-project` and `migrate-definition-of-done`).

## Optional Skills

These are not part of the linear flow above. They are triggered when the user opts in during `migrate-discover` (or, for `migrate-dedupe`, when duplication candidates surface). When triggered, **insert them at the indicated point** in the flow.

| Skill                              | When to run                                                        | Trigger                                         |
|------------------------------------|--------------------------------------------------------------------|-------------------------------------------------|
| `migrate-convert-linter`           | After `migrate-discover`, before `migrate-analyze-imports`.        | User opts in during `migrate-discover`.         |
| `migrate-convert-type-checker`     | After `migrate-discover`, before `migrate-analyze-imports`.        | User opts in during `migrate-discover`.         |
| `migrate-convert-package-manager`  | After `migrate-discover`, before `migrate-analyze-imports`.        | User opts in during `migrate-discover` **AND** the workspace itself uses uv. The skill is opinionated about uv — see its header for the gating rule. |
| `migrate-dedupe`                   | After `migrate-split-big-component` or `migrate-extract-standalone-modules` surfaces duplication candidates. | Duplication candidates surfaced and user approves. |

> ⚠ `migrate-convert-package-manager` only converts **to uv**. If the workspace uses Poetry, PDM, or Hatch as its standard, **skip this skill entirely** — the project should be aligned to the workspace's manager via a manual step instead.

### Ordering when multiple converters are opted in

When the user opts into more than one of the optional `migrate-convert-*` skills during `migrate-discover`, run them in **this order** between `migrate-discover` and `migrate-analyze-imports`:

1. `migrate-convert-package-manager` — runs first because it rewrites `pyproject.toml` wholesale; subsequent skills must operate on the final layout.
2. `migrate-convert-linter` — runs second so workspace-level lint config consolidation happens against the final `pyproject.toml`.
3. `migrate-convert-type-checker` — runs last; type-checker config is the most localized of the three.

`migrate-dedupe` is triggered later (after the big component is split and duplication candidates surface) and has **no ordering dependency** with the converters.

Commit between each optional skill the same way the main phases commit (see each skill's `## Commit` section).

## Execution checklist

For each phase:
1. **Validate `state.md`** against the rules in `migrate-discover` (`### Validation rules`). Abort the phase if validation fails.
2. Load the skill (`migrate-<phase>`).
3. Execute its `Steps` in order.
4. Run its `Verify` section. **If verification fails, do not commit and do not proceed.** Either fix the issue, or `git reset --hard` to back out the phase and consult the user.
5. On success, commit per the phase's `## Commit` section, using the `#` from **this** orchestrator table (not any number baked into the sub-skill).

## Validation
- **The phase graph is a DAG.** Every `Depends on` entry references an
  earlier-numbered phase (or an earlier step of the 4b sub-track), so a strict
  top-to-bottom execution always satisfies dependencies. (An earlier version of
  this table violated that — it listed `generate-shim` *before* `extract-to-base`;
  the shim phases are now a post-extraction sub-track, phase 4b.)
- Every skill referenced above exists as `migrate-<name>/SKILL.md` under `.agents/skills/polylith/migrate-project/`.
- Each phase's `Verify` block uses the commands recorded in `migration/<project-name>/state.md` (`RUN_TEST_CMD`, optionally `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD`, plus `POLY_CMD_PREFIX check`).
