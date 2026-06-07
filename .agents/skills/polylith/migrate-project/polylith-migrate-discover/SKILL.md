---
name: polylith-migrate-discover
description: "[Internal sub-skill of `polylith-migrate-orchestrator`. Do not load directly — load `polylith-migrate-orchestrator` first, which drives all phases.] Create `migration/<PROJECT>/state.md` and `migration/<PROJECT>/manifest.md` by inspecting the existing project under `projects/<PROJECT>/`."
---

# Skill: polylith-migrate-discover

## Goal
Inspect the project and create two artifacts that drive every subsequent migration phase:
- `migration/<PROJECT>/state.md` — a flat `KEY=value` file (see schema below).
- `migration/<PROJECT>/manifest.md` — a human-readable structural inventory.

> 💡 `<PROJECT>` is the project subfolder name (e.g., `api` for `projects/api/`). Use that exact string everywhere — paths, filenames, branch names.

## Canonical `state.md` schema

All later skills read `state.md` as a flat `KEY=value` file. Use **exactly** this format — no markdown tables, no fenced TOML, no inline comments. One key per line.

```ini
# migration/<PROJECT>/state.md
PROJECT_DIR=projects/<PROJECT>
ORIG_TOP_NS=<current import namespace>
TARGET_TOP_NS=<desired Polylith namespace, defaults to ORIG_TOP_NS>
INITIAL_BASE_NAME=<snake_case base name for the temporary migration base>
ALIAS=<short kebab-case alias for poly info/deps tables, or empty>
GROUP=<polylith project group, or empty>

PACKAGE_MANAGER=<poetry|pipenv|pip|uv|setuptools>
LINTER=<flake8|pylint|ruff|none>
FORMATTER=<black|isort|ruff|none>
TYPE_CHECKER=<mypy|pyright|ty|none>
POLY_CMD_PREFIX=<poetry poly|pipenv run poly|pdm run poly|hatch run poly|uv run poly|poly>
BRICK_IMPORT_MECHANISM=<editable-root|pytest-pythonpath|other — how the workspace exposes <TARGET_TOP_NS>.* bricks for import>

SHIM_STRATEGY=<shim|shimless — chosen in phase 2 (polylith-migrate-analyze-imports); may be empty at discover>

CONVERT_LINTER=<yes|no>
CONVERT_TYPE_CHECKER=<yes|no>
CONVERT_PACKAGE_MANAGER=<yes|no>

RUN_TEST_CMD=<full command to run tests>
RUN_LINT_CMD=<full command to run linting, or empty>
RUN_TYPECHECK_CMD=<full command to run type checking, or empty>

GIT_BRANCH=<migration branch name created in orchestrator Phase 0>
GIT_BASE_SHA=<commit SHA of the migration branch start point>
```

### Field reference

| Key | Description | Source |
|-----|-------------|--------|
| `PROJECT_DIR` | Project subfolder path. | The orchestrator's `<PROJECT>`. |
| `ORIG_TOP_NS` | Current top-level Python package name. | First non-`tests` directory under `projects/<PROJECT>/src/` or `projects/<PROJECT>/`. |
| `TARGET_TOP_NS` | Desired Polylith namespace. | `workspace.toml` `[tool.polylith].namespace`, or `ORIG_TOP_NS` if no workspace exists yet. |
| `INITIAL_BASE_NAME` | Name of the **single temporary base** used to hold all code during early phases. Becomes the **default base name** in `polylith-migrate-isolate-base-and-big-component`. Final migrations usually contain *several* bases — this is just the starting one. | Derived from `[project.name]`, confirmed by user. |
| `ALIAS` | Short alias shown in `poly info` / `poly deps` tables. Optional. | Derived, confirmed by user. |
| `GROUP` | Polylith project group. Optional. | Asked from user. |
| `PACKAGE_MANAGER` / `LINTER` / `FORMATTER` / `TYPE_CHECKER` | Detected tooling. | Detection table below. |
| `POLY_CMD_PREFIX` | Prefix every `poly …` command in later skills uses. | Derived from `PACKAGE_MANAGER`. |
| `BRICK_IMPORT_MECHANISM` | How the workspace makes `<TARGET_TOP_NS>.*` bricks importable for tests/dev. `editable-root` (root project is editable-installed; e.g. Hatch `dev-mode-dirs`), `pytest-pythonpath` (root `[tool.pytest.ini_options].pythonpath = ["bases","components","development"]`), or `other`. | Step 4: confirmed/established below. |
| `SHIM_STRATEGY` | `shim` or `shimless` — chosen in phase 2 (`polylith-migrate-analyze-imports`). May be empty at discover. | `polylith-migrate-analyze-imports`. |
| `CONVERT_*` | Whether the user opted in to a tooling conversion. | Asked from user. |
| `RUN_TEST_CMD` etc. | The exact shell commands the migration verifies against after each phase. | Derived from project config, confirmed by user if ambiguous. |
| `GIT_BRANCH` / `GIT_BASE_SHA` | Set by the orchestrator's Phase 0; recorded here so later skills know where to roll back to. | Orchestrator. |

