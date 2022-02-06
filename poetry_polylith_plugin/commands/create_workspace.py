from pathlib import Path

from cleo.helpers import option

from poetry.console.commands.command import Command
from poetry_polylith_plugin.components import workspaces


command_name = "poly create workspace"


class CreateWorkspaceCommand(Command):
    name = command_name
    description = "Creates a <comment>Polylith</> workspace in the current directory."

    options = [
        option("name", None, "Name of the workspace.", flag=False),
    ]

    def handle(self) -> int:
        path = Path.cwd()
        namespace = self.option("name")

        if not namespace:
            raise ValueError(
                "Please add a workspace name. Poetry poly create workspace --name myname"
            )

        workspaces.create_workspace(path, namespace)

        return 0
