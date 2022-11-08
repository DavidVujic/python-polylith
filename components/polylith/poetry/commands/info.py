from pathlib import Path

from poetry.console.commands.command import Command
from polylith import project, repo, workspace
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
        project_names = project.get_project_names(root)
        components_data = component.get_components_data(root, ns)
        bases_data = base.get_bases_data(root, ns)

        self.line(f"<comment>projects</>: {len(project_names)}")
        self.line(f"<comment>components</>: {len(components_data)}")
        self.line(f"<comment>bases</>: {len(bases_data)}")

        return 0
