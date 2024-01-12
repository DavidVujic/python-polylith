from polylith import commands
from polylith.poly_cli import create
from typer import Option, Typer
from typing_extensions import Annotated

app = Typer()

app.add_typer(create.app, name="create", help="Commands for creating a workspace, bases, components and projects.")


@app.command("info")
def info_command(
    short: Annotated[
        bool, Option(help="Display Workspace Info adjusted for many projects.")
    ] = False
):
    """Info about the Polylith workspace."""
    commands.info.run(short)


@app.command("diff")
def diff_command(
    since: Annotated[str, Option(help="Changed since a specific tag.")] = None,
    short: Annotated[bool, Option(help="Print short view.")] = False,
    bricks: Annotated[bool, Option(help="Print changed bricks.")] = False,
):
    """Shows changed bricks compared to the latest git tag."""
    commands.diff.run(since, short, bricks)


if __name__ == "__main__":
    app()
