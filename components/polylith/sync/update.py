from pathlib import Path
from typing import List, Union

import tomlkit
from polylith import project, repo, workspace
from tomlkit.toml_document import TOMLDocument


def to_package(namespace: str, brick: str, brick_path: str, theme: str) -> dict:
    folder = f"{brick_path}" if theme == "loose" else f"{brick_path}/{brick}/src"

    return {"include": f"{namespace}/{brick}", "from": folder}


def copy_toml_data(data: TOMLDocument) -> dict:
    original = tomlkit.dumps(data)
    copy: dict = tomlkit.parse(original)

    return copy


def generate_updated_hatch_project(
    data: TOMLDocument, packages: List[dict]
) -> str:
    copy = copy_toml_data(data)

    if copy["tool"]["hatch"].get("build") is None:
        copy["tool"]["hatch"].add("build", {"force-include": {}})

    if copy["tool"]["hatch"]["build"].get("force-include") is None:
        copy["tool"]["hatch"]["build"]["force-include"] = {}

    for package in packages:
        brick = package["include"]
        relative_path = package.get("from", "")
        include = Path(relative_path, brick).as_posix()

        copy["tool"]["hatch"]["build"]["force-include"][include] = brick

    return tomlkit.dumps(copy)


def generate_updated_poetry_project(data: TOMLDocument, packages: List[dict]) -> str:
    copy = copy_toml_data(data)

    if copy["tool"]["poetry"].get("packages") is None:
        copy["tool"]["poetry"].add("packages", [])

    for package in packages:
        copy["tool"]["poetry"]["packages"].append(package)

    copy["tool"]["poetry"]["packages"].multiline(True)

    return tomlkit.dumps(copy)


def generate_updated_project(data: TOMLDocument, packages: List[dict]) -> Union[str, None]:
    if repo.is_poetry(data):
        return generate_updated_poetry_project(data, packages)

    if repo.is_hatch(data):
        return generate_updated_hatch_project(data, packages)

    return None


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

    if not generated:
        return

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(generated)


def update_project(path: Path, namespace: str, diff: dict):
    packages = to_packages(path, namespace, diff)

    if packages:
        rewrite_project_file(diff["path"], packages)
