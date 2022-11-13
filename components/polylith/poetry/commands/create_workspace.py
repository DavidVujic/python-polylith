from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith.workspace.create import create_workspace


class CreateWorkspaceCommand(Command):
    name = "poly create workspace"
    description = "Creates a <comment>Polylith</> workspace in the current directory."

    options = [
        option(long_name="name", description="Name of the workspace.", flag=False),
        option(
            long_name="theme",
            description="Workspace theme",
            flag=False,
            default="tdd",
        ),
    ]

    def handle(self) -> int:
        path = Path.cwd()
        namespace = self.option("name")
        theme = self.option("theme")

        if not namespace:
            raise ValueError(
                "Please add a workspace name. Poetry poly create workspace --name myname"
            )

        create_workspace(path, namespace, theme)

        return 0
