from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import project
from polylith.poetry.commands.create import create

command_name = "poly create project"


class CreateProjectCommand(Command):
    name = command_name
    description = "Creates a <comment>Polylith</> project."

    options = [
        option("name", None, "Name of the project.", flag=False),
        option(
            "description",
            None,
            "Description of the project.",
            flag=False,
            value_required=False,
        ),
    ]

    def handle(self) -> int:
        create(self, project.create_project)

        return 0
