---
name: polylith-migrate-dedupe
description: "[Internal sub-skill of `polylith-migrate-orchestrator` (optional, runs only when opted in during `polylith-migrate-discover`). Do not load directly — load `polylith-migrate-orchestrator` first.] Identify and execute controlled deduplication of code during migration (if the user opts in)."
---

# Skill: polylith-migrate-dedupe

> 📐 **Scope vs sibling skills.** This skill is **opportunistic deduplication** that may be triggered any time during refactoring when duplication candidates surface. It is **not** the canonical place for the structural decompositions:
> - For "split this big component into smaller ones", use `polylith-migrate-split-big-component` (it already includes a dedup-analysis subsection — usually sufficient on a first migration).
> - For "this component's `core.py` mixes domains", use `polylith-migrate-split-component-internals`.
> - For "two projects have overlapping code, split shared from project-specific", use `polylith-migrate-isolate-shared-and-project-logic`.
>
> Use `polylith-migrate-dedupe` when none of the above fits cleanly — e.g., duplication discovered across already-extracted components that don't map to a structural split.

## Goal
Identify duplication candidates during the migration process and execute controlled deduplication for user-approved candidates.

## When to Use
- After splitting the big component or extracting standalone modules.
- When potential duplication between components is suspected.

## Classification

Use this table when deciding whether a candidate is a real duplicate:

| Class | Definition | Action |
|-------|------------|--------|
| **Identical** | Same logic, same control flow, only trivial differences (variable names, formatting, ordering of independent statements). | Extract into a shared component. Both call sites import from it. |
| **Similar** | Same purpose, slightly different behaviour (e.g., different default arguments, project-specific fields on an otherwise shared model). | Extract a **parameterized** shared component. Project-specific behaviour passes in as arguments or subclass hooks. Avoid forcing a one-size-fits-all signature. |
| **Coincidental** | Looks similar (same function name, same shape) but serves unrelated purposes. | Leave alone. Sharing here would couple two domains that should evolve independently. |

## When to parameterize vs. keep separate

- **Parameterize** when the core logic is identical and only data/config differs.
- **Keep separate** when control flow or structure diverges (different frameworks, different patterns) — forcing a shared abstraction here creates a brittle "shared core" that grows project-specific flags over time.
- **Extract shared base + per-project wrappers** when there's a significant shared core but non-trivial project-specific logic around it.

### Worked example — logging

Two projects each had their own `init_logging`. The core (structlog setup, base log levels, JSON formatter) was identical; the differences were:

- Project A added loggers for `httpx`, `backoff`.
- Project B added a logger for `confluent_kafka_helpers`.

The shared component exposed an `init(config, *, extra_loggers=None, cache_logger_on_first_use=False)` function. Each project's base calls `init` with its own `extra_loggers` dict. No coincidental coupling, no version skew, and adding a third project requires only its own dict — not a change to the shared component.

## Shared-component naming

When creating a shared component to deduplicate code, name it after the **domain or capability** it represents, never after how it's used. Good: `logging`, `kafka_client`, `merchant_serializer`. Bad: `shared_utils`, `common`, `helpers`, `misc`. Generic-named bricks attract more code over time and become the next thing that needs decomposing.

## Inputs
From `migration/<PROJECT>/state.md`:
- `TARGET_TOP_NS`
- Verification commands (`RUN_TEST_CMD`, `RUN_LINT_CMD`, `RUN_TYPECHECK_CMD`).

From `migration/<PROJECT>/manifest.md`:
- Module map of components.

> All inputs from `state.md` are assumed to satisfy the validation rules in `polylith-migrate-discover` (`### Validation rules`). Validate before proceeding.

## Steps

### 1. Identify Duplication Candidates
- Use `directory_tree` and `grep` to scan for overlapping logic between components.
- Classify candidates by type:
  - **Identical**: Code that is exactly the same.
  - **Similar**: Code that serves the same purpose but with minor differences.
  - **Coincidental**: Code that looks similar but serves unrelated purposes.

### 2. Present Candidates to the User
- Provide a list of duplication candidates, including:
  - Component names.
  - File paths.
  - Type of duplication (identical, similar, coincidental).
  - Risk assessment (low, medium, high).
- Ask the user to approve or reject each candidate for deduplication.

### 3. Execute Deduplication for Approved Candidates
- For each approved candidate:
  - **Identical Code**: Extract the shared logic into a new component and update imports.
  - **Similar Code**: Refactor to use shared logic or parameterize differences.
  - **Coincidental Code**: Leave as-is.
- Update `pyproject.toml` to include any new components.
- Run `POLY_CMD_PREFIX sync` to synchronize the workspace.

### 4. Verify Changes
- Run `RUN_TEST_CMD` to ensure no regressions.
- Run `RUN_LINT_CMD` and `RUN_TYPECHECK_CMD` if set.
- Run `POLY_CMD_PREFIX check` to validate the workspace structure.

## Verify
- All tests pass (`RUN_TEST_CMD`).
- Linting and type-checking pass (if set).
- The workspace structure is valid (`POLY_CMD_PREFIX check`).

## Common failure modes

| Symptom | Likely cause | Remediation |
|---------|--------------|-------------|
| Two pieces of code look identical but operate on different domains (e.g., both are `validate(...)` but one is for users, the other for transactions) | Coincidental similarity, not real duplication. | Classify as "coincidental"; leave both in place. Resist the urge to share. |
| The candidate shared component would pull in framework-specific dependencies (e.g., a "logging" shared brick that needs both `confluent_kafka_helpers` and `httpx`) | Wrong shared abstraction — you're sharing the union of two project surfaces. | Revert and parameterize instead: keep the shared core minimal and pass project-specific values as arguments. See the "Pattern: Parameterize the shared component" guidance in `polylith-migrate-split-big-component`. |
| Tests break after deduplication because `mock.patch("<old.path>")` no longer hits anything | Patch strings reference the pre-dedup module path. | Update patch strings to the new shared module path. Validate by deliberately breaking the patched function and confirming the test fails. |

## Done When
- Duplication candidates are identified and presented to the user.
- User-approved candidates are deduplicated.
- All tests and checks pass.
- The workspace structure is valid.

## Commit

After verification passes, commit this phase to the migration branch:

```bash
git add -A && git commit -m "migrate(<PROJECT>): phase optional — dedupe"
```

Substitute `<PROJECT>` from `state.md`. This is an **optional** skill off the numbered main line, so the commit uses the literal `phase optional` label (no `<N>`). Do not proceed without a clean commit — the per-phase commit is the rollback point for the next phase's failure-mode tables.