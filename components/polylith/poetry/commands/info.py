from pathlib import Path

from poetry.console.commands.command import Command
from polylith import info, repo, workspace


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
        bases = info.get_bases(root, ns)
        components = info.get_components(root, ns)
        projects_data = info.get_bricks_in_projects(root, components, bases, ns)

        info.print_workspace_summary(projects_data, bases, components)
        info.print_bricks_in_projects(projects_data, bases, components)

        return 0
