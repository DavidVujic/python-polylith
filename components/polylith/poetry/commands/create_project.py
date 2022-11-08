from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith.poetry.commands.create import create
from polylith import project

command_name = "poly create project"


class CreateProjectCommand(Command):
    name = command_name
    description = "Creates a <comment>Polylith</> project."

    options = [
        option("name", None, "Name of the project.", flag=False),
    ]

    def handle(self) -> int:
        create(self, project.create_project)

        return 0
