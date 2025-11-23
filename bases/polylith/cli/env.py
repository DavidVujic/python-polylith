import sysconfig
from pathlib import Path

from polylith import configuration, environment, info, repo
from typer import Typer

app = Typer()


@app.command("setup")
def setup_command():
    """Setup the current virtual environment, by adding the bases and components paths as module root."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    projects_data = info.get_projects_data(root, ns)
    dev_project_data = next(p for p in projects_data if p["type"] == "development")

    env_dir = Path(sysconfig.get_paths().get("purelib"))

    environment.add_paths(dev_project_data, env_dir, root)
