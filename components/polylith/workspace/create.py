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
bricks = "{brick}/{namespace}/{package}"
tests = "test/{brick}/{namespace}/{package}"

[tool.polylith.test]
enabled = true
template = \"\"\"\
from {namespace}.{package} import {modulename}


def test_sample():
    assert {modulename} is not None
\"\"\"
"""


def create_workspace_config(path: Path, namespace: str) -> None:
    content: dict = tomlkit.loads(
        template.replace('namespace = "{namespace}"', f'namespace = "{namespace}"')
    )

    fullpath = path / repo.workspace_file

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(content))


def create_workspace(path: Path, namespace: str) -> None:
    create_dir(path, repo.bases_dir, keep=True)
    create_dir(path, repo.components_dir, keep=True)
    create_dir(path, repo.projects_dir, keep=True)

    create_development(path, keep=True)

    create_workspace_config(path, namespace)

    readme.create_workspace_readme(path, namespace)
