from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith.bricks import component
from polylith.poetry.commands.create import create


class CreateComponentCommand(Command):
    name = "poly create component"
    description = "Creates a <comment>Polylith</> component."

    options = [
        option("name", None, "Name of the component.", flag=False),
        option(
            "description",
            None,
            "Description of the component.",
            flag=False,
            value_required=False,
        ),
    ]

    def handle(self) -> int:
        create(self, component.create_component)

        return 0
