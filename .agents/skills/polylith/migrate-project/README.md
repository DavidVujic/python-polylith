# Project Migration Skills

> **Note for contributors:** this README is a **human reference** and a skill **index**. Agents load each `migrate-*/SKILL.md` independently via the skill loader; this README is **not** auto-loaded with any skill. Anything an agent must know to act has to live in the relevant `SKILL.md` itself, not here.

This directory contains skills for migrating **non-Polylith Python projects** into a Polylith workspace. They cooperate via two artifacts under `migration/<PROJECT>/`:

- `state.md` — a flat `KEY=value` file. Canonical schema lives in [`migrate-discover/SKILL.md`](./migrate-discover/SKILL.md).
- `manifest.md` — a human-readable structural inventory of the source project.

---

## ⚠️ When to use these skills

**Only** when:
1. A human has **explicitly instructed** to migrate a specific project (e.g., "migrate `projects/my-app` to Polylith").
2. The target project lives under `projects/<PROJECT>/` of this Polylith workspace.
3. The goal is to refactor the project into Polylith bricks (bases and components).

**Do not use** for:
- Automated or unattended migrations.
- Projects that are already structured as Polylith bricks.
- Daily Polylith development tasks — for those, see the sibling `polylith-*` skills.

---

## How to invoke

Load the orchestrator and let it drive the rest:

```
Load the `migrate-orchestrator` skill and migrate `projects/<project-name>`.
```

The orchestrator will:
1. Ask the user for explicit confirmation.
2. Establish a git safety net (dedicated branch + per-phase commits).
3. Load and execute each phase skill in order, verifying after each.

> **Why every sub-skill says "do not load directly".** Each `migrate-<phase>` skill's `description:` starts with a redirect to `migrate-orchestrator`. This is intentional: it makes the orchestrator the only valid entry point regardless of which sub-skill the agent's fuzzy-match initially favours. The sub-skills depend on state (`migration/<PROJECT>/state.md`) and a git safety net that only the orchestrator sets up.

---

## Downstream installation

When this skill set is installed into another Polylith workspace (e.g. via a skills package), the in-skill `[ENTRY POINT]` / `[Internal sub-skill of migrate-orchestrator …]` markers in each `description:` are the primary routing signal — they ship with the package.

For an extra-strong signal, downstream consumers should add the following snippet to their own repo-level `AGENTS.md` (or equivalent agent-routing file). It is **not** required — the in-skill markers are usually sufficient — but it removes any ambiguity for agents that read `AGENTS.md` before scanning skill descriptions.

```markdown
## Polylith migration instructions

When the user asks to migrate a non-Polylith Python project to Polylith
(e.g. "migrate `projects/<name>` to Polylith"), load the
`migrate-orchestrator` skill first and let it drive the workflow.

Never load `migrate-discover`, `migrate-extract-to-base`, or any other
`migrate-*` sub-skill directly — they are phases the orchestrator
invokes in order, with per-phase verification and git checkpoints
between them.
```

---

## Workflow at a glance

