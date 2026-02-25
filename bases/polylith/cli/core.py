from pathlib import Path
from typing import List, Union

from polylith import commands, configuration, info, repo
from polylith.cli import build, create, delete, env, options, test
from typer import Exit, Option, Typer
from typing_extensions import Annotated

app = Typer(no_args_is_help=True)

app.add_typer(
    create.app,
    name="create",
    help="Commands for creating a workspace, bases, components and projects.",
    no_args_is_help=True,
)

app.add_typer(
    delete.app,
    name="delete",
    help="Commands for deleting bases and components.",
    no_args_is_help=True,
)

app.add_typer(
    test.app,
    name="test",
    help="Commands for tests.",
    no_args_is_help=True,
)

app.add_typer(
    build.app,
    name="build",
    help="For Package & Dependency Management tools without support for plugins or build hooks.",
    no_args_is_help=True,
)

app.add_typer(
    env.app,
    name="env",
    help="For Package & Dependency Management tools without support for plugins or build hooks.",
    no_args_is_help=True,
)


def filtered_projects_data(
    projects_data: List[dict], directory: Union[str, None]
) -> List[dict]:
    dir_path = Path(directory).as_posix() if directory else Path.cwd().name

    return [p for p in projects_data if dir_path in p["path"].as_posix()]


def enriched_with_lock_file_data(
    root: Path, project_data: dict, is_verbose: bool
) -> dict:
    try:
        return commands.check.with_third_party_libs_from_lock_file(root, project_data)
    except ValueError as e:
        if is_verbose:
            name = project_data["name"]
            print(f"{name}: {e}")

        return project_data


def enriched_with_lock_files_data(
    root: Path, projects_data: List[dict], is_verbose: bool
) -> List[dict]:
    return [enriched_with_lock_file_data(root, p, is_verbose) for p in projects_data]


@app.command("info")
def info_command(
    short: Annotated[bool, options.short_workspace] = False,
    save: Annotated[bool, options.save] = False,
):
    """Info about the Polylith workspace."""
    root = repo.get_workspace_root(Path.cwd())
    output = configuration.get_output_dir(root, "info") if save else None

    cli_options = {
        "short": short,
        "save": save,
        "output": output,
    }
    commands.info.run(root, cli_options)


@app.command("check")
def check_command(
    strict: Annotated[bool, options.strict] = False,
    verbose: Annotated[bool, options.verbose] = False,
    quiet: Annotated[bool, options.quiet] = False,
    directory: Annotated[str, options.directory] = "",
    alias: Annotated[str, options.alias] = "",
):
    """Validates the Polylith workspace."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    all_projects_data = info.get_projects_data(root, ns)
    only_projects_data = [p for p in all_projects_data if info.is_project(p)]

    cli_options = {
        "verbose": verbose,
        "short": False,
        "quiet": quiet,
        "strict": strict,
        "alias": str.split(alias, ",") if alias else [],
    }

    filtered_projects = filtered_projects_data(only_projects_data, directory)
    enriched_projects = enriched_with_lock_files_data(root, filtered_projects, verbose)

    result = commands.check.run(root, ns, enriched_projects, cli_options)
    libs_result = commands.check.check_libs_versions(
        filtered_projects, all_projects_data, cli_options
    )

    if not result or not libs_result:
        raise Exit(code=1)


@app.command("diff")
def diff_command(
    since: Annotated[str, Option(help="Changed since a specific tag.")] = "",
    short: Annotated[bool, options.short] = False,
    bricks: Annotated[bool, Option(help="Print changed bricks.")] = False,
    deps: Annotated[
        bool, Option(help="Print bricks that depend on changes. Use with --bricks.")
    ] = False,
):
    """Shows changed bricks compared to the latest git tag."""
    options = {"short": short, "bricks": bricks, "deps": deps}

    commands.diff.run(since, options)


@app.command("libs")
def libs_command(
    strict: Annotated[bool, options.strict] = False,
    directory: Annotated[str, options.directory] = "",
    alias: Annotated[str, options.alias] = "",
    short: Annotated[bool, options.short] = False,
    save: Annotated[bool, options.save] = False,
):
    """Show third-party libraries used in the workspace."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    all_projects_data = info.get_projects_data(root, ns)
    output = configuration.get_output_dir(root, "libs") if save else None

    cli_options = {
        "strict": strict,
        "alias": str.split(alias, ",") if alias else [],
        "short": short,
        "save": save,
        "output": output,
    }

    projects_data = filtered_projects_data(all_projects_data, directory)
    merged_projects_data = enriched_with_lock_files_data(root, projects_data, False)

    results = commands.libs.run(root, ns, merged_projects_data, cli_options)
    commands.libs.run_library_versions(projects_data, all_projects_data, cli_options)

    if not all(results):
        raise Exit(code=1)


@app.command("sync")
def sync_command(
    quiet: Annotated[bool, options.quiet] = False,
    directory: Annotated[str, options.directory] = "",
    verbose: Annotated[bool, options.verbose] = False,
):
    """Update pyproject.toml with missing bricks."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    all_projects_data = info.get_projects_data(root, ns)

    cli_options = {
        "quiet": quiet,
        "verbose": verbose,
    }

    projects_data = filtered_projects_data(all_projects_data, directory)

    for p in projects_data:
        commands.sync.run(root, ns, p, cli_options)


@app.command("deps")
def deps_command(
    directory: Annotated[str, options.directory] = "",
    brick: Annotated[str, options.brick] = "",
    interface: Annotated[bool, options.interface] = False,
    save: Annotated[bool, options.save] = False,
):
    """Visualize the dependencies between bricks."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    dir_path = Path(directory).as_posix() if directory else None
    output = configuration.get_output_dir(root, "deps") if save else None

    cli_options = {
        "directory": dir_path,
        "brick": brick or None,
        "save": save,
        "output": output,
        "show_interface": interface,
    }

    commands.deps.run(root, ns, cli_options)


if __name__ == "__main__":
    app()
