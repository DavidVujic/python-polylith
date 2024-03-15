from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands, configuration, info, repo
from polylith.poetry.commands.check import command_options
from polylith.poetry.internals import filter_projects_data, find_third_party_libs


class LibsCommand(Command):
    name = "poly libs"
    description = "Show third-party libraries used in the workspace."

    options = command_options + [
        option(
            long_name="short",
            short_name="s",
            description="Display Workspace Info adjusted for many projects",
            flag=True,
        ),
    ]

    def print_report(self, root: Path, ns: str, data: dict, options: dict) -> bool:
        name = data["name"]
        path = data["path"]

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
        options = {
            "strict": self.option("strict"),
            "alias": self.option("alias"),
            "short": self.option("short"),
        }

        directory = self.option("directory")
        root = repo.get_workspace_root(Path.cwd())
        ns = configuration.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = filter_projects_data(self.poetry, directory, all_projects_data)

        results = {self.print_report(root, ns, data, options) for data in projects_data}

        commands.libs.library_versions(all_projects_data, projects_data, options)

        return 0 if all(results) else 1
