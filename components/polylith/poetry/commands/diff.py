from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import diff, info, repo


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
            files = diff.collect.get_files(tag)
            bases = diff.collect.get_changed_bases(root, files)
            components = diff.collect.get_changed_components(root, files)
            projects = diff.collect.get_changed_projects(files)
            projects_data = info.get_bricks_in_projects(root)

            short = self.option("short")

            if short:
                self.line(",".join(projects))
            else:
                diff.report.print_diff_summary(tag, bases, components)
                diff.report.print_detected_changes_in_projects(projects)
                diff.report.print_diff_details(projects_data, bases, components)

        return 0
