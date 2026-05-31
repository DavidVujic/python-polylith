---
name: migrate-analyze-imports
description: Analyze the project's import graph to identify files importing from the original namespace, potential circular imports, and symbols exported by the original namespace.
---

# Skill: migrate-analyze-imports

## Goal
Analyze the project's import graph to identify:
1. All files importing from the original namespace
2. Potential circular imports
3. Symbols exported by the original namespace

This information is used to guide the namespace migration and generate a compatibility shim.

## Inputs
- Project name (from `migration/<project-name>/state.md`)
- Original namespace (from `migration/<project-name>/state.md`)

## Steps

### 1. Identify files importing from the original namespace
1. Search for `from <original_namespace> import` and `import <original_namespace>` in all Python files in the project.
2. Record the file paths and import statements in `migration/<project-name>/import_analysis.md`.

### 2. Identify potential circular imports
1. Manually inspect the import graph to detect circular dependencies between the original namespace and the new base location.
2. Record any circular import chains in `migration/<project-name>/import_analysis.md`.

### 3. List symbols exported by the original namespace
1. Inspect the original namespace's `__init__.py` to list all public symbols (those not starting with `_`).
2. Record the exported symbols in `migration/<project-name>/import_analysis.md`.

## Output
- A report file: `migration/<project-name>/import_analysis.md` with:
  - Files importing from the original namespace
  - Circular import chains (if any)
  - Symbols exported by the original namespace

## Verify
1. Confirm that `migration/<project-name>/import_analysis.md` exists and is not empty.
2. Verify that the report includes:
   - A list of files importing from the original namespace
   - Any circular import chains
   - Symbols exported by the original namespace

## Commit
```bash
git add migration/<project-name>/import_analysis.md
git commit -m "migrate(<project-name>): phase 2 — analyze-imports"
```