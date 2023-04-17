from pathlib import Path

from poetry.console.commands.command import Command
from polylith import info, project, repo, sync, workspace


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
        workspace_data = {"bases": bases, "components": components}

        if self.option("directory"):
            project_name = project.get_project_name(self.poetry.pyproject.data)

            data = next((p for p in projects_data if p["name"] == project_name), None)

            if not data:
                raise ValueError(f"Didn't find project in {self.option('directory')}")

            diffs = [sync.calculate_diff(root, ns, data, workspace_data)]
        else:
            diffs = [
                sync.calculate_diff(root, ns, data, workspace_data)
                for data in projects_data
            ]

        for diff in diffs:
            sync.report.print_summary(diff)
            sync.update_project(root, ns, diff)

        return 0
