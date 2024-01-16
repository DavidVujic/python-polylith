from pathlib import Path

from poetry.console.commands.command import Command
from polylith import commands, info, repo, workspace
from polylith.poetry.commands.check import command_options
from polylith.poetry.internals import filter_projects_data, find_third_party_libs


class LibsCommand(Command):
    name = "poly libs"
    description = "Show third-party libraries used in the workspace."

    options = command_options

    def print_report(self, root: Path, ns: str, data: dict) -> bool:
        name = data["name"]
        path = data["path"]

        options = {"strict": self.option("strict"), "alias": self.option("alias")}

        try:
            third_party_libs = find_third_party_libs(self.poetry, path)
            merged = {
                **data,
                **{"deps": {"items": third_party_libs, "source": "poetry.lock"}},
            }

            return commands.libs.run(root, ns, merged, options)
        except ValueError as e:
            self.line_error(f"{name}: <error>{e}</error>")
            return False

    def handle(self) -> int:
        directory = self.option("directory")
        root = repo.get_workspace_root(Path.cwd())
        ns = workspace.parser.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = filter_projects_data(self.poetry, directory, all_projects_data)

        results = {self.print_report(root, ns, data) for data in projects_data}

        return 0 if all(results) else 1
