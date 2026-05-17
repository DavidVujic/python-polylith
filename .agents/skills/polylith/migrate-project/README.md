# Project Migration Skills

This directory contains skills for migrating **non-Polylith Python projects** into a Polylith workspace.
These skills are **only** relevant when a human explicitly requests to migrate a specific project (e.g., "Migrate the project `my-app` in `/projects/my-app` to Polylith").

---

## ⚠️ Important Disclaimer
**These skills are NOT for daily Polylith workflows or already-migrated projects.**
They are **only** intended for use when:
1. A human has **explicitly instructed** to migrate a specific project.
2. The target project has been copied into the `/projects` folder of this Polylith workspace.
3. The goal is to refactor the project into Polylith bricks (bases, components, etc.).

**Do NOT use these skills for:**
- Automated or unattended migrations.
- Projects that are already structured as Polylith workspaces.
- Daily development tasks in a Polylith workspace.

---

## Purpose
The skills in this directory automate and standardize the process of migrating a Python project to a Polylith workspace. They ensure the migration is performed consistently and efficiently, with minimal manual intervention.

---

## How to Use
1. **Explicit Invocation**: Load the `migrate.orchestrator` skill and specify the project name (e.g., `my-app`).
   Example:
   ```
   Load the `migrate.orchestrator` skill and provide the project name (e.g., `my-app`).
   ```

2. **Follow the Workflow**: The orchestrator will guide you through the migration process, ensuring all dependencies are satisfied.

3. **Verify Completion**: After executing a skill, verify its completion before proceeding to the next step. Each skill includes a "Verify" section to confirm its success.

---

## Key Files
- [`SKILLS.md`](./SKILLS.md): Index of all project migration skills, their descriptions, and dependencies.
- [`orchestrator/skill.md`](./orchestrator/skill.md): Defines the step-by-step migration process and ensures all dependencies are satisfied.

---

## Workflow Overview
The migration process consists of the following phases:
1. **Discovery**: Inspect the project and create `state.md` and `manifest.md`.
2. **Tooling Standardization**: Align the project's tooling (e.g., package manager, linter, type checker) with the workspace's standards.
3. **Extraction**: Extract application code into a temporary migration base and prepare the project for Polylith.
4. **Refactoring**: Split the big component into focused components, extract standalone modules, and isolate shared/project-specific logic.
5. **Testing**: Restructure unit tests to align with the workspace's Polylith theme.
6. **Completion**: Verify that all migration criteria are met.
