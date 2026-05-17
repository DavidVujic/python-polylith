---
name: discover
description: Create `migration/<PROJECT>/state.md` and `migration/<PROJECT>/manifest.md` by inspecting the existing project under `projects/<app>/`.
---

# Skill: discover

## Goal
Inspect the project and create `state.md` and `manifest.md` to guide the migration process.

## Steps

### 1. Record Project Metadata
Record the following in `migration/<PROJECT>/state.md`:

| Field | Description | Example |
|-------|-------------|---------|
| `PROJECT_DIR` | Project subfolder path | `projects/api` |
| `ORIG_TOP_NS` | Current import namespace | `myapp` |
| `TARGET_TOP_NS` | Desired Polylith namespace (default: `ORIG_TOP_NS`) | `myapp` |
| `BRICK_NAME` | Derived from `[project.name]` (ask user to confirm) | `example_a` |
| `ALIAS` | Short kebab-case alias for Polylith (ask user to confirm) | `svc-a` |
| `GROUP` | Optional project group (ask user) | `domain-a` |

#### Derive `BRICK_NAME` from `[project.name]`:
| `[project.name]` | `BRICK_NAME` |
|------------------|--------------|
| `example-service-a` | `example_a` |
| `order-management-api` | `order_management` |
| `payment-worker` | `payment` |

#### Derive `ALIAS` from `[project.name]`:
| `[project.name]` | `ALIAS` |
|------------------|---------|
| `example-service-a` | `svc-a` |
| `order-management-api` | `order-mgmt` |
| `payment-worker` | `payment` |

### 2. Detect Tools
Detect the project's package manager, linter, formatter, and type checker by scanning config files:

| Tool | Detection Criteria |
|------|--------------------|
| **Package Manager** | |
| Poetry | `poetry.lock` or `[tool.poetry]` in `pyproject.toml` |
| Pipenv | `Pipfile` or `Pipfile.lock` |
| Pip | `requirements.txt` (no lock file) |
| UV | `uv.lock` or `[tool.uv]` in `pyproject.toml` |
| Setuptools | `setup.py` or `setup.cfg` only |
| **Linter** | |
| Flake8 | `setup.cfg` or `.flake8` |
| Pylint | `[tool.pylint]` or `.pylintrc` |
| Ruff | `[tool.ruff]` |
| **Formatter** | |
| Black | `[tool.black]` |
| Isort | `[tool.isort]` |
| Ruff | `[tool.ruff]` |
| **Type Checker** | |
| Mypy | `mypy.ini` or `[tool.mypy]` |
| Pyright | `[tool.pyright]` or `pyrightconfig.json` |
| Ty | `[tool.ty]` |

Record the detected tools in `migration/<PROJECT>/state.md`:

```text
PACKAGE_MANAGER=<poetry|pipenv|pip|uv|setuptools>
LINTER=<flake8|pylint|ruff|none>
FORMATTER=<black|isort|ruff|none>
TYPE_CHECKER=<mypy|pyright|ty|none>
```

### 6. Determine `poly` Command Prefix

Based on the detected package manager, determine the correct command prefix for `poly`:

| Package Manager | `poly` Command Prefix | Example |
|-----------------|-----------------------|---------|
| Poetry | `poetry poly` | `poetry poly check` |
| Pipenv | `pipenv run poly` | `pipenv run poly sync` |
| Pip | `poly` | `poly info` |
| UV | `uv run poly` | `uv run poly check` |
| Setuptools | `poly` | `poly sync` |

Record the command prefix in `migration/<PROJECT>/state.md`:

```text
POLY_CMD_PREFIX=<poetry poly|pipenv run poly|poly|uv run poly>
```

### 3. Ask User for Preferences
- Ask the user if they want to convert the linter to `ruff` and the type checker to `ty`.
- Record their choices in `state.md`:
  ```text
  CONVERT_LINTER=<yes|no>
  CONVERT_TYPE_CHECKER=<yes|no>
  ```

### 4. Discover Commands
Look inside `projects/<app>/` for config files and record the following commands:
- `RUN_TEST_CMD`: Command to run tests.
- `RUN_LINT_CMD`: Command to run linting (optional).
- `RUN_TYPECHECK_CMD`: Command to run type checking (optional).

### 5. Create `manifest.md`
Record the following in `migration/<PROJECT>/manifest.md`:
- Directory tree of `projects/<app>/`.
- Module map (path + one-line description of role).
- Entrypoints (FastAPI app, CLI, worker, etc.).
- Test directory structure and count.
- Infrastructure files (Dockerfiles, k8s manifests, etc.).

## Done When
- `state.md` and `manifest.md` are created and populated.
- User confirms `BRICK_NAME`, `ALIAS`, and tooling preferences.
- All detected tools and commands are recorded.
