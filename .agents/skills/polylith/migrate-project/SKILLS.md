---
name: migrate-project
description: Skills for migrating a non-Polylith Python project into a Polylith workspace. **Only use when explicitly requested by a human.**
---

# Project Migration Skills Index

This file serves as an index for all **project migration skills** available in the Polylith CLI. These skills are **only** for migrating **non-Polylith Python projects** into a Polylith workspace **when explicitly requested by a human**.

**⚠️ When to Use These Skills**
- A human has **explicitly instructed** to migrate a specific project (e.g., "Migrate the project `my-app` in `/projects/my-app` to Polylith").
- The target project has been copied into the `/projects` folder of this Polylith workspace.
- These skills are **not** relevant for daily Polylith workflows or already-migrated projects.
- They are **not** intended for automated or unattended use.

## Orchestrator
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [orchestrator](./orchestrator/skill.md) | Orchestrates the migration workflow by defining the order and dependencies of migration skills. | None |

## Discovery
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [discover](./discover/skill.md) | Create `migration/<PROJECT>/state.md` and `migration/<PROJECT>/manifest.md` by inspecting the existing project under `projects/<app>/`. Detect the current linter and type checker, and ask the user if they want to convert them. | None |

## Extraction
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [extract-to-base](./extract-to-base/skill.md) | Extract all application code from `projects/<app>/` into a temporary migration base. | discover |
| [prepare-project](./prepare-project/skill.md) | Clean up the project subfolder and consolidate dependencies. | extract-to-base |
| [isolate-base-and-big-component](./isolate-base-and-big-component/skill.md) | Shrink the temporary migration base into thin bases and a big component. | prepare-project |

## Refactoring
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [split-big-component](./split-big-component/skill.md) | Split the big component into multiple focused components. | isolate-base-and-big-component |
| [extract-standalone-modules](./extract-standalone-modules/skill.md) | Extract foundational modules (e.g., `consts.py`, `exceptions.py`) into standalone components. | split-big-component |
| [isolate-shared-and-project-logic](./isolate-shared-and-project-logic/skill.md) | Identify and isolate shared and project-specific logic in monolithic components (e.g., `models`, `schemas`). | extract-standalone-modules, split-big-component |
| [distribute-wiring](./distribute-wiring/skill.md) | Distribute app-wiring code from the residual component into the appropriate bases and shared components. | isolate-shared-and-project-logic |
| [split-component-internals](./split-component-internals/skill.md) | Split monolithic `core.py` files in generic components (e.g., `models`, `schemas`) into domain-focused modules. | distribute-wiring |
| [refactor-tests](./refactor-tests/skill.md) | Restructure unit tests to align with the workspace's Polylith theme. | split-component-internals |

## Optional Tooling Conversions
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [convert-linter](./convert-linter/skill.md) | Replace the project's existing linter and formatter with **ruff** (if the user opts in). | discover |
| [convert-type-checker](./convert-type-checker/skill.md) | Replace the project's existing type checker with **ty** (if the user opts in). | discover |
| [convert-package-manager](./convert-package-manager/skill.md) | Convert the project's `pyproject.toml` to PEP 621/uv format and register it as a workspace member (if the user opts in). | discover |

## Optional Deduplication
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [dedupe](./dedupe/skill.md) | Identify and execute controlled deduplication of code during migration (if the user opts in). | split-big-component, extract-standalone-modules |

## Completion
| Skill | Description | Dependencies |
|-------|-------------|--------------|
| [definition-of-done](./definition-of-done/skill.md) | Define the criteria for completing the migration process. | refactor-tests |
