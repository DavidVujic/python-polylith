---
name: polylith-testing
description: List Polylith bricks and projects affected by **test-code** changes since a git tag using `poly test diff`. Use for selective test runs in CI ("which tests do I need to run?"). For implementation-code diffs, use `polylith-diff` instead.
---

# Testing Skill

## Quick command

```bash
# Human-readable (default)
uv run poly test diff

# Pipe-friendly: comma-separated list of affected bricks (use this in scripts)
uv run poly test diff --short
```

> **Agent rule of thumb:** when the goal is to *do something* with the result (run pytest, drive CI), reach for `--short` first. The default output is for human readers.

**Command prefix:** If you do not know the package manager, list lock files with `ls uv.lock poetry.lock pdm.lock 2>/dev/null` (a `pyproject.toml` is always present, so it tells you nothing on its own). Use `uv run poly` (uv), `poetry poly` (poetry), `pdm run poly` (pdm), `hatch run poly` (hatch), or `poly` (activated venv). Examples below use `uv run`.

> ⚠ `poly test diff` **reports only** — it does not execute tests. Pipe its output into `pytest` / `unittest`.
> **`poly test diff` vs `poly diff`:**
> - `poly test diff` → which **test files** changed (drives test runs).
> - `poly diff` → which **brick implementations** changed (drives releases). Load `polylith-diff`.

## Tag selection
- Default: latest git tag matching `[tool.polylith.tag.patterns].stable` from `workspace.toml` (e.g. `stable-*`).
- `--since <ref>` — pin a tag/branch/commit. The output line `Test diff based on stable-4` shows the tag the CLI selected.

## Command reference

| Option       | Default             | Description                                                                                  |
|--------------|---------------------|----------------------------------------------------------------------------------------------|
| `--since`    | latest matching tag | Reference tag (or branch/commit) to diff against.                                            |
| `--short`    | `false`             | Pipe-friendly output: a comma-separated list of affected brick names — nothing else.         |
| `--bricks`   | `false`             | Print the affected bricks as a human-readable report (`⚙ Changes affecting <name>` lines).   |
| `--projects` | `false`             | Print the affected projects as a human-readable report.                                      |

> 💡 **For piping into `pytest` use `--short`.** It emits just the brick names separated by commas, with no headers, prefixes, or decoration — exactly what a script needs. `--bricks` is meant for humans reading the output.

## Examples

```bash
# Default: against latest stable-* tag
uv run poly test diff

# Pipe-friendly bricks list (best for scripts / agents)
uv run poly test diff --short

# Pin a tag, then pipe affected bricks into pytest
uv run poly test diff --since stable-4 --short

# Human-readable list of affected bricks
uv run poly test diff --bricks
```

### Sample output (default, no flags)

```
Projects and bricks affected by changes in tests
Test diff based on stable-4

Affected projects: 5
Affected components: 1
Affected bases: 0

  brick   consumer_project   message-api   aws lambda   my_fastapi_project   gcp function
 ────────────────────────────────────────────────────────────────────────────────────────
  log            ✔                ✔            ✔                ✔                 ✔
```

`✔` = the column project is affected by the row brick's test changes.

### Sample output (`--short`)

```
log,message
```

Just the brick names, comma-separated. No header, no prefix, no namespace. Empty result = no affected bricks.

### Sample output (`--bricks`)

`--bricks` is a human-readable variant; one line per affected brick:

```
⚙ Changes affecting log
⚙ Changes affecting message
```

Use `--short` instead when piping into another tool.

## Executing tests for affected bricks

> 💡 **Most common case — "I changed code, run the tests for it":** that's driven by `poly diff` (implementation diff), not `poly test diff`. Load `polylith-diff` for the canonical recipe; the same `pytest -k` pattern shown below works there.

`poly test diff` only reports — you drive the test runner yourself. The established Polylith pattern is to feed `--short` straight into `pytest -k`: brick names become an `or`-expression that pytest matches against test IDs, so you don't need to know the namespace, the theme, or whether each brick is a base or a component.

### Recommended flow

1. Capture `poly test diff --short`.
2. Replace the commas with ` or ` to form a pytest `-k` expression.
3. Pass it to `pytest -k`. Skip the call when the result is empty (no affected bricks).

### Shell one-liner (uv)

```bash
changes="$(uv run poly test diff --short)"
[ -n "$changes" ] && uv run pytest -k "${changes//,/ or }"
```

Example: `--short` outputs `log,message` → pytest is invoked as `pytest -k "log or message"`, which collects every test whose ID contains `log` or `message` (the brick directory name appears in the test path, so this matches both `test/components/<ns>/log/...` and `test/bases/<ns>/log/...` automatically).

### Caveat — substring matching

`pytest -k` matches **substrings** of test IDs, so a brick named `log` will also pull in tests whose name happens to contain `log` (e.g. tests for an unrelated brick called `logger` or a function `test_login`). If a brick name is short or generic and produces unwanted matches, fall back to passing explicit test directories instead.

## Running targeted tests for a single brick

If you are iteratively debugging or just created a single brick, you do not need to use `poly test diff`. You can run the test runner directly against the brick's test folder.

Check `workspace.toml` to determine the `theme` and `namespace`:
- For the **`loose`** theme (recommended): `pytest test/components/<namespace>/<basename>` or `pytest test/bases/<namespace>/<basename>`.
- For the **`tdd`** theme: `pytest components/<basename>/test` or `pytest bases/<basename>/test`.

## Notes for the agent
- Always exits 0 — informational, never a CI gate.
- If no matching tag exists and `--since` isn't passed, prints `No matching tags or commits found in repository.` and exits 0. Handle this in scripts.
