from pathlib import Path

import tomlkit
from polylith import readme, repo
from polylith.development import create_development
from polylith.dirs import create_dir

template = """\
[tool.polylith]
namespace = "{namespace}"
git_tag_pattern = "stable-*"

[tool.polylith.structure]
theme = "{theme}"

[tool.polylith.resources]
brick_docs_enabled = false

[tool.polylith.test]
enabled = true
"""


def create_workspace_config(path: Path, namespace: str, theme: str) -> None:
    formatted = template.format(namespace=namespace, theme=theme)
    content: dict = tomlkit.loads(formatted)

    fullpath = path / repo.workspace_file

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(content))


def create_workspace(path: Path, namespace: str, theme: str) -> None:
    create_dir(path, repo.bases_dir, keep=True)
    create_dir(path, repo.components_dir, keep=True)
    create_dir(path, repo.projects_dir, keep=True)

    create_development(path, keep=True)

    create_workspace_config(path, namespace, theme)

    readme.create_workspace_readme(path, namespace)
