from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands


class DiffCommand(Command):
    name = "poly diff"
    description = "Shows changed bricks compared to the latest git tag."

    options = [
        option(
            long_name="short",
            short_name="s",
            description="Print short view",
            flag=True,
        ),
        option(
            long_name="bricks",
            description="Print changed bricks",
            flag=True,
        ),
        option(
            long_name="since",
            description="Changed since a specific tag",
            flag=False,
        ),
    ]

    def handle(self) -> int:
        since = self.option("since")
        short = True if self.option("short") else False
        bricks = True if self.option("bricks") else False

        commands.diff.run(since, short, bricks)

        return 0
