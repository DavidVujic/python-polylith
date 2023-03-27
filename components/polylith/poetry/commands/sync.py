from pathlib import Path

from poetry.console.commands.command import Command
from polylith import info, project, repo, workspace


class SyncCommand(Command):
    name = "poly sync"
    description = "Update <comment>pyproject.toml</comment> with missing bricks."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())

        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        ns = workspace.parser.get_namespace_from_config(root)

        bases = info.get_bases(root, ns)
        components = info.get_components(root, ns)

        projects_data = info.get_bricks_in_projects(root, components, bases, ns)

        if self.option("directory"):
            project_name = project.get_project_name(self.poetry.pyproject.data)

            data = next((p for p in projects_data if p["name"] == project_name), None)
        else:
            data = next((p for p in projects_data if not info.is_project(p)))

        if not data:
            raise ValueError("Didn't find the project.")

        components_diff = set(components).difference(data["components"])
        bases_diff = set(bases).difference(data["bases"])

        print(components_diff)
        print(bases_diff)

        return 0
