from pathlib import Path

import tomlkit
from polylith import building, repo, toml
from typer import Exit, Typer

app = Typer()


def get_work_dir() -> Path:
    return building.get_work_dir({})


def get_project_data(build_dir: Path) -> tomlkit.TOMLDocument:
    fullpath = build_dir / repo.default_toml

    if not fullpath.exists():
        raise Exit(code=1)

    return toml.read_toml_document(fullpath)


@app.command("setup")
def setup_command():
    """Prepare a project before building a wheel or a source distribution (sdist).
    Run it before the build command of your Package & Dependency Management tool.

    """
    work_dir = get_work_dir()
    build_dir = Path.cwd()

    data = get_project_data(build_dir)
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
    work_dir = get_work_dir()
    build_dir = Path.cwd()

    data = get_project_data(build_dir)
    bricks = toml.get_project_packages_from_polylith_section(data)

    if not bricks:
        return

    destination_dir = building.calculate_destination_dir(data)

    building.cleanup(work_dir)
    building.cleanup(destination_dir)
