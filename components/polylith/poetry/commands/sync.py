from pathlib import Path

from poetry.console.commands.command import Command
from polylith import project, repo, sync


class SyncCommand(Command):
    name = "poly sync"
    description = "Update <comment>pyproject.toml</comment> with missing bricks."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())

        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        project_name = (
            project.get_project_name(self.poetry.pyproject.data)
            if self.option("directory")
            else None
        )

        res = sync.calculate_difference(root, project_name)

        print(res)
        return 0
