from pathlib import Path

from cleo.helpers import option
from poetry.console.commands.command import Command
from polylith import commands, configuration, diff, repo
from polylith.poetry.commands.diff import command_options


class TestDiffCommand(Command):
    name = "poly test diff"
    description = (
        "Shows the Polylith projects and bricks that are affected by changes in tests."
    )

    options = command_options + [
        option(
            long_name="bricks",
            description="Bricks affected by changes in tests",
            flag=True,
        ),
        option(
            long_name="projects",
            description="Projects affected by changes in tests",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        since = self.option("since")

        options = {
            "short": self.option("short"),
            "bricks": self.option("bricks"),
            "projects": self.option("projects"),
        }

        root = repo.get_workspace_root(Path.cwd())
        ns = configuration.get_namespace_from_config(root)

        tag = diff.collect.get_latest_tag(root, since) or since

        if tag:
            commands.test.run(root, ns, tag, options)
        else:
            self.line("No matching tags or commits found in repository.")

        return 0