### Deriving `INITIAL_BASE_NAME` and `ALIAS` from `[project.name]`

| `[project.name]`        | `INITIAL_BASE_NAME` (snake) | `ALIAS` (kebab) |
|-------------------------|-----------------------------|-----------------|
| `example-service-a`     | `example_a`                 | `svc-a`         |
| `order-management-api`  | `order_management`          | `order-mgmt`    |
| `payment-worker`        | `payment`                   | `payment`       |

### Validation rules

When any later phase loads `state.md`, validate before proceeding:

1. **File exists** at `migration/<PROJECT>/state.md`.
2. **Format**: every line is one of: blank, `# comment`, or `KEY=value`. No markdown tables, no fenced TOML, no inline comments after a value.
3. **Schema coverage**: every key from the schema above is present. A value may be empty (for optional keys), but the key line must exist.
4. **Enumerations**: `PACKAGE_MANAGER`, `LINTER`, `FORMATTER`, `TYPE_CHECKER`, `BRICK_IMPORT_MECHANISM`, `SHIM_STRATEGY` (when set), and the three `CONVERT_*` flags use only the documented values.
5. **Required non-empty**: `PROJECT_DIR`, `ORIG_TOP_NS`, `TARGET_TOP_NS`, `INITIAL_BASE_NAME`, `PACKAGE_MANAGER`, `POLY_CMD_PREFIX`, `BRICK_IMPORT_MECHANISM`, `RUN_TEST_CMD`, `GIT_BRANCH`, `GIT_BASE_SHA` must all be non-empty. (`SHIM_STRATEGY` may be empty until phase 2 sets it.)
6. **Consistency**: `POLY_CMD_PREFIX` matches `PACKAGE_MANAGER` per the mapping table.

If validation fails, abort the phase, surface the offending line(s) to the user, and ask them to fix `state.md` before retrying. Never silently coerce values.

## Steps

> Run these in order. Every step writes to `state.md` or `manifest.md`. Do not skip the confirmation gates (steps 4 and 7).

### 1. Record project metadata
Read `projects/<PROJECT>/pyproject.toml` (or `setup.cfg`/`setup.py`) and fill in `PROJECT_DIR`, `ORIG_TOP_NS`, `TARGET_TOP_NS`, and the **derived** `INITIAL_BASE_NAME`, `ALIAS` per the tables above.

### 2. Detect tooling
Scan project config files and fill in `PACKAGE_MANAGER`, `LINTER`, `FORMATTER`, `TYPE_CHECKER`:

