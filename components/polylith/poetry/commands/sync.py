from pathlib import Path
from typing import List

from poetry.console.commands.command import Command
from polylith import info, project, repo, sync, workspace


class SyncCommand(Command):
    name = "poly sync"
    description = "Update <comment>pyproject.toml</comment> with missing bricks."

    def filter_projects_data(self, all_projects_data: List[dict]) -> List[dict]:
        if self.option("directory"):
            project_name = project.get_project_name(self.poetry.pyproject.data)

            data = next(
                (p for p in all_projects_data if p["name"] == project_name), None
            )

            if not data:
                raise ValueError(f"Didn't find project in {self.option('directory')}")

            return [data]

        return all_projects_data

    def handle(self) -> int:
        is_verbose = self.option("verbose")
        is_quiet = self.option("quiet")

        root = repo.get_workspace_root(Path.cwd())
        ns = workspace.parser.get_namespace_from_config(root)

        bases = info.get_bases(root, ns)
        components = info.get_components(root, ns)
        workspace_data = {"bases": bases, "components": components}

        all_projects_data = info.get_bricks_in_projects(root, components, bases, ns)
        projects_data = self.filter_projects_data(all_projects_data)

        diffs = [
            sync.calculate_diff(root, ns, data, workspace_data)
            for data in projects_data
        ]

        for diff in diffs:
            sync.update_project(root, ns, diff)

            if is_quiet:
                continue

            sync.report.print_summary(diff)

            if is_verbose:
                sync.report.print_brick_imports(diff)

        return 0
