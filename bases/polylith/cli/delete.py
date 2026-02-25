from pathlib import Path

from polylith import commands, configuration, repo
from typer import Exit, Option, Typer
from typing_extensions import Annotated

app = Typer(no_args_is_help=True)


def _delete_brick(brick_type: str, name: str, dry_run: bool, force: bool) -> None:
    root = repo.get_workspace_root(Path.cwd())
    namespace = configuration.get_namespace_from_config(root)

    cli_options = {
        "brick_type": brick_type,
        "name": name,
        "dry_run": dry_run,
        "force": force,
    }

    result = commands.delete.run(root, namespace, cli_options)

    if not result:
        raise Exit(code=1)


@app.command("component")
def component_command(
    name: Annotated[str, Option(help="Name of the component to delete.")],
    dry_run: Annotated[
        bool, Option(help="Print what would be deleted, but do nothing.")
    ] = False,
    force: Annotated[
        bool,
        Option(help="Delete even if other bricks/projects still use it."),
    ] = False,
):
    """Deletes a Polylith component (including generated tests)."""

    _delete_brick("component", name, dry_run, force)


@app.command("base")
def base_command(
    name: Annotated[str, Option(help="Name of the base to delete.")],
    dry_run: Annotated[
        bool, Option(help="Print what would be deleted, but do nothing.")
    ] = False,
    force: Annotated[
        bool,
        Option(help="Delete even if other bricks/projects still use it."),
    ] = False,
):
    """Deletes a Polylith base (including generated tests)."""

    _delete_brick("base", name, dry_run, force)
