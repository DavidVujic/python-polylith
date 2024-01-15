from pathlib import Path
from typing import Union

from polylith import project, repo
from polylith.bricks import base, component
from polylith.commands.create import create
from polylith.workspace.create import create_workspace
from typer import Exit, Option, Typer
from typing_extensions import Annotated

app = Typer()


@app.command("base")
def base_command(
    name: Annotated[str, Option(help="Name of the base.")],
    description: Annotated[str, Option(help="Description of the base.")] = "",
):
    """Creates a Polylith base."""
    create(name, description, base.create_base)


@app.command("component")
def component_command(
    name: Annotated[str, Option(help="Name of the component.")],
    description: Annotated[str, Option(help="Description of the component.")] = "",
):
    """Creates a Polylith component."""
    create(name, description, component.create_component)


def _create_project(root: Path, _ns: str, name: str, description: Union[str, None]):
    root_pyproject: dict = project.get_toml(root / repo.default_toml)

    if repo.is_poetry(root_pyproject):
        template = project.templates.poetry_pyproject
    elif repo.is_hatch(root_pyproject):
        template = project.templates.hatch_pyproject

    if not template:
        print("Failed to guess the used Package & Dependency Management")
        print(
            "Is the root pyproject.toml missing, or are you using a tool not supported by Polylith?"
        )
        raise Exit(code=1)

    project.create_project(root, template, name, description or "")


@app.command("project")
def project_command(
    name: Annotated[str, Option(help="Name of the project.")],
    description: Annotated[str, Option(help="Description of the project.")] = "",
):
    """Creates a Polylith project."""
    create(name, description, _create_project)


@app.command("workspace")
def workspace_command(
    name: Annotated[str, Option(help="Name of the workspace.")],
    theme: Annotated[str, Option(help="Workspace theme.")] = "tdd",
):
    """Creates a Polylith workspace in the current directory."""
    path = Path.cwd()

    create_workspace(path, name, theme)
