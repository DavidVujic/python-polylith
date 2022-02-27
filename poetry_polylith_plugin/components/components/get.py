from pathlib import Path

from poetry_polylith_plugin.components.components.constants import dir_name


def get_component_dirs(path: Path, top_dir):
    component_dir = path / top_dir

    return (f for f in component_dir.iterdir() if f.is_dir())


def dirs(path, ns, parent):
    return (f.name for f in path.glob(f"{parent}/{ns}/{path.name}") if f.is_dir())


def component_dirs(path: Path, ns: str):
    src_dirs = dirs(path, ns, "src")
    test_dirs = dirs(path, ns, "test")

    return {
        "name": path.name,
        "src": True if next(src_dirs, None) else False,
        "test": True if next(test_dirs, None) else False,
    }


def get_components_data(path: Path, ns: str, top_dir: str = dir_name):
    dirs = get_component_dirs(path, top_dir)

    return [component_dirs(d, ns) for d in dirs]
