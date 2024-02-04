from pathlib import Path

from polylith.pdm.hooks.workspace import build_initialize


def pdm_build_initialize(context):
    """Adding an additional pth file to the virtual environment

    Making the virtual environment aware of the Polylith Workspace.
    """

    context.ensure_build_dir()

    build_dir = Path(context.build_dir)
    root = Path(context.root)

    build_initialize(context.config, build_dir, root)
