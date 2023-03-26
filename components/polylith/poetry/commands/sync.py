from pathlib import Path

from poetry.console.commands.command import Command
from polylith import repo


class SyncCommand(Command):
    name = "poly sync"
    description = (
        "Add missing bricks to the <comment>Polylith</> development pyproject.toml."
    )

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        self.line("Hello world from the poly sync command")

        return 0
