from functools import partial
from pathlib import Path

from poetry.console.commands.command import Command
from polylith import commands, configuration, info, repo
from polylith.poetry.commands import command_options
from polylith.poetry.internals import (
    distributions,
    filter_projects_data,
    merge_project_data,
)


class LibsCommand(Command):
    name = "poly libs"
    description = "Show third-party libraries used in the workspace."

    options = [
        command_options.alias,
        command_options.save,
        command_options.short,
        command_options.strict,
    ]

    def merged_project_data(self, project_data: dict) -> dict:
        name = project_data["name"]

        try:
            return merge_project_data(project_data)
        except ValueError as e:
            self.line_error(f"{name}: <error>{e}</error>")
            return project_data

    def handle(self) -> int:
        root = repo.get_workspace_root(Path.cwd())
        dists_fn = partial(distributions, root)
        save = self.option("save")

        output = configuration.get_output_dir(root, "libs") if save else None

        options = {
            "strict": self.option("strict"),
            "alias": self.option("alias"),
            "short": self.option("short"),
            "save": save,
            "output": output,
            "dists_fn": dists_fn,
        }

        directory = self.option("directory")
        ns = configuration.get_namespace_from_config(root)

        all_projects_data = info.get_projects_data(root, ns)
        projects_data = filter_projects_data(self.poetry, directory, all_projects_data)

        merged_projects_data = [
            self.merged_project_data(data) for data in projects_data
        ]

        results = commands.libs.run(root, ns, merged_projects_data, options)
        commands.libs.run_library_versions(projects_data, all_projects_data, options)

        return 0 if all(results) else 1
