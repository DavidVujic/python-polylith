from pathlib import Path
from typing import List

import tomlkit
from polylith import project, repo, workspace
from tomlkit.toml_document import TOMLDocument


def to_package(namespace: str, brick: str, brick_path: str, theme: str) -> dict:
    folder = f"{brick_path}" if theme == "loose" else f"{brick_path}/{brick}/src"

    return {"include": f"{namespace}/{brick}", "from": folder}


def generate_updated_project(data: TOMLDocument, packages: List[dict]) -> str:
    original = tomlkit.dumps(data)
    copy: dict = tomlkit.parse(original)

    if copy["tool"]["poetry"].get("packages") is None:
        copy["tool"]["poetry"].add("packages", [])

    for package in packages:
        copy["tool"]["poetry"]["packages"].append(package)

    copy["tool"]["poetry"]["packages"].multiline(True)

    return tomlkit.dumps(copy)


def to_packages(root: Path, namespace: str, diff: dict) -> List[dict]:
    theme = workspace.parser.get_theme_from_config(root)

    is_project = diff["is_project"]

    bases_path = "../../bases" if is_project else "bases"
    components_path = "../../components" if is_project else "components"

    a = [to_package(namespace, b, bases_path, theme) for b in diff["bases"]]
    b = [to_package(namespace, c, components_path, theme) for c in diff["components"]]

    return a + b


def rewrite_project_file(path: Path, packages: List[dict]):
    fullpath = path / repo.default_toml
    project_toml = project.get_toml(fullpath)

    generated = generate_updated_project(project_toml, packages)

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(generated)


def update_project(path: Path, namespace: str, diff: dict):
    packages = to_packages(path, namespace, diff)

    if packages:
        rewrite_project_file(diff["path"], packages)
