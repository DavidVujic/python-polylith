from pathlib import Path
from typing import Union

from polylith import building, repo, toml
from typer import Exit, Typer

app = Typer()


def get_pyproject(build_dir: Path) -> dict:
    pyproject = build_dir / repo.default_toml

    if not pyproject.exists():
        raise Exit(code=1)

    data = toml.read_toml_document(pyproject)
    return data


def calculate_root(bricks: dict) -> Union[str, None]:
    brick_path = next((v for v in bricks.values()), None)

    return str.split(brick_path, "/")[0] if brick_path else None


def calculate_destination_dir(data: dict) -> Union[Path, None]:
    bricks = toml.get_project_packages_from_polylith_section(data)

    if not bricks:
        return None

    custom_top_ns = toml.get_custom_top_namespace_from_polylith_section(data)

    if custom_top_ns:
        return Path(custom_top_ns)

    root = calculate_root(bricks)

    return Path(root) if root else None


@app.command("setup")
def setup_command():
    """Prepare a project before building a wheel or a source distribution (sdist).
    Run it before the build command of your Package & Dependency Management tool.

    """
    work_dir = building.get_work_dir({})
    build_dir = Path.cwd()

    data = get_pyproject(build_dir)
    bricks = toml.get_project_packages_from_polylith_section(data)

    if not bricks:
        return

    custom_top_ns = toml.get_custom_top_namespace_from_polylith_section(data)

    if not custom_top_ns:
        building.copy_bricks_as_is(bricks, build_dir)
    else:
        building.copy_and_rewrite_bricks(bricks, custom_top_ns, work_dir, build_dir)


@app.command("teardown")
def teardown_command():
    """Clean up temporary directories. Run it after the build command of your Package & Dependency Management tool."""
    work_dir = building.get_work_dir({})
    build_dir = Path.cwd()

    data = get_pyproject(build_dir)
    bricks = toml.get_project_packages_from_polylith_section(data)

    if not bricks:
        return

    destination_dir = calculate_destination_dir(data)

    building.cleanup(work_dir)
    building.cleanup(destination_dir)
