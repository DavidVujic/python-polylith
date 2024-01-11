import typer
from polylith.poly_cli import create
from typing_extensions import Annotated

from pathlib import Path
from polylith import info, repo, workspace

app = typer.Typer()

app.add_typer(create.app, name="create")


@app.command("info")
def info_command(
    short: Annotated[
        bool, typer.Option(help="Display Workspace Info adjusted for many projects.")
    ] = False
):
    """Info about the Polylith workspace."""

    root = repo.get_workspace_root(Path.cwd())
    ns = workspace.parser.get_namespace_from_config(root)
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)
    projects_data = info.get_bricks_in_projects(root, components, bases, ns)

    info.print_workspace_summary(projects_data, bases, components)

    if components or bases:
        if short:
            info.print_compressed_view_for_bricks_in_projects(
                projects_data, bases, components
            )
        else:
            info.print_bricks_in_projects(projects_data, bases, components)


if __name__ == "__main__":
    app()
