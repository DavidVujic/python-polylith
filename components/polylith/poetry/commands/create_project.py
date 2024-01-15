from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import project
from polylith.commands.create import create

command_name = "poly create project"


def create_project(root: Path, options: dict):
    package = options["package"]
    desc = options["description"] or ""

    project.create_project(root, project.templates.poetry_pyproject, package, desc)


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
        name = self.option("name")
        description = self.option("description")

        create(name, description, create_project)

        return 0
