from pathlib import Path

from poetry.console.commands.command import Command
from polylith import commands, configuration, info, repo
from polylith.poetry.internals import filter_projects_data


class SyncCommand(Command):
    name = "poly sync"
    description = "Update <comment>pyproject.toml</comment> with missing bricks."

    def handle(self) -> int:
        directory = self.option("directory")
        root = repo.get_workspace_root(Path.cwd())
        ns = configuration.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = filter_projects_data(self.poetry, directory, all_projects_data)

        options = {"verbose": self.option("verbose"), "quiet": self.option("quiet")}

        for data in projects_data:
            commands.sync.run(root, ns, data, options)

        return 0
