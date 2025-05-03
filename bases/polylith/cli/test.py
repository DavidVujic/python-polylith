from pathlib import Path

from polylith import commands, configuration, diff, repo
from polylith.cli import options
from typer import Option, Typer
from typing_extensions import Annotated

app = Typer()


@app.command("diff")
def diff_command(
    since: Annotated[str, Option(help="Changed since a specific tag.")] = "",
    short: Annotated[bool, options.short] = False,
    bricks: Annotated[bool, Option(help="Bricks affected by changes in tests")] = False,
    projects: Annotated[
        bool, Option(help="Projects affected by changes in tests")
    ] = False,
):
    """Shows the Polylith projects and bricks that are affected by changes in tests."""
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    tag = diff.collect.get_latest_tag(root, since) or since

    if not tag:
        print("No matching tags or commits found in repository.")
        return

    options = {"short": short, "bricks": bricks, "projects": projects}

    commands.test.run(root, ns, tag, options)
