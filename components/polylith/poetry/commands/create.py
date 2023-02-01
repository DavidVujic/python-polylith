from pathlib import Path

from polylith import repo, workspace


def create(command, fn):
    root = repo.find_workspace_root(Path.cwd())
    name = command.option("name")
    description = command.option("description")
    namespace = workspace.parser.get_namespace_from_config(root)

    if not name:
        raise ValueError("Please add a name by using --name or -n")

    if not namespace:
        raise ValueError(
            "Didn't find a namespace. Expected to find it in workspace.toml."
        )

    fn(root, namespace, name, description)
