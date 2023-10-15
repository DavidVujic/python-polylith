from pathlib import Path
from typing import List, Union

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import diff, info, repo, workspace


def opt(
    name: str, short: Union[str, None] = None, description: Union[str, None] = None
) -> dict:
    desc = description or f"Print changed {name}"

    defaults = {
        "long_name": name,
        "description": desc,
        "flag": True,
    }

    extra = {"short_name": short} if short else {}

    return {**defaults, **extra}


class DiffCommand(Command):
    name = "poly diff"
    description = "Shows changed bricks compared to the latest git tag."

    options = [
        option(**opt("short", short="s", description="Print short view")),
        option(**opt("projects")),
        option(**opt("bricks")),
    ]

    def has_partial_options(self) -> bool:
        return any(self.option(k) for k in {"projects", "bricks"})

    def print_partial_views(
        self, projects: list, bases: List[str], components: List[str]
    ) -> None:
        short = self.option("short")

        if short and not self.has_partial_options():
            diff.report.print_detected_changes_in_projects(projects, short)

            return

        if self.option("projects"):
            diff.report.print_detected_changes_in_projects(projects, short)

        if self.option("bricks"):
            diff.report.print_detected_changes_in_bricks(bases, components, short)

    def handle(self) -> int:
        root = repo.get_workspace_root(Path.cwd())
        tag = diff.collect.get_latest_tag(root)

        if not tag:
            self.line("No tags found in repository.")

            return 0

        ns = workspace.parser.get_namespace_from_config(root)
        files = diff.collect.get_files(tag)
        bases = diff.collect.get_changed_bases(files, ns)
        components = diff.collect.get_changed_components(files, ns)
        projects = diff.collect.get_changed_projects(files)
        all_projects_data = info.get_bricks_in_projects(root, components, bases, ns)
        projects_data = [p for p in all_projects_data if info.is_project(p)]

        short = self.option("short")

        if not short and not self.has_partial_options():
            diff.report.print_diff_summary(tag, bases, components)
            diff.report.print_detected_changes_in_projects(projects, short)
            diff.report.print_diff_details(projects_data, bases, components)
        else:
            self.print_partial_views(projects, bases, components)

        return 0
