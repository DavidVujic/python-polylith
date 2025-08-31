from pathlib import Path

from poetry.console.commands.command import Command
from polylith import commands, configuration, repo
from polylith.poetry.commands import command_options


class InfoCommand(Command):
    name = "poly info"
    description = "Info about the <comment>Polylith</> workspace."

    options = [command_options.save, command_options.short]

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
