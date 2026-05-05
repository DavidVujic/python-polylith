---
name: polylith-dependency-visualization
description: Visualize **brick × brick** dependencies with `poly deps` — find circular dependencies, inspect a brick's public interface, and detect interface-bypass violations. Use for "what depends on what", "circular deps", "interface violation". For brick × project usage, use `polylith-workspace-inspection`.
---

# Dependency Visualization Skill

## Quick command

```bash
uv run poly deps
```

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> **`poly deps` vs `poly info`:**
> - `poly deps` → **brick × brick** (dependencies between bricks; interface compliance).
> - `poly info` → **brick × project** (which projects use which brick). Load `polylith-workspace-inspection`.
> ⚠ `poly deps` does **not** fail on warnings (circular deps, interface violations are informational). For pass/fail, use `poly check` (load `polylith-check`).

## Command reference

| Option         | Default | Description                                                                                  |
|----------------|---------|----------------------------------------------------------------------------------------------|
| `--brick`      | —       | Restrict output to the named brick.                                                          |
| `--interface`  | `false` | Show the brick's public interface and flag bricks that bypass it.                            |
| `--save`       | `false` | Persist the report to a file under the workspace's output dir.                               |
| `--directory`  | cwd     | Restrict analysis to projects whose path matches this directory.                             |

## Examples

```bash
# Full matrix
uv run poly deps

# One brick + interface compliance check
uv run poly deps --brick message --interface

# Save report
uv run poly deps --save
```

### Output format

```
                         d   g
                         a   r           m
                         t   e           e   s
                         a   e   k       s   c
                         b   t   a       s   h
                         a   i   f   l   a   e
                         s   n   k   o   g   m
  brick                  e   g   a   g   e   a
 ─────────────────────────────────────────────
  greeting               -   -   -   -   -   -
  kafka                  -   -   -   ✔   -   -
  message                ✔   -   ✔   -   -   ✔
  greet_api              -   ✔   -   ✔   -   -
```

`✔` = row brick imports column brick.

### Warning messages

```
ℹ brick_a is used by brick_b and also uses brick_a.        # circular
ℹ Found in brick_a: helloworld is not part of the public interface of brick_b.   # interface violation
```

## Fixing an interface violation

When `--interface` reports a violation:
1. Identify the offending import in the violating brick (e.g. `from <ns>.brick_b.internal import helloworld`).
2. Add `helloworld` to `<ns>/brick_b/__init__.py`:
   ```python
   from <ns>.brick_b.internal import helloworld
   ```
3. Update the importer to `from <ns>.brick_b import helloworld`.
4. Re-run `poly deps --interface` to confirm.

## Notes for the agent
- Circular deps usually mean two bricks share a concept that should be extracted into a third brick — flag this for the user; don't silently break the cycle by hiding imports.
