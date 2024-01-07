from pathlib import Path
from typing import Union

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import project
from polylith.poetry.commands.create import create

command_name = "poly create project"


pyproject_template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = "{description}"
authors = {authors}
license = ""

packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""


def create_project(root: Path, _ns: str, name: str, description: Union[str, None]):
    project.create_project(root, pyproject_template, name, description or "")


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
        create(self, create_project)

        return 0
