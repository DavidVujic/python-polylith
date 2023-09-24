from pathlib import Path
from typing import Set, Union

from cleo.helpers import option
from poetry.console.commands.command import Command
from poetry.factory import Factory
from polylith import check, info, project, repo, workspace


class CheckCommand(Command):
    name = "poly check"
    description = "Validates the <comment>Polylith</> workspace."

    options = [
        option(
            long_name="strict",
            description="More strict checks when matching name of third-party libraries and imports",
            flag=True,
        ),
    ]

    def find_third_party_libs(self, path: Union[Path, None]) -> Set:
        project_poetry = Factory().create_poetry(path) if path else self.poetry

        if not project_poetry.locker.is_locked():
            raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

        packages = project_poetry.locker.locked_repository().packages

        return {p.name for p in packages}

    def print_report(self, root: Path, ns: str, project_data: dict) -> bool:
        is_verbose = self.option("verbose")
        is_quiet = self.option("quiet")
        is_strict = self.option("strict")

        path = project_data["path"]
        name = project_data["name"]

        try:
            third_party_libs = self.find_third_party_libs(path)
            res, details = check.report.create_report(
                root,
                ns,
                project_data,
                third_party_libs,
                is_strict,
            )

            if is_quiet:
                return res

            check.report.print_missing_deps(details["brick_diff"], name)
            check.report.print_missing_deps(details["libs_diff"], name)

            if is_verbose:
                check.report.print_brick_imports(details["brick_imports"])
                check.report.print_brick_imports(details["third_party_imports"])

            return res
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

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = [p for p in all_projects_data if info.is_project(p)]

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
