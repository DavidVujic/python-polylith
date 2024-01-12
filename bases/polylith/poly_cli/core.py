import typer
from polylith import commands
from polylith.poly_cli import create
from typing_extensions import Annotated

app = typer.Typer()

app.add_typer(create.app, name="create")


@app.command("info")
def info_command(
    short: Annotated[
        bool, typer.Option(help="Display Workspace Info adjusted for many projects.")
    ] = False
):
    """Info about the Polylith workspace."""
    commands.info.run(short)


if __name__ == "__main__":
    app()
