import subprocess
from pathlib import Path

from poetry.console.commands.command import Command
from polylith import repo, workspace


class DiffCommand(Command):
    name = "poly diff"
    description = (
        "Shows changed bricks compared to the latest git tag."
    )

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        tag_pattern = workspace.parser.get_git_tag_pattern_from_config(root)
        res = subprocess.run(
            ["git", "tag", "-l", "--sort=-committerdate", f"{tag_pattern}"],
            capture_output=True,
        )
        self.line
        latest_tag = next((tag for tag in res.stdout.decode("utf-8").split()), None)

        self.line(f"TAG: {latest_tag}")

        return 0
