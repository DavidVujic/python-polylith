# PDM Build Hook for a Polylith workspace

A plugin for [PDM](https://pdm-project.org) and the Polylith Architecture.

This build hook is making the virtual environment aware of a Polylith Workspace.

When running `pdm install` it will add an additional pth file to the virtual environment,
including paths to the `bases` and `components` folders.

## Usage
PDM has already a configuration option called `project-dir`, that is meant for defining a custom
path to the Python source code. But it only allows one directory.

The code in a Polylith workspace is organized into two folders (bases, components),
and that is the reason for using this hook.


## Installation
``` toml
[build-system]
requires = ["pdm-backend", "pdm-polylith-workspace"]
build-backend = "pdm.backend"

```

This is only needed in the Polylith workspace `pyproject.toml`, and not in the individual projects.

## Polylith documentation
[the Python tools for the Polylith Architecture](https://davidvujic.github.io/python-polylith-docs)
