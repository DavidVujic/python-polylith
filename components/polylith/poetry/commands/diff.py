from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands
from polylith.poetry.commands import command_options


class DiffCommand(Command):
    name = "poly diff"
    description = "Shows changed bricks compared to the latest git tag."

    options = [
        command_options.short,
        command_options.since,
        option(
            long_name="bricks",
            description="Print changed bricks",
            flag=True,
        ),
        option(
            long_name="deps",
            description="Print bricks that depend on the changes. Use with --bricks.",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        since = self.option("since")

        options = {
            "short": self.option("short"),
            "bricks": self.option("bricks"),
            "deps": self.option("deps"),
        }

        commands.diff.run(since, options)

        return 0
