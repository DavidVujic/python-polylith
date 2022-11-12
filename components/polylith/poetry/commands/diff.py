from pathlib import Path

from poetry.console.commands.command import Command
from polylith import repo


class DiffCommand(Command):
    name = "poly diff"
    description = "Shows changed bricks compared to the."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        return 0
