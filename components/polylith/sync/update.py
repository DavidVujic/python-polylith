from pathlib import Path
from typing import List, Set

import tomlkit
from polylith import project, repo
from tomlkit.toml_document import TOMLDocument


def to_package(namespace: str, brick: str, brick_folder: str, is_project: bool) -> dict:
    from_path = f"../../{brick_folder}" if is_project else brick_folder

    return {"include": f"{namespace}/{brick}", "from": from_path}


def generate_updated_project(data: TOMLDocument, packages: List[dict]) -> str:
    original = tomlkit.dumps(data)
    copy: dict = tomlkit.parse(original)

    if copy["tool"]["poetry"].get("packages") is None:
        copy["tool"]["poetry"].add("packages", [])

    for package in packages:
        copy["tool"]["poetry"]["packages"].append(package)

    copy["tool"]["poetry"]["packages"].multiline(True)

    return tomlkit.dumps(copy)


def to_packages(
    namespace: str, bases: Set[str], components: Set[str], is_project: bool
) -> List[dict]:
    a = [to_package(namespace, b, "bases", is_project) for b in bases]
    b = [to_package(namespace, c, "components", is_project) for c in components]

    return a + b


def update_project(path: Path, packages: List[dict]) -> None:
    fullpath = path / repo.default_toml
    project_toml = project.get_toml(fullpath)

    generated = generate_updated_project(project_toml, packages)

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(generated)
