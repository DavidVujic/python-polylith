from pathlib import Path

from poetry.console.commands.command import Command
from polylith import check, project, repo


class CheckCommand(Command):
    name = "poly check"
    description = "Validates the <comment>Polylith</> workspace."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        projects = project.get_project_names_and_paths(root)

        res = [check.report.run(proj) for proj in projects]

        return 0 if all(res) else 1
