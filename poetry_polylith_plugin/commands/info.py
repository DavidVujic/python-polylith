from pathlib import Path

import tomlkit
from poetry.console.commands.command import Command
from poetry_polylith_plugin.components import repo, workspaces


def get_project_name(data):
    return data.get("tool", {}).get("poetry", {}).get("name")


def get_toml(path: Path) -> dict:
    with path.open() as f:
        return tomlkit.loads(f.read())


def get_project_files(path: Path):
    return path.glob("projects/**/*.toml")


def get_project_names(path):
    file_paths = get_project_files(path) or []
    tomls = (get_toml(p) for p in file_paths)

    return [get_project_name(d) for d in tomls]


def get_component_dirs(path: Path, top_dir):
    component_dir = path / top_dir

    return (f for f in component_dir.iterdir() if f.is_dir())


def dirs(path, ns, parent):
    return (f.name for f in path.glob(f"{parent}/{ns}/{path.name}") if f.is_dir())


def component_dirs(path: Path, ns: str):
    src_dirs = dirs(path, ns, "src")
    test_dirs = dirs(path, ns, "test")

    return {
        "name": path.name,
        "src": True if next(src_dirs, None) else False,
        "test": True if next(test_dirs, None) else False,
    }


def get_components_data(path: Path, ns: str):
    dirs = get_component_dirs(path, "components")

    return [component_dirs(d, ns) for d in dirs]


def get_bases_data(path: Path, ns: str):
    dirs = get_component_dirs(path, "bases")

    return [component_dirs(d, ns) for d in dirs]


class InfoCommand(Command):
    name = "poly info"
    description = "Info about the <comment>Polylith</> workspace."

    def handle(self) -> int:
        root = repo.find_workspace_root(Path.cwd())
        if not root:
            return 1  # TODO: send message about not finding the workspace

        ns = workspaces.get_namespace_from_config(root)
        project_names = get_project_names(root)
        components_data = get_components_data(root, ns)
        bases_data = get_bases_data(root, ns)

        self.line(f"<comment>projects</>: {len(project_names)}")
        self.line(f"<comment>components</>: {len(components_data)}")
        self.line(f"<comment>bases</>: {len(bases_data)}")

        return 0
