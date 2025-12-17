import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set, Tuple

import tomlkit
from polylith import configuration, deps, info, repo, toml


@dataclass(frozen=True)
class DeleteRequest:
    brick_type: str
    name: str
    dry_run: bool
    force: bool


@dataclass(frozen=True)
class BrickRef:
    include: str
    dir_name: str


@dataclass(frozen=True)
class BrickUsage:
    used_by_bricks: List[str]
    used_by_projects: List[str]


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


def _get_brick_dir_name(brick_type: str) -> str:
    if brick_type == "component":
        return repo.components_dir
    if brick_type == "base":
        return repo.bases_dir

    raise ValueError(f"Unknown brick type: {brick_type}")


def _brick_exists(
    brick_type: str,
    name: str,
    bases: Set[str],
    components: Set[str],
) -> bool:
    if brick_type == "component":
        return name in components

    return name in bases


def _missing_brick_message(brick_type: str, name: str) -> str:
    if brick_type == "component":
        return f"Component not found: {name}"

    return f"Base not found: {name}"


def _paths_to_delete(
    root: Path,
    theme: str,
    namespace: str,
    brick_dir_name: str,
    name: str,
) -> List[Path]:
    brick_dir = root / _brick_dir(theme, namespace, name, brick_dir_name)
    test_dir = root / _test_dir(theme, namespace, name, brick_dir_name)

    paths = [brick_dir]

    # In loose theme, tests live outside the brick folder.
    if theme == "loose" and test_dir != brick_dir:
        paths.append(test_dir)

    return paths


def _validate_can_delete(
    root: Path,
    namespace: str,
    brick_type: str,
    name: str,
) -> BrickUsage:
    import_data = _get_import_data(root, namespace)
    projects_data = info.get_projects_data(root, namespace)

    used_by_bricks = _collect_bricks_using_brick(import_data, name)
    used_by_projects = _collect_projects_using_brick(projects_data, brick_type, name)

    return BrickUsage(used_by_bricks=used_by_bricks, used_by_projects=used_by_projects)


def _delete_paths(paths: Iterable[Path]) -> None:
    for p in paths:
        if p.exists():
            shutil.rmtree(p)


def _project_pyproject_path(project_path: Path) -> Path:
    return project_path / repo.default_toml


def _would_update_pyproject(project_path: Path, brick_ref: BrickRef) -> bool:
    fullpath = _project_pyproject_path(project_path)

    if not fullpath.exists():
        return False

    data = toml.read_toml_document(fullpath)

    return bool(
        toml.remove_brick_from_project_packages(data, brick_ref.include, brick_ref.dir_name)
    )


def _update_pyproject(project_path: Path, brick_ref: BrickRef) -> bool:
    fullpath = _project_pyproject_path(project_path)

    if not fullpath.exists():
        return False

    data = toml.read_toml_document(fullpath)

    changed = toml.remove_brick_from_project_packages(
        data, brick_ref.include, brick_ref.dir_name
    )

    if not changed:
        return False

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(data))

    return True


def _parse_request(options: dict) -> DeleteRequest:
    brick_type = options["brick_type"]
    name = options["name"]
    dry_run = bool(options.get("dry_run"))
    force = bool(options.get("force"))

    return DeleteRequest(brick_type=brick_type, name=name, dry_run=dry_run, force=force)


def _print_usage_block(usage: BrickUsage, name: str) -> None:
    if usage.used_by_bricks:
        print(f"Used by bricks: {', '.join(usage.used_by_bricks)}")
    if usage.used_by_projects:
        print(f"Used by projects: {', '.join(usage.used_by_projects)}")

    if usage.used_by_bricks or usage.used_by_projects:
        print(f"Cannot delete '{name}' without --force")


def _print_dry_run(
    request: DeleteRequest,
    paths_to_delete: List[Path],
    project_paths: List[Path],
    brick_ref: BrickRef,
    usage: BrickUsage,
) -> None:
    print(f"Dry run: delete {request.brick_type} '{request.name}'")

    _print_usage_block(usage, request.name)

    existing = [p for p in paths_to_delete if p.exists()]
    missing = [p for p in paths_to_delete if not p.exists()]

    for p in existing:
        print(f"Would delete: {p}")
    for p in missing:
        print(f"Skip missing: {p}")

    pyprojects_to_update = []
    for p in project_paths:
        if _would_update_pyproject(p, brick_ref):
            pyprojects_to_update.append(_project_pyproject_path(p))

    for fullpath in pyprojects_to_update:
        print(f"Would update: {fullpath}")


def _print_updated_pyprojects(updated_projects: List[Path]) -> None:
    for p in updated_projects:
        print(f"Updated: {_project_pyproject_path(p)}")


def run(root: Path, namespace: str, options: dict) -> bool:
    request = _parse_request(options)
    brick_dir_name = _get_brick_dir_name(request.brick_type)

    theme = configuration.get_theme_from_config(root)
    bases, components = _get_all_bricks(root, namespace)

    if not _brick_exists(request.brick_type, request.name, bases, components):
        print(_missing_brick_message(request.brick_type, request.name))
        return False

    paths_to_delete = _paths_to_delete(
        root, theme, namespace, brick_dir_name, request.name
    )

    usage = _validate_can_delete(root, namespace, request.brick_type, request.name)

    if not request.force and (usage.used_by_bricks or usage.used_by_projects):
        _print_usage_block(usage, request.name)
        return False

    brick_ref = BrickRef(include=f"{namespace}/{request.name}", dir_name=brick_dir_name)
    project_paths = _project_paths(root)

    if request.dry_run:
        _print_dry_run(request, paths_to_delete, project_paths, brick_ref, usage)
        return True

    updated_projects = []
    for p in project_paths:
        if _update_pyproject(p, brick_ref):
            updated_projects.append(p)

    _delete_paths(paths_to_delete)

    if updated_projects:
        _print_updated_pyprojects(updated_projects)

    print(f"Deleted {request.brick_type}: {request.name}")

    return True
