---
name: migrate-split-big-component
description: "[Internal sub-skill of `migrate-orchestrator` (phase 5 of 11). Do not load directly — load `migrate-orchestrator` first, which drives all phases.] Split the big component (`components/<top_ns>/<INITIAL_BASE_NAME>/`) into multiple focused components."
---

# Skill: migrate-split-big-component

> 📐 **Scope vs sibling skills.** This skill operates **within one project** and turns *one component into many components*. Don't confuse with:
> - `migrate-extract-standalone-modules` — same scope (one project) but pulls *foundational modules* (`consts.py`, `exceptions.py`) out of the residual big component into their own standalone components.
> - `migrate-split-component-internals` — operates **inside one already-extracted component**, splitting its `core.py` into multiple files. No new components are created.
> - `migrate-isolate-shared-and-project-logic` — **cross-project** scope; identifies shared-vs-project-specific logic when migrating a 2nd+ project.
> - `migrate-dedupe` — opportunistic deduplication; this skill includes a dedup-analysis subsection so for a single project you usually don't need `migrate-dedupe` separately.

## Goal
Split the big component (`components/<top_ns>/<INITIAL_BASE_NAME>/`) into multiple focused components to improve maintainability, clarity, and reusability.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- `INITIAL_BASE_NAME`
- Verification commands.

From `migration/<PROJECT>/manifest.md`:
- Module map of the big component.

> All inputs from `state.md` are assumed to satisfy the validation rules in `migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### Phase 1: Plan the Split
1. **Review the Big Component**: Use `directory_tree` and `grep` to analyze the big component's structure and identify natural slices.
2. **Define Component Names**: Name components after the **domain or functionality** they represent (e.g., `domain_a_serializer`, `data_transformations`). Avoid generic names like `utils` or `helpers`.
3. **Create a Split Plan**: Record the following in `migration/<PROJECT>/split_plan.md`:
   - Brick name for each new component.
   - Files/modules to move into each component.
   - Public API (key functions/classes to export).
   - Bricks that will import from the new component.

**When NOT to Extract**:
- The module is tightly coupled to other modules in the component.
- The module is very small (< 20 lines) and extraction adds more indirection than value.

**Extraction Order**:
- Extract modules with **zero internal dependencies** first (e.g., `exceptions.py`, `consts.py`).
- Extract modules that depend on already-extracted modules next (e.g., `models.py` that imports `exceptions` and `consts`).

### Examples of Component Naming
Name components after the **domain or functionality** they represent:

| Original module name | Content (after inspection) | Component name |
|----------------------|----------------------------|----------------|
| `serializers.py`     | Serializes data for ERP | `domain_a_serializer` |
| `transformations/`   | Maps data between formats | `data_transformations` |
| `parsers.py`         | Parses event payloads | `event_parser` |
| `validators.py`      | Validates records | `record_validator` |

#### Avoiding circular imports when extracting modules

Extracting a module into a separate component can create circular imports if the new component imports from the parent component and the parent still imports from the new component. This commonly happens when a component's `__init__.py` eagerly imports from many submodules.

**Diagnosis:** The cycle typically looks like:

```
new_component.core → parent.__init__ → parent.submodule → new_component
```

Python triggers `parent.__init__` whenever any submodule of `parent` is imported (e.g. `from parent.consts import X` loads `parent/__init__.py` first).

**Resolution strategies (in order of preference):**

1. **Extract the circular part into its own component.** A circular dependency often signals that the code involved is isolated enough to be its own component. Extract the module that causes the cycle into a standalone component — this breaks the cycle structurally. A component doesn't have to be a "feature"; it can be a utility, a data definition, a pure technical module, or a single ORM model. If the code has a clear responsibility and can be imported without pulling in the rest of the parent, it belongs in its own brick.

   ```
   # Before (cycle): new_component → parent.consts → parent.__init__ → parent.handlers → new_component
   # After (no cycle): new_component → consts_component (standalone, no __init__ chain)
   ```

2. **Trim `__init__.py` exports.** Remove the problematic import from the parent's `__init__.py` and have callers import the submodule directly. This makes the dependency graph explicit and often eliminates the cycle without creating a new brick.

   ```python
   # Before: parent/__init__.py imports everything eagerly
   from parent.command_handler import CommandHandler  # triggers handler → new_component cycle
   
   # After: remove from __init__.py, callers import directly
   from parent.command_handler import CommandHandler  # in the base that needs it
   ```

3. **Standalone component instead of submodule.** If the new component would be a submodule of an existing package (e.g. `myns.models.example_transaction`), importing it triggers the parent package's `__init__.py` and all its eager imports. Make it a standalone component at the namespace level instead (e.g. `myns.example_transaction`).

4. **Deferred import (last resort).** Move the import inside the function that uses it. This works but hides the dependency and makes the code harder to reason about. Prefer strategies 1–3 first.

**Pre-flight check:** Before extracting a module, trace the import chain:
1. The new component imports `parent.submodule_X` → Python loads `parent.__init__`
2. Does `parent.__init__` (directly or transitively) import from the new component?
3. If yes → apply one of the strategies above (extract, trim, or restructure) before proceeding.

#### Refactoring shared infrastructure components

When a second project needs a component that already exists (e.g. `myns.logging`, `myns.kafka`), compare the implementations closely. Common refactoring patterns:

**Pattern: Parameterize the shared component.** When two implementations are 80%+ identical with project-specific extras, refactor the shared component to accept optional parameters rather than duplicating code.

Example — logging with project-specific loggers:
```python
# Shared component: myns.logging
def init(config, *, extra_loggers=None, cache_logger_on_first_use=False):
    loggers = {**_BASE_LOGGERS}
    loggers.update(_verbosity_overrides(config.LOG_VERBOSITY_LEVEL))
    if extra_loggers:
        loggers.update(extra_loggers)
    ...

