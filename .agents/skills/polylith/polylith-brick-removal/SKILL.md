---
name: polylith-brick-removal
description: Safely remove a Polylith brick (component or base) from the workspace. Use when the user wants to delete, remove, or tear down a component or base.
---

# Brick Removal Skill

> 💡 **Terminology:** this skill uses Polylith terms like *brick*, *component*, *base*, and *development project*. If they're unfamiliar, load `polylith-concepts` first.

There is no `poly remove` CLI command. Removing a brick is a manual process.

## Steps to remove a brick

1. **Delete the source code:**
   Delete the brick's directory under `components/<namespace>/<name>` or `bases/<namespace>/<name>`.
2. **Delete the tests:**
   Delete the brick's test directory under `test/components/<namespace>/<name>` or `test/bases/<namespace>/<name>`.
3. **Remove from projects:**
   Search across all `projects/*/pyproject.toml` files and remove the brick from the `[tool.polylith.bricks]` section.
4. **Remove from the development project:**
   Remove the brick from the `[tool.polylith.bricks]` section in the root `pyproject.toml` (the development project).
5. **Sync and Check:**
   Run `poly sync` (load `polylith-sync`) and `poly check` (load `polylith-check`) to ensure the workspace is valid and no other bricks were importing the deleted brick.

## Notes for the agent
- Always use your directory and file tools to verify the paths before deleting.
- If `poly check` fails after removal, it means another brick was depending on the removed brick. You must fix the importing brick.
