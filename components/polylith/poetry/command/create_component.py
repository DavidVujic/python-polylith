from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith.poetry.command.create import create
from polylith import component


class CreateComponentCommand(Command):
    name = "poly create component"
    description = "Creates a <comment>Polylith</> component."

    options = [
        option("name", None, "Name of the component.", flag=False),
    ]

    def handle(self) -> int:
        create(self, component.create_component)

        return 0
