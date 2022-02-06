from cleo.helpers import option
from poetry.console.commands.command import Command
from poetry_polylith_plugin.commands.create import create
from poetry_polylith_plugin.components import components

command_name = "poly create component"


class CreateComponentCommand(Command):
    name = command_name
    description = "Creates a <comment>Polylith</> component."

    options = [
        option("name", None, "Name of the component.", flag=False),
    ]

    def handle(self) -> int:
        create(self, components.create_component)

        return 0
