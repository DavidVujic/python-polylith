from pathlib import Path
from typing import List, Set

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
            description="Print short view",
            flag=True,
        ),
        option(
            long_name="bricks",
            description="Print changed bricks",
            flag=True,
        ),
        option(
            long_name="since",
            description="Changed since a specific tag",
            flag=False,
        ),
    ]

    def has_partial_options(self) -> bool:
        return any(self.option(k) for k in {"bricks"})

    def print_partial_views(
        self,
        affected_projects: Set[str],
        bases: List[str],
        components: List[str],
    ) -> None:
        short = self.option("short")

        if short and not self.has_partial_options():
            diff.report.print_projects_affected_by_changes(affected_projects, short)

            return

        if self.option("bricks"):
            diff.report.print_detected_changes_in_bricks(bases, components, short)

    def print_views(self, root: Path, tag: str) -> None:
        ns = workspace.parser.get_namespace_from_config(root)
        files = diff.collect.get_files(tag)
        bases = diff.collect.get_changed_bases(files, ns)
        components = diff.collect.get_changed_components(files, ns)
        projects = diff.collect.get_changed_projects(files)
        all_projects_data = info.get_bricks_in_projects(root, components, bases, ns)
        projects_data = [p for p in all_projects_data if info.is_project(p)]

        affected_projects = diff.collect.get_projects_affected_by_changes(
            projects_data, projects, bases, components
        )

        short = self.option("short")

        if not short and not self.has_partial_options():
            diff.report.print_diff_summary(tag, bases, components)
            diff.report.print_detected_changes_in_projects(projects, short)
            diff.report.print_diff_details(projects_data, bases, components)

            return

        self.print_partial_views(affected_projects, bases, components)

    def handle(self) -> int:
        root = repo.get_workspace_root(Path.cwd())

        tag_name = self.option("since")
        tag = diff.collect.get_latest_tag(root, tag_name)

        if not tag:
            self.line("No tags found in repository.")
        else:
            self.print_views(root, tag)

        return 0
