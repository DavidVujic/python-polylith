from pathlib import Path
from typing import Union
from polylith import repo, workspace


def create(name: Union[str, None], description: Union[str, None], fn):
    root = repo.get_workspace_root(Path.cwd())
    namespace = workspace.parser.get_namespace_from_config(root)

    if not name:
        raise ValueError("Please add a name by using --name")

    if not namespace:
        raise ValueError(
            "Didn't find a namespace. Expected to find it in workspace.toml."
        )

    options = {
        "namespace": namespace,
        "package": name,
        "description": description,
        "modulename": "core",
    }
    fn(root, options)
