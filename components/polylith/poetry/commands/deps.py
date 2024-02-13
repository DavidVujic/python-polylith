from pathlib import Path

from poetry.console.commands.command import Command
from polylith import commands, configuration, repo


class DepsCommand(Command):
    name = "poly deps"
    description = "Visualize the dependencies between <comment>bricks</>."

    def handle(self) -> int:
        directory = self.option("directory")
        root = repo.get_workspace_root(Path.cwd())
        ns = configuration.get_namespace_from_config(root)

        dir_path = Path(directory).as_posix() if directory else None

        commands.deps.run(root, ns, dir_path)

        return 0
