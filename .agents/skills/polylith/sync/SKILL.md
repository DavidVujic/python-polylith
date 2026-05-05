---
name: polylith-sync
description: Run `poly sync` to update each project's `[tool.polylith.bricks]` table with the bricks actually imported. Use this whenever a brick is added, removed, or its imports change — and before `poly check` or a release.
---

# Sync Skill

> 💡 **Terminology:** this skill uses Polylith terms like *brick*, *project*, and *development project*. If they're unfamiliar, load `polylith-concepts` first.

## Quick command

```bash
uv run poly sync --quiet
```

> ⚠ **Agents must pass `--quiet`.** `poly sync` has an interactive mode that will prompt on stdin and **hang the process** if no human is attached. `--quiet` suppresses output *and* disables the interactive prompts. **Never use `--verbose`** in an agent run — it is the opposite of `--quiet` and can trigger interactive mode. Save `--verbose` for humans who are debugging at a terminal.

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

## When to run
- After `poly create base` / `poly create component` — registers the new brick in the development project.
- After `poly create project` — only if the interactive prompt was skipped.
- After adding a new `import` between bricks — picks up the transitively pulled-in brick.
- Before `poly check` and before any release/CI run.

> ⚠ `poly sync` **adds** missing bricks but does **not** remove unused ones. Stale entries in `[tool.polylith.bricks]` must be deleted by hand. It also does not sync third-party libraries — use `poly libs` / `poly check` for those.

## What it does
- **Per project under `projects/`:** resolves the project's base(s), walks the import graph, and adds any imported brick missing from `[tool.polylith.bricks]`.
- **For the development project (root `pyproject.toml`):** always lists every base and every component in the workspace.

## Command reference

| Option         | Default | Description                                                                                                                |
|----------------|---------|----------------------------------------------------------------------------------------------------------------------------|
| `--directory`  | cwd     | Sync only projects whose path matches this directory.                                                                      |
| `--quiet`      | `false` | Suppress all output **and** disable interactive prompts. Exit code unchanged. **Required for agent runs.**                 |
| `--verbose`    | `false` | Print detailed information about each sync operation. **Can trigger interactive mode** — for human/terminal use only.      |

## Examples

```bash
# Agent / CI default — non-interactive, no output
uv run poly sync --quiet

# Agent: only one project, still non-interactive
uv run poly sync --quiet --directory projects/user_api

# Human, at a terminal: verbose for debugging missing bricks (may prompt!)
uv run poly sync --verbose
```

### Output

Nothing changed:
```
✔ project-a
✔ project-b
✔ development
```

A brick was added:
```
👉 the-cli
adding greeting component to the-cli
```

## Notes for the agent
- **Always run with `--quiet`.** Without it, `poly sync` may drop into an interactive prompt and hang the process — agents cannot answer stdin prompts. Never combine with `--verbose`, which leans the other way and can trigger interactive mode.
- The exit code is always 0 — `poly sync` is informational, not a gate. For a CI gate, follow it with `poly check` (load `polylith-check`).
- If a brick is showing up in unexpected projects after sync, it's because *something the project's base imports* (transitively) imports that brick. Trace it with `poly deps --brick <name>` (load `polylith-dependency-visualization`).
- **Git reminder:** If `poly sync` adds missing bricks to any `pyproject.toml` files, use your git tools to review the diff and ensure those changes are committed. Because `--quiet` suppresses output, the agent should rely on `git diff` (or re-run `poly info`) to confirm what changed.

## Background — the development project

The root `pyproject.toml` doubles as a "development project": a single virtual environment that includes every brick and every dependency (production *and* dev-only). The `development/` directory holds REPL scripts and notebooks that import bricks freely. `poly sync` keeps the development project complete by listing every brick in the workspace there. Per-project `pyproject.toml`s under `projects/` only list the bricks each project actually uses.

## Verification
After running `poly sync`, verify the changes by inspecting the `[tool.polylith.bricks]` section in the relevant `projects/<name>/pyproject.toml` or the root `pyproject.toml` to ensure the new bricks were added. Alternatively, run `poly info` (load `polylith-workspace-inspection`) to see the updated matrix.
