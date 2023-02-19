from pathlib import Path
from typing import List, Set

from poetry.console.commands.command import Command
from polylith import info, libs, repo, workspace


def get_projects_data(root: Path, ns: str) -> List[dict]:
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)

    return info.get_bricks_in_projects(root, components, bases, ns)


def get_third_party_imports(
    root: Path, ns: str, projects_data: List[dict]
) -> dict[str, dict[str, Set]]:
    bases = {b for data in projects_data for b in data.get("bases", [])}
    components = {c for data in projects_data for c in data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    bases_imports = libs.get_third_party_imports(root, bases_paths)
    components_imports = libs.get_third_party_imports(root, components_paths)

    return {"bases": bases_imports, "components": components_imports}


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
            self.line_error(
                "<error>Error: poetry.lock not found. Run `poetry lock` to create"
                " it.</error>"
            )
            return 1

        third_party_libs = self.find_third_party_libs()

        ns = workspace.parser.get_namespace_from_config(root)
        projects_data = get_projects_data(root, ns)

        # TODO: filter out current project name from projects data,
        # to make sense when passing the --directory flag

        brick_imports = get_third_party_imports(root, ns, projects_data)

        bases_imports = set().union(*brick_imports.get("bases", {}).values())
        components_imports = set().union(*brick_imports.get("components", {}).values())

        diff = (
            set().union(bases_imports, components_imports).difference(third_party_libs)
        )

        from pprint import pprint

        pprint(bases_imports)
        pprint(components_imports)
        pprint(diff)

        return 0
