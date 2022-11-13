from pathlib import Path

from poetry.console.commands.command import Command
from polylith import info, repo, workspace
from polylith.bricks import base, component


class InfoCommand(Command):
    name = "poly info"
    description = "Info about the <comment>Polylith</> workspace."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        ns = workspace.parser.get_namespace_from_config(root)
        bases_data = base.get_bases_data(root, ns)
        components_data = component.get_components_data(root, ns)
        projects_data = info.get_bricks_in_projects(root)

        info.print_workspace_summary(projects_data, bases_data, components_data)
        info.print_bricks_in_projects(projects_data, bases_data, components_data)

        return 0
