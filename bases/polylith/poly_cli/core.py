from pathlib import Path

from polylith import commands, info, repo, workspace
from polylith.poly_cli import create
from typer import Exit, Option, Typer
from typing_extensions import Annotated

app = Typer()

app.add_typer(
    create.app,
    name="create",
    help="Commands for creating a workspace, bases, components and projects.",
)


@app.command("info")
def info_command(
    short: Annotated[
        bool, Option(help="Display Workspace Info adjusted for many projects.")
    ] = False
):
    """Info about the Polylith workspace."""
    commands.info.run(short)


@app.command("check")
def check_command(
    strict: Annotated[
        bool,
        Option(
            help="More strict checks when matching name of third-party libraries and imports"
        ),
    ] = False,
    verbose: Annotated[
        bool,
        Option(help="More verbose output."),
    ] = False,
    quiet: Annotated[
        bool,
        Option(help="Do not output any messages."),
    ] = False,
    directory: Annotated[
        str,
        Option(
            help="The working directory for the command (defaults to the current working directory)."
        ),
    ] = "",
    alias: Annotated[
        str,
        Option(
            help="alias for third-party libraries, useful when an import differ from the library name"
        ),
    ] = "",
):
    """Validates the Polylith workspace."""

    root = repo.get_workspace_root(Path.cwd())
    ns = workspace.parser.get_namespace_from_config(root)

    all_projects_data = info.get_projects_data(root, ns)
    only_projects_data = [p for p in all_projects_data if info.is_project(p)]

    options = {
        "verbose": verbose,
        "quiet": quiet,
        "strict": strict,
        "alias": str.split(alias, ",") if alias else [],
    }

    dir_path = Path(directory).as_posix() if directory else Path.cwd().name

    projects_data = [p for p in only_projects_data if dir_path in p["path"].as_posix()]

    results = {commands.check.run(root, ns, p, options) for p in projects_data}

    if not all(results):
        raise Exit(code=1)


@app.command("diff")
def diff_command(
    since: Annotated[str, Option(help="Changed since a specific tag.")] = "",
    short: Annotated[bool, Option(help="Print short view.")] = False,
    bricks: Annotated[bool, Option(help="Print changed bricks.")] = False,
):
    """Shows changed bricks compared to the latest git tag."""
    commands.diff.run(since, short, bricks)


@app.command("libs")
def libs_command(
    strict: Annotated[
        bool,
        Option(
            help="More strict checks when matching name of third-party libraries and imports"
        ),
    ] = False,
    directory: Annotated[
        str,
        Option(
            help="The working directory for the command (defaults to the current working directory)."
        ),
    ] = "",
    alias: Annotated[
        str,
        Option(
            help="alias for third-party libraries, useful when an import differ from the library name"
        ),
    ] = "",
):
    """Show third-party libraries used in the workspace."""

    root = repo.get_workspace_root(Path.cwd())
    ns = workspace.parser.get_namespace_from_config(root)

    projects_data = info.get_projects_data(root, ns)

    options = {
        "strict": strict,
        "alias": str.split(alias, ",") if alias else [],
    }

    dir_path = Path(directory).as_posix() if directory else Path.cwd().name

    projects_data = [p for p in projects_data if dir_path in p["path"].as_posix()]

    results = {commands.libs.run(root, ns, p, options) for p in projects_data}

    if not all(results):
        raise Exit(code=1)


if __name__ == "__main__":
    app()
