from functools import partial

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
        fn = partial(project.create_project, pyproject_template)

        create(self, fn)

        return 0
