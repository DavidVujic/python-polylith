from pathlib import Path
from typing import List, Set

from poetry.console.commands.command import Command
from polylith import info, project, repo, workspace
from polylith.libs import report


def get_projects_data(root: Path, ns: str) -> List[dict]:
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)

    return info.get_bricks_in_projects(root, components, bases, ns)


def get_project_data(root: Path, ns: str, project_name: str) -> List[dict]:
    projects_data = get_projects_data(root, ns)

    filtered = next((p for p in projects_data if p["name"] == project_name), None)

    return [filtered] if filtered else projects_data


class LibsCommand(Command):
    name = "poly libs"
    description = "Show third-party libraries used in the workspace."

    def find_third_party_libs(self) -> Set[str]:
        packages = self.poetry.locker.locked_repository().packages

        return {p.name for p in packages if p.category == "main"}

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())

        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        if not self.poetry.locker.is_locked():
            raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

        third_party_libs = self.find_third_party_libs()

        ns = workspace.parser.get_namespace_from_config(root)

        project_name = project.get_project_name(self.poetry.pyproject.data)

        projects_data = get_project_data(root, ns, project_name)

        for project_data in projects_data:
            brick_imports = report.get_third_party_imports(root, ns, project_data)

            report.print_libs_summary(brick_imports, project_data["name"])
            report.print_libs_in_bricks(brick_imports)

            report.print_missing_installed_libs(
                brick_imports, third_party_libs, project_data
            )

        return 0
