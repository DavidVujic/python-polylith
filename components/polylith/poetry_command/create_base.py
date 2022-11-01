from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith.poetry_command.create import create
from polylith import base


class CreateBaseCommand(Command):
    name = "poly create base"
    description = "Creates a <comment>Polylith</> base."

    options = [
        option("name", None, "Name of the base.", flag=False),
    ]

    def handle(self) -> int:
        create(self, base.create_base)

        return 0