| Tool | Detection criteria |
|------|--------------------|
| **Package Manager** | |
| Poetry      | `poetry.lock` or `[tool.poetry]` in `pyproject.toml` |
| Pipenv      | `Pipfile` or `Pipfile.lock` |
| Pip         | `requirements.txt` (no lock file) |
| UV          | `uv.lock` or `[tool.uv]` in `pyproject.toml` |
| Setuptools  | `setup.py` or `setup.cfg` only |
| **Linter** | |
| Flake8 | `setup.cfg`, `tox.ini` `[flake8]` section, or `.flake8` |
| Pylint | `[tool.pylint]` or `.pylintrc` |
| Ruff   | `[tool.ruff]` |
| **Formatter** | |
| Black  | `[tool.black]` |
| Isort  | `[tool.isort]` |
| Ruff   | `[tool.ruff.format]` |
| **Type Checker** | |
| Mypy    | `mypy.ini`, `.mypy.ini`, or `[tool.mypy]` |
| Pyright | `[tool.pyright]` or `pyrightconfig.json` |
| Ty      | `[tool.ty]` |

### 3. Derive `POLY_CMD_PREFIX`
Map `PACKAGE_MANAGER` to the command prefix:

| `PACKAGE_MANAGER` | `POLY_CMD_PREFIX` |
|-------------------|-------------------|
| `poetry`     | `poetry poly`     |
| `pipenv`     | `pipenv run poly` |
| `pdm`        | `pdm run poly`    |
| `hatch`      | `hatch run poly`  |
| `uv`         | `uv run poly`     |
| `pip` / `setuptools` / activated venv | `poly` |

### 4. Discover verification commands
1. **Check for Virtualenv**: Verify if the project has a virtualenv or if dependencies are installed. For example:
   - For `uv`: Check for `uv.lock` or `.venv`. If no virtualenv exists, guide the user to run `uv sync`.
   - For `pdm`: Run `pdm venv list` to check for a virtualenv. If none exists, guide the user to run `pdm install`.
   - For `poetry`: Run `poetry env list` to check for a virtualenv. If none exists, guide the user to run `poetry install`.
   - For `pip`: Check if a `venv` or `.venv` directory exists. If not, guide the user to create and activate one.

2. **Reconcile the Python version**: Compare the project's `requires-python` with the workspace's (`requires-python` in the **root** `pyproject.toml` and the root `.python-version`). If they disagree (e.g. project `>=3.13`, workspace `>=3.12`), the baseline test command can silently resolve the wrong interpreter. Resolve **before** establishing the baseline by either:
   - aligning the workspace (bump the root `requires-python` / `.python-version`) — confirm with the user, as it affects every project; or
   - recording a per-command interpreter override in the verification commands (e.g. `uv run --python 3.13 …`).

3. **Establish the brick-import mechanism**: Tests and entrypoints import bricks as `<TARGET_TOP_NS>.<brick>` from `bases/` and `components/`. Confirm the workspace actually exposes them — this is a prerequisite for `RUN_TEST_CMD` to work **after** code is moved into a base (phase 3+). Inspect the **root** `pyproject.toml`:
   - If the root project is editable-installed so the namespace resolves (e.g. Hatch `dev-mode-dirs = ["components","bases","development", …]` **and** the root is actually installed — *not* `[tool.uv] package = false`), set `BRICK_IMPORT_MECHANISM=editable-root`.
   - Otherwise add `pythonpath = ["bases","components","development"]` to the root `[tool.pytest.ini_options]` and set `BRICK_IMPORT_MECHANISM=pytest-pythonpath`.
   - Sanity-check in the workspace env: `<package-manager> run python -c "import <TARGET_TOP_NS>"` (once at least one brick exists, e.g. after phase 3). It must succeed.
   > ⚠ **Common trap:** a root `pyproject.toml` with both `dev-mode-dirs` **and** `[tool.uv] package = false` looks configured but installs nothing — `<TARGET_TOP_NS>.*` is then unimportable and **every** post-`extract-to-base` test run fails with `ModuleNotFoundError: No module named '<TARGET_TOP_NS>'`. Prefer `pytest-pythonpath` (it avoids changing the install model), or make the root installable.

