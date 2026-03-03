from poetry.console.commands.command import Command
from polylith.commands.create import create


def try_create(command: Command, fn) -> int:
    name = command.option("name")
    description = command.option("description")

    try:
        create(name, description, fn)
    except ValueError as e:
        command.line_error(f"Did not create: <error>{e}</error>")

        return 1

    return 0
