from pathlib import Path
from typing import Union

from polylith import configuration, repo


def create(name: Union[str, None], description: Union[str, None], fn):
    root = repo.get_workspace_root(Path.cwd())
    namespace = configuration.get_namespace_from_config(root)

    if not name:
        raise ValueError("Please add a name by using --name")

    if not namespace:
        raise ValueError(
            "Didn't find a namespace. Expected to find it under [tool.polylith] in workspace.toml or pyproject.toml."
        )

    options = {
        "namespace": namespace,
        "package": name,
        "description": description,
        "modulename": "core",
    }
    fn(root, options)