4. **Verify `RUN_TEST_CMD`**: Run the test command in the project's directory to ensure it works.
   > ⚠ **You are executing untrusted code.** Running the project's tests and the
   > install/sync commands below executes arbitrary code from the project (e.g.
   > `setup.py`, `conftest.py`, build hooks) **and** from resolved third-party
   > packages (post-install scripts). Only run these on a project the user trusts;
   > do not proceed on an unknown or untrusted codebase.

   For example:
   - For `uv`: Run `uv run pytest tests --collect-only -q | tail -1`. If the command fails, guide the user to install test dependencies (e.g., `uv sync --extra tests`).
   - For `pdm`: Run `pdm run pytest tests --collect-only -q | tail -1`. If the command fails, guide the user to install test dependencies (e.g., `pdm install --group tests`).
   - For `poetry`: Run `poetry run pytest tests --collect-only -q | tail -1`. If the command fails, guide the user to install test dependencies (e.g., `poetry install --with tests`).
   - For `pip`: Run `python -m pytest tests --collect-only -q | tail -1`. If the command fails, guide the user to install test dependencies (e.g., `pip install -e ".[tests]"`).

5. **Record Baseline**: Record the baseline test count (e.g., number of tests collected) in `state.md`. If the command differs (e.g., `python -m pytest`), update `RUN_TEST_CMD` to match the working command.

6. **Inspect Config Files**: Inspect `Makefile`, `Justfile`, `tox.ini`, `pyproject.toml` `[tool.pytest.ini_options]`, and CI config (`.github/workflows/*.yml`, `.circleci/config.yml`, etc.) to identify the project's existing commands. Fill `RUN_TEST_CMD`, and `RUN_LINT_CMD` / `RUN_TYPECHECK_CMD` when present. If a command can't be found, leave the value empty.
   > 🔒 **Never store secrets in `state.md`.** `state.md` is committed. When a derived
   > command embeds a credential (an inline token, a `--token=…` flag, a database URL
   > with a password, an API key), do **not** copy the literal value. Reference the
   > environment variable name instead (e.g. `RUN_TEST_CMD=DATABASE_URL=$DATABASE_URL uv run pytest …`),
   > and have the user supply the secret via their environment at run time. Redact any
   > literal credential before writing the file. The same applies to `manifest.md` —
   > it captures structure, not secrets.

7. **Proceed Only After Verification**: Only proceed to the next phase if `RUN_TEST_CMD` succeeds. If it fails, guide the user to resolve the issue before continuing.

### 5. Determine tooling-conversion eligibility
Read the **workspace root** `pyproject.toml` to determine the workspace's standard linter, formatter, type checker, and package manager.

- If the project's `LINTER`/`FORMATTER` already matches the workspace's → set `CONVERT_LINTER=no` (skip).
- If the project's `TYPE_CHECKER` already matches the workspace's → set `CONVERT_TYPE_CHECKER=no` (skip).
- If the project's `PACKAGE_MANAGER` is already `uv` **and** the workspace uses uv → set `CONVERT_PACKAGE_MANAGER=no` (skip).
- If the workspace does **not** use uv, `polylith-migrate-convert-package-manager` does not apply at all — set `CONVERT_PACKAGE_MANAGER=no` and skip the question below.

### 6. Create `manifest.md`

Write `migration/<PROJECT>/manifest.md` using **exactly** this template — fixed headings, fixed shapes. Later phases parse this file by heading.

`````markdown
# migration/<PROJECT>/manifest.md

## Directory tree

<output of a `directory_tree` call on `projects/<PROJECT>/`, fenced as a code block>

## Module map

| Path | Role |
|------|------|
| `<relative path>` | <one-line description: "FastAPI route handlers", "Kafka consumer", "domain model", etc.> |

## Entrypoints

- `<path>`: <entrypoint type — FastAPI app / CLI main / Lambda handler / worker run / scheduled job>

## Tests

- Root: `<path>` (relative to project)
- File count: <n>
- Fixture files: `<path>`, `<path>`, …

## Infrastructure

- `<path>`: <type — Dockerfile / k8s manifest / Helm chart / alembic config / deploy script>
`````

