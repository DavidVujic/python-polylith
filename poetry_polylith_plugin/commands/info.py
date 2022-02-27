from pathlib import Path

from poetry.console.commands.command import Command
from poetry_polylith_plugin.components import bases, components, projects, repo, workspaces


class InfoCommand(Command):
    name = "poly info"
    description = "Info about the <comment>Polylith</> workspace."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        ns = workspaces.get_namespace_from_config(root)
        project_names = projects.get_project_names(root)
        components_data = components.get_components_data(root, ns)
        bases_data = bases.get_bases_data(root, ns)

        self.line(f"<comment>projects</>: {len(project_names)}")
        self.line(f"<comment>components</>: {len(components_data)}")
        self.line(f"<comment>bases</>: {len(bases_data)}")

        return 0
