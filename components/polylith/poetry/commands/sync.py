from pathlib import Path

from poetry.console.commands.command import Command
from polylith import project, repo, sync, workspace


class SyncCommand(Command):
    name = "poly sync"
    description = "Update <comment>pyproject.toml</comment> with missing bricks."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())

        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        directory = self.option("directory")
        is_project = True if directory else False
        project_name = (
            project.get_project_name(self.poetry.pyproject.data) if is_project else None
        )

        ns = workspace.parser.get_namespace_from_config(root)

        diff = sync.calculate_difference(root, ns, project_name)
        packages = sync.to_packages(ns, diff["bases"], diff["components"], is_project)

        print(diff)
        print(packages)
        # if packages:
        # sync.update_project(directory or root, packages)
        return 0
