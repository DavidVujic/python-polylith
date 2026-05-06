
# Polylith Skills

> **Note for contributors:** this README is a **human reference**. The agent loads each `*/SKILL.md` independently via the skill loader; this file is **not** auto-loaded with any skill. Anything an agent must know to act has to live in the relevant `SKILL.md` itself, not here.

## Available Skills

| Skill                     | Command            | Purpose                                                                                                  |
|---------------------------|--------------------|----------------------------------------------------------------------------------------------------------|
| [Workspace Setup](./polylith-workspace-setup/SKILL.md)             | `poly create workspace` | Initialize a Polylith workspace (`workspace.toml`, top-level dirs).                  |
| [Component Creation](./polylith-component-creation/SKILL.md)       | `poly create component` | Create a reusable brick (business logic, domain, capability).                        |
| [Base Creation](./polylith-base-creation/SKILL.md)                 | `poly create base`      | Create an entry-point brick (HTTP API, CLI, Lambda handler).                         |
| [Project Management](./polylith-project-management/SKILL.md)       | `poly create project`   | Create a deployable project that references bricks.                                  |
| [Brick Removal](./polylith-brick-removal/SKILL.md)                 | —                       | Safely delete a component or base (no `poly remove` exists).                         |
| [Sync](./polylith-sync/SKILL.md)                                   | `poly sync`             | Update each project's brick list to match actual imports.                            |
| [Workspace Inspection](./polylith-workspace-inspection/SKILL.md)   | `poly info`             | Show brick × project usage (which projects use which bricks).                        |
| [Dependency Visualization](./polylith-dependency-visualization/SKILL.md) | `poly deps`       | Show brick × brick dependencies and interface compliance.                            |
| [Testing](./polylith-testing/SKILL.md)                             | `poly test diff`        | List bricks/projects affected by **test-code** changes since a tag.                  |
| [Diff](./polylith-diff/SKILL.md)                                   | `poly diff`             | List bricks whose **implementation** changed since a tag.                            |
| [Check](./polylith-check/SKILL.md)                                 | `poly check`            | Validate the workspace (CI gate; exits 1 on failure).                                |
| [Libs](./polylith-libs/SKILL.md)                                   | `poly libs`             | Inspect third-party libraries per project.                                           |
| [Concepts](./polylith-concepts/SKILL.md)                           | —                       | Provides foundational knowledge about Polylith architecture and terminology.           |
