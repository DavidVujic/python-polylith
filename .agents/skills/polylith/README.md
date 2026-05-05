
# Polylith Skills

> **Note for contributors:** this README is a **human reference**. The agent loads each `*/SKILL.md` independently via the skill loader; this file is **not** auto-loaded with any skill. Anything an agent must know to act has to live in the relevant `SKILL.md` itself, not here.

## Available Skills

| Skill                     | Command            | Purpose                                                                                                  |
|---------------------------|--------------------|----------------------------------------------------------------------------------------------------------|
| [Workspace Setup](./workspace_setup/SKILL.md)             | `poly create workspace` | Initialize a Polylith workspace (`workspace.toml`, top-level dirs).                  |
| [Component Creation](./component_creation/SKILL.md)       | `poly create component` | Create a reusable brick (business logic, domain, capability).                        |
| [Base Creation](./base_creation/SKILL.md)                 | `poly create base`      | Create an entry-point brick (HTTP API, CLI, Lambda handler).                         |
| [Project Management](./project_management/SKILL.md)       | `poly create project`   | Create a deployable project that references bricks.                                  |
| [Brick Removal](./brick_removal/SKILL.md)                 | —                       | Safely delete a component or base (no `poly remove` exists).                         |
| [Sync](./sync/SKILL.md)                                   | `poly sync`             | Update each project's brick list to match actual imports.                            |
| [Workspace Inspection](./workspace_inspection/SKILL.md)   | `poly info`             | Show brick × project usage (which projects use which bricks).                        |
| [Dependency Visualization](./dependency_visualization/SKILL.md) | `poly deps`       | Show brick × brick dependencies and interface compliance.                            |
| [Testing](./testing/SKILL.md)                             | `poly test diff`        | List bricks/projects affected by **test-code** changes since a tag.                  |
| [Diff](./diff/SKILL.md)                                   | `poly diff`             | List bricks whose **implementation** changed since a tag.                            |
| [Check](./check/SKILL.md)                                 | `poly check`            | Validate the workspace (CI gate; exits 1 on failure).                                |
| [Libs](./libs/SKILL.md)                                   | `poly libs`             | Inspect third-party libraries per project.                                           |
| [Concepts](./concepts/SKILL.md)                           | —                       | Provides foundational knowledge about Polylith architecture and terminology.           |

---

## For humans — getting started

1. **Set up the workspace** — [Workspace Setup](./workspace_setup/SKILL.md).
2. **Understand the basics** — [Concepts](./concepts/SKILL.md).
3. **Create bricks** — [Component Creation](./component_creation/SKILL.md) and [Base Creation](./base_creation/SKILL.md).
4. **Create deployable projects** — [Project Management](./project_management/SKILL.md).
5. **Remove bricks safely** — [Brick Removal](./brick_removal/SKILL.md).
6. **Sync brick usage** — [Sync](./sync/SKILL.md).
7. **Inspect** — [Workspace Inspection](./workspace_inspection/SKILL.md) (brick × project) and [Dependency Visualization](./dependency_visualization/SKILL.md) (brick × brick).
8. **Validate** — [Check](./check/SKILL.md) (CI gate) and [Libs](./libs/SKILL.md) (library inspection).
9. **Diff between releases** — [Diff](./diff/SKILL.md) and [Testing](./testing/SKILL.md).
