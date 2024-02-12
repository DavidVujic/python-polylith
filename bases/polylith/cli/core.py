from pathlib import Path

from polylith import commands, configuration, info, repo
from polylith.cli import create, options
from typer import Exit, Option, Typer
from typing_extensions import Annotated

app = Typer()

app.add_typer(
    create.app,
    name="create",
    help="Commands for creating a workspace, bases, components and projects.",
)


@app.command("info")
def info_command(short: Annotated[bool, options.short_workspace] = False):
    """Info about the Polylith workspace."""
    commands.info.run(short)


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
        "quiet": quiet,
        "strict": strict,
        "alias": str.split(alias, ",") if alias else [],
    }

    dir_path = Path(directory).as_posix() if directory else Path.cwd().name
    projects_data = [p for p in only_projects_data if dir_path in p["path"].as_posix()]
    results = {commands.check.run(root, ns, p, cli_options) for p in projects_data}

    if not all(results):
        raise Exit(code=1)


@app.command("diff")
def diff_command(
    since: Annotated[str, Option(help="Changed since a specific tag.")] = "",
    short: Annotated[bool, options.short] = False,
    bricks: Annotated[bool, Option(help="Print changed bricks.")] = False,
):
    """Shows changed bricks compared to the latest git tag."""
    commands.diff.run(since, short, bricks)


@app.command("libs")
def libs_command(
    strict: Annotated[bool, options.strict] = False,
    directory: Annotated[str, options.directory] = "",
    alias: Annotated[str, options.alias] = "",
):
    """Show third-party libraries used in the workspace."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    projects_data = info.get_projects_data(root, ns)

    cli_options = {
        "strict": strict,
        "alias": str.split(alias, ",") if alias else [],
    }

    dir_path = Path(directory).as_posix() if directory else Path.cwd().name
    projects_data = [p for p in projects_data if dir_path in p["path"].as_posix()]
    results = {commands.libs.run(root, ns, p, cli_options) for p in projects_data}

    if not all(results):
        raise Exit(code=1)


@app.command("sync")
def sync_command(
    strict: Annotated[bool, options.strict] = False,
    quiet: Annotated[bool, options.quiet] = False,
    directory: Annotated[str, options.directory] = "",
    verbose: Annotated[str, options.verbose] = "",
):
    """Update pyproject.toml with missing bricks."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    projects_data = info.get_projects_data(root, ns)

    cli_options = {
        "strict": strict,
        "quiet": quiet,
        "verbose": verbose,
    }

    dir_path = Path(directory).as_posix() if directory else Path.cwd().name
    projects_data = [p for p in projects_data if dir_path in p["path"].as_posix()]

    for p in projects_data:
        commands.sync.run(root, ns, p, cli_options)


@app.command("deps")
def deps_command(directory: Annotated[str, options.directory] = ""):
    """Visualize the dependencies between bricks."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    dir_path = Path(directory).as_posix() if directory else None

    commands.deps.run(root, ns, dir_path)


if __name__ == "__main__":
    app()
