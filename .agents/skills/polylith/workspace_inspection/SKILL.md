---
name: polylith-workspace-inspection
description: Show **brick × project usage** with `poly info` — which projects use which bricks, plus workspace counts. Use for "workspace overview", "which projects use X", "find orphaned bricks". For brick-to-brick dependencies, use `polylith-dependency-visualization`.
---

# Workspace Inspection Skill

## Quick command

```bash
uv run poly info
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> **`poly info` vs `poly deps`:**
> - `poly info` → **brick × project** (which project uses which brick).
> - `poly deps` → **brick × brick** (which brick uses which brick). Load `polylith-dependency-visualization`.
> 💡 A brick that is `-` in every project except `development` is **orphaned in production** — flag it for the user.

## Command reference

| Option        | Default | Description                                                                                                     |
|---------------|---------|-----------------------------------------------------------------------------------------------------------------|
| `--short`     | `false` | Compact view — for workspaces where the full matrix doesn't fit.                                                |
| `--save`      | `false` | Persist the report to a file under the workspace's output dir.                                                  |
| `--group`     | —       | Show only projects in the named group(s) (comma-separated), defined in `[tool.polylith.projects.groups]`.       |

## Examples

```bash
# Full matrix
uv run poly info

# Compact summary
uv run poly info --short

# Filter to a project group
uv run poly info --group hooks
```

### Sample output

```
Workspace summary
projects: 6  components: 7  bases: 5  development: 1

  brick           consumer   message-api   aws lambda   fastapi   gcp fn   development
 ──────────────────────────────────────────────────────────────────────────────────────
  greeting           -            -             ✔          ✔        ✔          ✔
  kafka              ✔            ✔             -          -        -          ✔
  log                ✔            ✔             ✔          ✔        ✔          ✔
  greet_api          -            -             -          ✔        -          ✔
  message_api        -            ✔             -          -        -          ✔
```

- Rows are bricks; columns are projects (rightmost = development).
- `✔` = the brick is used by that project; `-` = not used.
- The `development` column should be `✔` for every brick (enforced by `poly sync`); a `-` there means a brick was created but isn't yet known to the development project.

## Notes for the agent
- `poly info` exits 0 — it's a report, not a gate.
- For wide workspaces, prefer `--short` or `--group <name>`.
- To turn this report into action: cross-reference orphans (only `development = ✔`) with `poly deps --brick <name>` to confirm nothing imports them, then propose deletion to the user.
