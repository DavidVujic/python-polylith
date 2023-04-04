from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import diff, info, repo, workspace


class DiffCommand(Command):
    name = "poly diff"
    description = "Shows changed bricks compared to the latest git tag."

    options = [
        option(
            long_name="short",
            short_name="s",
            description="Print only changed projects",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        tag = diff.collect.get_latest_tag(root)

        if not tag:
            self.line("No tags found in repository.")
        else:
            ns = workspace.parser.get_namespace_from_config(root)
            files = diff.collect.get_files(tag)
            bases = diff.collect.get_changed_bases(files, ns)
            components = diff.collect.get_changed_components(files, ns)
            projects = diff.collect.get_changed_projects(files)
            all_projects_data = info.get_bricks_in_projects(root, components, bases, ns)
            projects_data = [p for p in all_projects_data if info.is_project(p)]

            short = self.option("short")

            if short:
                diff.report.print_short_diff(projects_data, projects, bases, components)
            else:
                diff.report.print_diff_summary(tag, bases, components)
                diff.report.print_detected_changes_in_projects(projects)
                diff.report.print_diff_details(projects_data, bases, components)

        return 0
