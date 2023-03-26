from pathlib import Path
from typing import Set, Union

from poetry.console.commands.command import Command
from poetry.factory import Factory
from polylith import info, project, repo, workspace
from polylith.libs import report


class LibsCommand(Command):
    name = "poly libs"
    description = "Show third-party libraries used in the workspace."

    def find_third_party_libs(self, path: Union[Path, None]) -> Set:
        project_poetry = Factory().create_poetry(path) if path else self.poetry

        if not project_poetry.locker.is_locked():
            raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

        packages = project_poetry.locker.locked_repository().packages

        return {p.name for p in packages}

    def print_report(self, root: Path, ns: str, data: dict) -> bool:
        name = data["name"]
        path = data["path"]

        brick_imports = report.get_third_party_imports(root, ns, data)

        report.print_libs_summary(brick_imports, data)
        report.print_libs_in_bricks(brick_imports)

        try:
            third_party_libs = self.find_third_party_libs(path)

            return report.print_missing_installed_libs(
                brick_imports, third_party_libs, name
            )
        except ValueError as e:
            self.line_error(f"{name}: <error>{e}</error>")
            return False

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())

        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        ns = workspace.parser.get_namespace_from_config(root)

        projects_data = info.get_projects_data(root, ns)

        if self.option("directory"):
            project_name = project.get_project_name(self.poetry.pyproject.data)

            data = next((p for p in projects_data if p["name"] == project_name), None)

            if not data:
                raise ValueError(f"Didn't find project in {self.option('directory')}")

            res = self.print_report(root, ns, data)
            result_code = 0 if res else 1
        else:
            results = {self.print_report(root, ns, data) for data in projects_data}

            result_code = 0 if all(results) else 1

        return result_code
