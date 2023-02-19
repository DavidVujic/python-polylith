from pathlib import Path
from typing import List, Set

from poetry.console.commands.command import Command
from polylith import info, repo, workspace
from polylith.libs import report


def get_projects_data(root: Path, ns: str) -> List[dict]:
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)

    return info.get_bricks_in_projects(root, components, bases, ns)


class LibsCommand(Command):
    name = "poly libs"
    description = "Show third-party libraries used in the workspace."

    def find_third_party_libs(self) -> Set[str]:
        packages = self.poetry.locker.locked_repository().packages

        return {p.name for p in packages if p.category == "main"}

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())

        if not root:
            raise ValueError(
                "Didn't find the workspace root. Expected to find a workspace.toml file."
            )

        if not self.poetry.locker.is_locked():
            raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

        third_party_libs = self.find_third_party_libs()

        ns = workspace.parser.get_namespace_from_config(root)
        projects_data = get_projects_data(root, ns)

        # TODO: filter out current project name from projects data,
        # to make sense when passing the --directory flag

        brick_imports = report.get_third_party_imports(root, ns, projects_data)
        diff = report.calculate_diff(brick_imports, third_party_libs)

        from pprint import pprint

        pprint(diff)

        return 0
