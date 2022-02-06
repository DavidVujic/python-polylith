from cleo.helpers import option
from poetry.console.commands.command import Command
from poetry_polylith_plugin.commands.create import create
from poetry_polylith_plugin.components import projects

command_name = "poly create project"


class CreateProjectCommand(Command):
    name = command_name
    description = "Creates a <comment>Polylith</> project."

    options = [
        option("name", None, "Name of the project.", flag=False),
    ]

    def handle(self) -> int:
        create(self, projects.create_project)

        return 0
