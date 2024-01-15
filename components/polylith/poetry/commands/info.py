from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands


class InfoCommand(Command):
    name = "poly info"
    description = "Info about the <comment>Polylith</> workspace."

    options = [
        option(
            long_name="short",
            short_name="s",
            description="Display Workspace Info adjusted for many projects",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        short = True if self.option("short") else False

        commands.info.run(short)

        return 0
