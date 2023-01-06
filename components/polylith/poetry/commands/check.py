from pathlib import Path

from poetry.console.commands.command import Command
from polylith import check, repo


class CheckCommand(Command):
    name = "poly check"
    description = "Validates the <comment>Polylith</> workspace."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        check.run_command(root)
        return 0
