import shutil
from pathlib import Path
from typing import List, Set, Tuple

import tomlkit
from polylith import configuration, deps, info, project, repo, toml


def _brick_dir(theme: str, namespace: str, name: str, brick_dir_name: str) -> Path:
    if theme == "loose":
        return Path(brick_dir_name, namespace, name)

    return Path(brick_dir_name, name)


def _test_dir(theme: str, namespace: str, name: str, brick_dir_name: str) -> Path:
    if theme == "loose":
        return Path("test", brick_dir_name, namespace, name)

    return Path(brick_dir_name, name, "test", namespace, name)


def _collect_projects_using_brick(
    projects_data: List[dict], brick_type: str, name: str
) -> List[str]:
    key = "components" if brick_type == "component" else "bases"

    return sorted([p["name"] for p in projects_data if name in (p.get(key) or [])])


def _collect_bricks_using_brick(import_data: dict, brick: str) -> List[str]:
    used_by = {k for k, v in import_data.items() if brick in (v or set())}

    return sorted(used_by.difference({brick}))


def _remove_brick_from_project_pyproject(
    root: Path, project_path: Path, namespace: str, brick_dir_name: str, brick: str
) -> bool:
    fullpath = project_path / repo.default_toml

    if not fullpath.exists():
        return False

    data = project.get_toml(fullpath)

    brick_include = f"{namespace}/{brick}"
    changed = toml.remove_brick_from_project_packages(
        data, brick_include, brick_dir_name
    )

    if not changed:
        return False

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(data))

    return True


def _project_paths(root: Path) -> List[Path]:
    paths = [root]
    paths.extend([p.parent for p in root.glob(f"projects/*/{repo.default_toml}")])

    return paths


def _get_all_bricks(root: Path, namespace: str) -> Tuple[Set[str], Set[str]]:
    bases = set(info.get_bases(root, namespace))
    components = set(info.get_components(root, namespace))

    return bases, components


def _get_import_data(root: Path, namespace: str) -> dict:
    bases, components = _get_all_bricks(root, namespace)
    brick_imports = deps.get_brick_imports(root, namespace, bases, components)

    return {**brick_imports.get("bases", {}), **brick_imports.get("components", {})}


def _validate_can_delete(
    root: Path,
    namespace: str,
    brick_type: str,
    name: str,
) -> Tuple[List[str], List[str]]:
    import_data = _get_import_data(root, namespace)
    projects_data = info.get_projects_data(root, namespace)

    used_by_bricks = _collect_bricks_using_brick(import_data, name)
    used_by_projects = _collect_projects_using_brick(projects_data, brick_type, name)

    return used_by_bricks, used_by_projects


def _delete_paths(paths: List[Path]) -> None:
    for p in paths:
        if p.exists():
            shutil.rmtree(p)


def run(root: Path, namespace: str, options: dict) -> bool:
    brick_type = options["brick_type"]
    name = options["name"]
    dry_run = bool(options.get("dry_run"))
    force = bool(options.get("force"))

    if brick_type not in {"component", "base"}:
        raise ValueError(f"Unknown brick type: {brick_type}")

    brick_dir_name = (
        repo.components_dir if brick_type == "component" else repo.bases_dir
    )

    theme = configuration.get_theme_from_config(root)

    bases, components = _get_all_bricks(root, namespace)

    if brick_type == "component" and name not in components:
        print(f"Component not found: {name}")
        return False

    if brick_type == "base" and name not in bases:
        print(f"Base not found: {name}")
        return False

    brick_dir = root / _brick_dir(theme, namespace, name, brick_dir_name)
    test_dir = root / _test_dir(theme, namespace, name, brick_dir_name)

    paths_to_delete = [brick_dir]

    # In loose theme, tests live outside the brick folder.
    if theme == "loose" and test_dir != brick_dir:
        paths_to_delete.append(test_dir)

    used_by_bricks, used_by_projects = _validate_can_delete(
        root, namespace, brick_type, name
    )

    if (used_by_bricks or used_by_projects) and not force:
        if used_by_bricks:
            print(f"Cannot delete '{name}': used by bricks: {', '.join(used_by_bricks)}")
        if used_by_projects:
            print(
                f"Cannot delete '{name}': used by projects: {', '.join(used_by_projects)}"
            )
        print("Re-run with --force to delete anyway.")
        return False

    project_paths = _project_paths(root)

    if dry_run:
        existing = [p for p in paths_to_delete if p.exists()]
        missing = [p for p in paths_to_delete if not p.exists()]

        for p in existing:
            print(f"Would delete: {p}")
        for p in missing:
            print(f"Missing (skip): {p}")

        for p in project_paths:
            fullpath = p / repo.default_toml
            if fullpath.exists():
                print(f"Would update: {fullpath}")

        return True

    updated_projects = []
    for p in project_paths:
        if _remove_brick_from_project_pyproject(
            root, p, namespace, brick_dir_name, name
        ):
            updated_projects.append(p)

    _delete_paths(paths_to_delete)

    if updated_projects:
        for p in updated_projects:
            print(f"Updated: {p / repo.default_toml}")

    print(f"Deleted {brick_type}: {name}")

    return True