| # | Phase                                  | Skill                                          | Depends on                                                          |
|---|----------------------------------------|------------------------------------------------|---------------------------------------------------------------------|
| — | Orchestration                          | [`migrate-orchestrator`](./migrate-orchestrator/SKILL.md) | —                                                          |
| 1 | Discover                               | [`migrate-discover`](./migrate-discover/SKILL.md) | —                                                                |
| 2 | Extract to base                        | [`migrate-extract-to-base`](./migrate-extract-to-base/SKILL.md) | `migrate-discover`                                  |
| 3 | Prepare project                        | [`migrate-prepare-project`](./migrate-prepare-project/SKILL.md) | `migrate-extract-to-base`                           |
| 4 | Isolate base and big component         | [`migrate-isolate-base-and-big-component`](./migrate-isolate-base-and-big-component/SKILL.md) | `migrate-prepare-project`            |
| 5 | Split big component                    | [`migrate-split-big-component`](./migrate-split-big-component/SKILL.md) | `migrate-isolate-base-and-big-component`    |
| 6 | Extract standalone modules             | [`migrate-extract-standalone-modules`](./migrate-extract-standalone-modules/SKILL.md) | `migrate-split-big-component`         |
| 7 | Isolate shared and project logic       | [`migrate-isolate-shared-and-project-logic`](./migrate-isolate-shared-and-project-logic/SKILL.md) | `migrate-extract-standalone-modules`, `migrate-split-big-component` |
| 8 | Distribute wiring                      | [`migrate-distribute-wiring`](./migrate-distribute-wiring/SKILL.md) | `migrate-isolate-shared-and-project-logic`          |
| 9 | Split component internals              | [`migrate-split-component-internals`](./migrate-split-component-internals/SKILL.md) | `migrate-distribute-wiring`           |
|10 | Refactor tests                         | [`migrate-refactor-tests`](./migrate-refactor-tests/SKILL.md) | `migrate-split-component-internals`                    |
|11 | Definition of done                     | [`migrate-definition-of-done`](./migrate-definition-of-done/SKILL.md) | `migrate-refactor-tests`                       |

### Optional skills (triggered during `migrate-discover`)

| Skill                                                                                           | Purpose                                                                                              | Trigger / dependency                                                              |
|-------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| [`migrate-convert-linter`](./migrate-convert-linter/SKILL.md)                                   | Align the project's linter/formatter with the **workspace's** configured tool.                      | `CONVERT_LINTER=yes` in `state.md`. Runs between phase 1 and phase 2.             |
| [`migrate-convert-type-checker`](./migrate-convert-type-checker/SKILL.md)                       | Align the project's type checker with the **workspace's** configured tool.                          | `CONVERT_TYPE_CHECKER=yes` in `state.md`. Runs between phase 1 and phase 2.       |
| [`migrate-convert-package-manager`](./migrate-convert-package-manager/SKILL.md)                 | Convert the project's `pyproject.toml` to uv workspaces. **Opinionated about uv** — only run when the workspace itself uses uv. | `CONVERT_PACKAGE_MANAGER=yes` in `state.md`. Runs between phase 1 and phase 2.    |
| [`migrate-dedupe`](./migrate-dedupe/SKILL.md)                                                   | Identify and apply controlled deduplication discovered during refactoring.                          | User approval. Runs after phase 5 or phase 6.                                     |

---

## Scope of the four "splitting" skills

These skills overlap in vocabulary but address different scopes. Use this matrix to decide which one applies:

| Skill                                       | Scope                                          | Trigger                                                                   |
|---------------------------------------------|------------------------------------------------|---------------------------------------------------------------------------|
| `migrate-split-big-component`               | Within one project; component → multiple components. | The temporary big component from phase 4 is too large.              |
| `migrate-extract-standalone-modules`        | Within one project; pulls foundational modules out of the residual. | Residual still contains `consts.py`/`exceptions.py`/`models.py`.  |
| `migrate-split-component-internals`         | Within one already-extracted shared component; `core.py` → multiple files. | A component's `core.py` mixes multiple domains internally.      |
| `migrate-isolate-shared-and-project-logic`  | Cross-project; separate shared vs project-specific in components used by ≥ 2 projects. | Migrating a 2nd+ project that overlaps with an already-extracted one. |

> 💡 In a fresh migration of a single project, you usually run `migrate-split-big-component` → `migrate-extract-standalone-modules` → `migrate-split-component-internals`, and skip `migrate-isolate-shared-and-project-logic` until a second project is migrated.

---

## Files in this directory

- `README.md` — this file (human reference + index).
- `migrate-orchestrator/SKILL.md` — entry point; defines the phase order and the git safety net.
- `migrate-<phase>/SKILL.md` — one per phase listed above.
