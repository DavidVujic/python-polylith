from pathlib import Path

import tomlkit
from polylith import repo
from polylith.dirs import create_dir
from polylith.repo import projects_dir


def create_project_toml(template: str, template_data: dict) -> tomlkit.TOMLDocument:
    content = template.format(**template_data)

    return tomlkit.loads(content)


def create_project(path: Path, template: str, name: str, description: str) -> None:
    d = create_dir(path, f"{projects_dir}/{name}")

    authors = repo.get_authors(path)
    python_version = repo.get_python_version(path)

    project_toml = create_project_toml(
        template,
        {
            "name": name,
            "description": description,
            "authors": authors,
            "python_version": python_version,
        },
    )

    fullpath = d / repo.default_toml

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(project_toml))
