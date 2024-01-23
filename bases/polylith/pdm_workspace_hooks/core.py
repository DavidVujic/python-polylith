import os


def pdm_build_initialize(context):
    """Adding an additional pth file to the virtual environment

    Making the virtual environment aware of the Polylith Workspace.
    """

    context.ensure_build_dir()
    filepath = os.path.join(context.build_dir, "polylith_workspace.pth")

    with open(filepath, "w") as f:
        f.write(f"{context.config.root}/bases\n")
        f.write(f"{context.config.root}/components\n")
