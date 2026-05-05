---
name: polylith-project-management
description: Create a deployable Polylith project with `poly create project` — a lightweight `pyproject.toml` under `projects/<name>/` that references bricks for deployment as a Docker image, wheel, AWS Lambda, GCP Cloud Function, or other artifact. Use when the user wants a new deployable, service, microservice, or release target.
---

# Project Management Skill

> 💡 **Terminology:** this skill uses Polylith terms like *brick*, *base*, *namespace*, and *development project*. If they're unfamiliar, load `polylith-concepts` first.

## Quick command

```bash
uv run poly create project --name user_api --quiet
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> ⚠ **Do NOT invent flags** for selecting components/bases/deployment targets — they don't exist. The CLI accepts only `--name`, `--description`, and `--quiet`. Bricks are attached manually and via later `poly sync` runs.
> ⚠ **There is no `poly build project` command.** Building the artifact (Docker, wheel, Lambda zip) is the **package manager's** job (`uv build`, `poetry build`, `hatch build`, `pdm build`).

## What `poly create project` actually does
1. Detects the build backend in the **root** `pyproject.toml` (Hatchling, PDM, or Poetry) and picks the matching `pyproject.toml` template.
2. Writes `projects/<name>/pyproject.toml`, inheriting authors and `requires-python` from the root.
3. If `--quiet` is not used, it runs an interactive prompt to add bricks. Agents must always use `--quiet` and manage bricks manually.

## Prerequisites
- A Polylith workspace already exists (load `polylith-workspace-setup` if not).
- The root `pyproject.toml` exists and uses Hatchling, uv, Poetry, pixi, Maturin or PDM. Without it, the command exits non-zero with `Failed to guess the used Package & Dependency Management`.

## Command reference

| Option          | Required | Default | Description                                  |
|-----------------|----------|---------|----------------------------------------------|
| `--name`        | yes      | —       | Name of the project.                         |
| `--description` | no       | `""`    | Optional human-readable description.         |
| `--quiet`       | no       | `false` | Suppress the interactive prompt.             |

## Examples

```bash
# Minimal — bypass interactive prompt
uv run poly create project --name user_api --quiet

# With description
uv run poly create project --name consumer --description "Kafka order consumer" --quiet
```

## What gets written

```
projects/user_api/pyproject.toml
```

For the **Hatchling** backend (most common with Polylith):

```toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[project]
name = "user_api"
version = "0.1.0"
description = "User-facing HTTP API"
authors = [{ name = "Jane Doe", email = "jane@example.com" }]
requires-python = ">=3.12"
dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["mycompany"]

[tool.hatch.build.hooks.polylith-bricks]

[tool.polylith.bricks]
# Populated by `poly sync` (e.g. "../../bases/mycompany/api" = "mycompany/api")
```

`name`, `description`, `authors`, `requires-python`, and `packages` come from the root `pyproject.toml` and the `--name` / `--description` flags. `[tool.polylith.bricks]` is populated manually or by `poly sync`.

### Backend differences

| Build backend | Build hook in project       | Notes                                     |
|---------------|------------------------------|-------------------------------------------|
| Hatchling     | `hatch-polylith-bricks`      | Most common.                              |
| PDM           | `pdm-polylith-bricks`        |                                           |
| Poetry        | (no build hook)              | Uses `poetry-polylith-plugin` at runtime. |

## After creation
- Whenever imports change, run `poly sync` (load `polylith-sync`).
- Before a release / in CI, run `poly check` (load `polylith-check`).

## Notes for the agent
- **Always use `--quiet`.** AI agents cannot interact with `stdin` prompts and the process will hang indefinitely if `--quiet` is omitted.
- After creating the project with `--quiet`, you *can* link a base manually, but **it is not strictly required right away**. Empty projects are perfectly valid. If the user wants to add a base later, or if the base doesn't exist yet, simply leave the `[tool.polylith.bricks]` section empty for now.
- **Manual Base Linking Syntax:** When it's time to link a base manually, edit the `[tool.polylith.bricks]` section in `projects/<name>/pyproject.toml`. Check `workspace.toml` first to determine the `theme` and `namespace`.
  - For the **`loose`** theme (recommended): `"../../bases/<namespace>/<basename>" = "<namespace>/<basename>"` (e.g., `"../../bases/mycompany/api" = "mycompany/api"`).
  - For the **`tdd`** theme: `"../../bases/<basename>/src/<namespace>/<basename>" = "<namespace>/<basename>"` (e.g., `"../../bases/api/src/mycompany/api" = "mycompany/api"`).
- Components are never selected directly; they are pulled in transitively by the imports of the chosen base when you run `poly sync`.

## Verification
After creation, verify the project exists by checking `projects/<name>/pyproject.toml`. If the base already exists and the user wants it linked now, edit the `[tool.polylith.bricks]` section in that file to include the base, and then run `poly sync` to populate its transitive dependencies. Otherwise, the empty project is ready for development to proceed.
