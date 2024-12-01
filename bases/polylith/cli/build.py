from pathlib import Path
from typing import Union

from polylith import building, repo, toml
from typer import Exit, Typer

app = Typer()


def get_pyproject(build_dir: Path) -> Path:
    pyproject = build_dir / repo.default_toml

    if not pyproject.exists():
        raise Exit(code=1)

    return pyproject


def get_bricks(pyproject: Path) -> dict:
    data = toml.read_toml_document(pyproject)

    return toml.get_project_packages_from_polylith_section(data)


def calculate_destination_dir(pyproject: Path) -> Union[Path, None]:
    bricks = get_bricks(pyproject)

    if not bricks:
        return None

    custom_top_ns = toml.get_custom_top_namespace_from_polylith_section(pyproject)
    top_ns = next((v for v in bricks.values()), None)

    if custom_top_ns:
        return Path(custom_top_ns)

    return Path(top_ns) if top_ns else None


@app.command("setup")
def setup_command():
    """Prepare a project before building a wheel or a source distribution (sdist).
    Run it before the build command of your Package & Dependency Management tool.

    """
    work_dir = building.get_work_dir({})
    build_dir = Path.cwd()

    pyproject = get_pyproject(build_dir)
    bricks = get_bricks(pyproject)

    if not bricks:
        return

    custom_top_ns = toml.get_custom_top_namespace_from_polylith_section(pyproject)

    if not custom_top_ns:
        building.copy_bricks_as_is(bricks, build_dir)
    else:
        building.copy_and_rewrite_bricks(bricks, custom_top_ns, work_dir, build_dir)


@app.command("teardown")
def teardown_command():
    """Clean up temporary directories. Run it after the build command of your Package & Dependency Management tool."""
    work_dir = building.get_work_dir({})
    build_dir = Path.cwd()

    pyproject = get_pyproject(build_dir)
    bricks = get_bricks(pyproject)

    if not bricks:
        return

    destination_dir = calculate_destination_dir(pyproject)

    building.cleanup(work_dir)
    building.cleanup(destination_dir)
