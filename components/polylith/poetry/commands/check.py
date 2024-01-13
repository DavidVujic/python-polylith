from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands, info, project, repo, workspace
from polylith.poetry import internals

command_options = [
    option(
        long_name="strict",
        description="More strict checks when matching name of third-party libraries and imports",
        flag=True,
    ),
    option(
        long_name="alias",
        description="alias for a third-party library, useful when an import differ from the library name",
        flag=False,
        multiple=True,
    ),
]


class CheckCommand(Command):
    name = "poly check"
    description = "Validates the <comment>Polylith</> workspace."

    options = command_options

    def print_report(self, root: Path, ns: str, project_data: dict) -> bool:
        path = project_data["path"]
        name = project_data["name"]

        options = {
            "verbose": True if self.option("verbose") else False,
            "quiet": True if self.option("quiet") else False,
            "strict": True if self.option("strict") else False,
            "alias": self.option("alias") or [],
        }

        try:
            third_party_libs = internals.find_third_party_libs(self.poetry, path)
            merged = {**project_data, **{"deps": third_party_libs}}

            return commands.check.run(root, ns, merged, options)
        except ValueError as e:
            self.line_error(f"{name}: <error>{e}</error>")
            return False

    def handle(self) -> int:
        specific_directory = self.option("directory")
        root = repo.get_workspace_root(Path.cwd())
        ns = workspace.parser.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = [p for p in all_projects_data if info.is_project(p)]

        if specific_directory:
            project_name = project.get_project_name(self.poetry.pyproject.data)
            data = next((p for p in projects_data if p["name"] == project_name), None)

            if not data:
                raise ValueError(f"Didn't find project in {specific_directory}")

            res = self.print_report(root, ns, data)
            return 0 if res else 1

        results = {self.print_report(root, ns, data) for data in projects_data}

        return 0 if all(results) else 1