# Project A base:
init(config, extra_loggers={"httpx": {...}, "backoff": {...}},
     cache_logger_on_first_use=config.LOG_CACHE_LOGGER_ON_FIRST_USE)

# Project B base:
init(config, extra_loggers={"confluent_kafka_helpers": {...}})
```

**When to parameterize vs. keep separate:**
- **Parameterize** when the core logic is identical and only data/config differs.
- **Keep separate** when the control flow or structure diverges (different frameworks, different patterns).
- **Extract shared base + project-specific wrappers** when there's a significant shared core but non-trivial project-specific logic around it.

#### Splitting Component Internals

Components with generic names like `models`, `schemas`, `exceptions`, or `consts` may start with a single `core.py` file. As the workspace grows, these components can accumulate code from different domains. Splitting `core.py` into multiple domain-focused modules **inside the component** can improve maintainability and clarity.

**When to Split:**
- If the `core.py` file contains definitions from multiple distinct domains (e.g., `domain_a` and `domain_b`).
- If the file contains helper/utility functions alongside class definitions.
- If preparing for a second project migration that will contribute to the same component.

**Approach:**
- Group definitions by the domain concept they serve.
- Name each module after the domain or functionality it represents (e.g., `domain_a.py`, `domain_b.py`).
- Ensure the public API remains unchanged to avoid breaking existing imports.

#### Cross-component duplication analysis

After drafting the split plan (but before executing any moves), analyze the planned components — and any _already existing_ components in the workspace — for duplication:

1. **Identify overlap:** For each planned component, check whether an existing component already contains similar logic. Look for:
   - Functions/classes with the same or very similar names.
   - Modules that operate on the same domain concept (e.g., two different `domain_a_serializer` implementations).
   - Copy-pasted utility functions (string helpers, date formatting, retry wrappers, etc.).

2. **Classify the overlap:**
   - **Identical or near-identical:** the code does the same thing with trivial differences (variable names, formatting). → Extract to a shared component.
   - **Same purpose, different behavior:** the code solves the same problem but with project-specific logic (e.g., different serialization schemas). → Keep separate, but extract any genuinely shared helpers.
   - **Coincidental similarity:** the code looks similar but serves unrelated purposes. → Leave separate.

3. **Propose shared extractions:** When genuinely duplicated code is found, add a step to the split plan:
   - Create a new shared component (or extend an existing one) containing the common logic.
   - Have both the existing and the new component depend on the shared one.
   - Record this in `<PROJECT>/split_plan.md` with a rationale.

4. **Always confirm with the user** before creating shared components — "is this code genuinely shareable?" is a judgment call that depends on how the projects will evolve.

### Phase 2: Execute the Split
For each planned component in `split_plan.md`:
1. **Create the Component**: Create the component directory with `__init__.py`.
2. **Move Files/Modules**: Move the relevant files/modules into the new component.
3. **Define the Public API**: Update `__init__.py` to re-export the public API.
4. **Update Callers**: Update all imports to reference the new component.
5. **Update `pyproject.toml`**: Add the new brick to the project's `[tool.polylith.bricks]`.
6. **Run Verification**: Ensure tests, linting, and type-checking pass.

## Verify
- `RUN_TEST_CMD` succeeds.
- If set, `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` succeed.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.
- Run `POLY_CMD_PREFIX sync` to synchronize the `[tool.polylith.bricks]` table with actual imports.

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| New component is named `utils`, `helpers`, `common`, or `misc` | Naming taken from old module names instead of the domain the code serves. | Rename to a domain-specific name (see the "Examples of Component Naming" table). Generic-named bricks attract more code and become the next big component. |
| Extracted component imports back into the residual via the residual's `__init__.py` | Circular import — see the "Avoiding circular imports" subsection above. | Apply strategies 1–3 from that subsection (extract the cyclic part, trim `__init__.py` exports, or restructure to standalone). Strategy 4 (deferred import) only as last resort. |
| `poly check` flags the newly extracted component as not used by any project | The project's base still imports from the residual path (`<TARGET_TOP_NS>.<INITIAL_BASE_NAME>.<x>`) instead of the new component. | Update the base's imports to the new component's public API, then `POLY_CMD_PREFIX sync --quiet` and re-run check. |
| Verification fails and you can't quickly diagnose | Phase commit not yet made. | `git reset --hard HEAD` to roll back to the previous phase's commit and consult the user. |

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase 5 — split-big-component"
```

Substitute `<PROJECT>`, `<N>`, and `<phase-name>` from `state.md` and the orchestrator's phase table. Do not proceed to the next phase without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.
