from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands, configuration, repo


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
        option(
            long_name="save",
            description="Store the contents of this command to file",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        short = True if self.option("short") else False
        save = self.option("save")

        root = repo.get_workspace_root(Path.cwd())
        output = configuration.get_output_dir(root, "info") if save else None

        options = {
            "short": short,
            "save": save,
            "output": output,
        }
        commands.info.run(root, options)

        return 0
