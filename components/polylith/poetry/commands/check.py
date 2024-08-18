from functools import partial
from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands, configuration, info, repo
from polylith.poetry import internals

command_options = [
    option(
        long_name="strict",
        description="More strict checks when matching name and version of third-party libraries and imports.",
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

    def merged_project_data(self, project_data: dict) -> dict:
        name = project_data["name"]

        try:
            return internals.merge_project_data(project_data)
        except ValueError as e:
            self.line_error(f"{name}: <error>{e}</error>")
            return project_data

    def handle(self) -> int:
        root = repo.get_workspace_root(Path.cwd())
        dists_fn = partial(internals.distributions, root)

        options = {
            "verbose": True if self.option("verbose") else False,
            "short": False,
            "quiet": True if self.option("quiet") else False,
            "strict": True if self.option("strict") else False,
            "alias": self.option("alias") or [],
            "dists_fn": dists_fn,
        }

        directory = self.option("directory")
        ns = configuration.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        only_projects_data = [p for p in all_projects_data if info.is_project(p)]

        projects_data = internals.filter_projects_data(
            self.poetry, directory, only_projects_data
        )

        merged_projects_data = [
            self.merged_project_data(data) for data in projects_data
        ]

        results = {
            commands.check.run(root, ns, data, options) for data in merged_projects_data
        }

        libs_result = commands.check.check_libs_versions(
            projects_data, all_projects_data, options
        )

        return 0 if all(results) and libs_result else 1
