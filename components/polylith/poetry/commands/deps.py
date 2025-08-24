from pathlib import Path
from cleo.helpers import option

from poetry.console.commands.command import Command
from polylith import commands, configuration, repo


class DepsCommand(Command):
    name = "poly deps"
    description = "Visualize the dependencies between <comment>bricks</>."

    options = [
        option(
            long_name="brick",
            description="Shows dependencies for selected brick",
            flag=False,
        ),
        option(
            long_name="save",
            description="Store the contents of this command to file",
            flag=True,
        ),
    ]

    def handle(self) -> int:
        directory = self.option("directory")
        brick = self.option("brick")
        save = self.option("save")

        root = repo.get_workspace_root(Path.cwd())
        ns = configuration.get_namespace_from_config(root)

        dir_path = Path(directory).as_posix() if directory else None

        options = {"directory": dir_path, "brick": brick, "save": save}
        commands.deps.run(root, ns, options)

        return 0