> ⚠ Keep the five `##` headings literal. Downstream phases reference them by name; renaming a heading silently breaks input discovery.

### 7. Present derived values, then confirm with the user
**Do not proceed past this step without explicit user confirmation.** Present the derived state in one block:

```
Derived from projects/<PROJECT>/:
  INITIAL_BASE_NAME = <value>     ← initial base name; you will likely add more bases later
  ALIAS             = <value>     ← short alias for poly info/deps tables (optional)
  GROUP             = <value>     ← project group (optional)

Detected tooling:
  PACKAGE_MANAGER = <value>
  LINTER          = <value>
  FORMATTER       = <value>
  TYPE_CHECKER    = <value>

Verification commands:
  RUN_TEST_CMD       = <value>
  RUN_LINT_CMD       = <value or empty>
  RUN_TYPECHECK_CMD  = <value or empty>

Optional conversions you can opt into:
  - Convert linter/formatter to match workspace standard?     (default: no)
  - Convert type checker to match workspace standard?         (default: no)
  - Convert package manager to uv (workspace-uv only)?        (default: no)

Confirm the values above, or correct any of them.
```

Wait for the user's response. Update `state.md` with corrections and the `CONVERT_*` answers.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| Derived `INITIAL_BASE_NAME` collides with an existing brick under `bases/<TARGET_TOP_NS>/` or `components/<TARGET_TOP_NS>/` | Two projects derive the same base name from a generic `[project.name]`. | Append a project-specific suffix (e.g., `payment_api` instead of `payment`) and re-confirm with the user. Check before writing `state.md`. |
| Project has no detectable test command | No `pytest` / `make test` / CI config that reveals a runnable test command. | Ask the user explicitly. If none exists, set `RUN_TEST_CMD=` empty and record that **every later phase loses its primary safety check** — flag the heightened risk and, after each phase, verify that each base's entrypoint module imports cleanly and its wiring matches the original. |
| Multiple linters or formatters are configured simultaneously (e.g., black + ruff format both active) | Project history accumulated tools without a cleanup. | Record both in `state.md` (comma-separated values are acceptable in this one case), and flag for resolution during `polylith-migrate-convert-linter`. Do **not** silently pick one. |
| Baseline test command resolves the wrong Python (e.g. "incompatible with the project's Python requirement") | Project `requires-python` disagrees with the workspace root `requires-python` / `.python-version`. | Reconcile per step 4.2 — align the workspace version (confirm with user) or record a per-command `--python <X>` override in the verification commands. |
| `ModuleNotFoundError: No module named '<TARGET_TOP_NS>'` once code is in a base | The workspace doesn't expose bricks (e.g. root `[tool.uv] package = false` with `dev-mode-dirs` that never takes effect). | Establish `BRICK_IMPORT_MECHANISM` per step 4.3 — add a root pytest `pythonpath`, or make the root editable-installable. |

## Done When
The following artifacts and conditions all hold:

- [ ] `migration/<PROJECT>/state.md` exists and contains **every** key in the schema (empty values where N/A, but no missing keys).
- [ ] `migration/<PROJECT>/manifest.md` exists with all five sections (directory tree, module map, entrypoints, tests, infrastructure).
- [ ] The user has explicitly confirmed `INITIAL_BASE_NAME`, `ALIAS`, `GROUP`, and the three `CONVERT_*` flags.
- [ ] `RUN_TEST_CMD` is set and **runs successfully on the project's current code** (the migration's baseline pass-rate), with the Python version reconciled (step 4.2).
- [ ] `BRICK_IMPORT_MECHANISM` is set and the workspace can import `<TARGET_TOP_NS>.*` (step 4.3).
- [ ] `GIT_BRANCH` and `GIT_BASE_SHA` are populated (from orchestrator Phase 0).

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase <N> — discover"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
