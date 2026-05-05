---
name: polylith-dependency-management
description: Add or manage third-party dependencies in a Polylith workspace. Use when the user wants to install a new library (e.g., requests, fastapi) for a brick or project.
---

# Dependency Management Skill

> 💡 **Terminology:** this skill uses Polylith terms like *brick*, *project*, and *development project*. If they're unfamiliar, load `polylith-concepts` first.

Polylith manages third-party dependencies differently than standard Python projects.

## Rules for adding dependencies

1. **The Development Project (Root):**
   **Every** third-party library used anywhere in the workspace must be added to the root `pyproject.toml` (the development project). This ensures local REPLs, tests, and the shared lockfile work correctly. Use your package manager (e.g., `uv add <package>`, `poetry add <package>`) at the workspace root.
2. **Deployable Projects (`projects/<name>`):**
   If a library is required for production by a specific deployable project, it must **also** be added to that project's `pyproject.toml` under `projects/<name>/`. Do this by manually editing the `dependencies` array in `projects/<name>/pyproject.toml`.

> ⚠ **Never add dependencies to a brick's directory.** Bricks do not have their own `pyproject.toml` files.

## Example Workflow: Adding `requests` to an `api` project

1. Install it at the root so the lockfile updates and it's available for local development:
   ```bash
   uv add requests
   ```
2. Manually add it to the deployable project that needs it:
   Edit `projects/api/pyproject.toml`. 
   
   **Important Versioning Rule:** Before adding the dependency to the project, check the root `pyproject.toml`. If it contains a `[tool.uv.workspace]` section (e.g., `members = ["projects/*"]`), then `uv workspaces` is enabled. 
   
   If `uv workspaces` is enabled, **do not specify the version** in the project's `pyproject.toml`. Just use the package name, because versions are centrally pinned in the root. If workspaces are not enabled, then you should specify the version.
   
   ```toml
   # WITH uv/poetry workspaces enabled (Recommended):
   dependencies = [
       "requests"
   ]
   
   # WITHOUT workspaces enabled:
   dependencies = [
       "requests>=2.31.0"
   ]
   ```
3. Run `poly check` (load `polylith-check`) to verify the workspace is valid. `poly check` will catch if a project imports `requests` but forgot to declare it in its `pyproject.toml`.

## Notes for the agent
- Use `poly libs` (load `polylith-libs`) to inspect current dependency usage across projects.
