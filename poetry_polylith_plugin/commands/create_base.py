from cleo.helpers import option
from poetry.console.commands.command import Command
from poetry_polylith_plugin.commands.create import create
from poetry_polylith_plugin.components import bases

command_name = "poly create base"


class CreateBaseCommand(Command):
    name = command_name
    description = "Creates a <comment>Polylith</> base."

    options = [
        option("name", None, "Name of the base.", flag=False),
    ]

    def handle(self) -> int:
        create(self, bases.create_base)

        return 0
