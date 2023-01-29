from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith.bricks import base
from polylith.poetry.commands.create import create


class CreateBaseCommand(Command):
    name = "poly create base"
    description = "Creates a <comment>Polylith</> base."

    options = [
        option("name", None, "Name of the base.", flag=False),
        option(
            "description",
            None,
            "Description of the base.",
            flag=False,
            value_required=False,
        ),
    ]

    def handle(self) -> int:
        create(self, base.create_base)

        return 0
