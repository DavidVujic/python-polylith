# Python tooling for Polylith

A command line interface that adds tooling support for the Polylith Architecture in Python.

## Documentation
Have a look at the [documentation](https://davidvujic.github.io/python-polylith-docs/).
You will find installation, setup, usage guides and more.

## Quick start

`Poetry` user? For Poetry, the recommended setup is to install the `poetry-polylith-plugin`.
Read more about Poetry in the [documentation](https://davidvujic.github.io/python-polylith-docs/installation/).

## Setup for Hatch users
Create a directory for your code, initialize it with __git__ and setup the basics with `hatch`:

``` shell
git init

hatch new --init
```

Add the Polylith CLI as a dev dependency in `pyproject.toml`:

``` toml
[tool.hatch.envs.default]
dependencies = ["polylith-cli"]
```

Add configuration for a local virtual environment in the `pyproject.toml`:
``` toml
[tool.hatch.envs.default]
type = "virtual"
path = ".venv"
python = "3.12"  # your preferred version here
```

Make `Hatch` aware of the Polylith structure, by adding this to the `pyproject.toml`:
``` toml
[tool.hatch.build]
dev-mode-dirs = ["components", "bases", "development", "."]

```

Next: create a Polylith workspace, with a basic Polylith folder structure.
The `poly` command is now available in the local virtual environment.
You can run commands in the context of `hatch run` to make Polylith aware of the development environment.

``` shell
hatch run poly create workspace --name my_namespace --theme loose
```

### Ready for coding!

Add components, bases and projects:

``` shell
hatch run poly create component --name my_component

hatch run poly create base --name my_example_endpoint

hatch run poly create project --name my_example_project
```

For details, have a look at the [documentation](https://davidvujic.github.io/python-polylith-docs/).
There, you will find guides for setup, migration, packaging, available commands, code examples and more.


## Setup for PDM users
Create a directory for your code, initialize it with __git__ and setup the basics with `PDM`.

``` shell
git init

pdm init -n --backend pdm-backend minimal
```

### Add a workspace hook
Make `PDM` aware of the Polylith structure, by adding the `pdm-polylith-workspace` hook to the newly created `pyproject.toml`.

The build hook will add an additional `pth` file to the virtual environment,
with paths to the Polylith source code folders (bases, components).

``` toml
[build-system]
requires = ["pdm-backend", "pdm-polylith-workspace"]
build-backend = "pdm.backend"

```

### Add the polylith-cli
Add the Polylith CLI as a dev dependency and setup the virtual environment paths.

``` shell
touch README.md

pdm add -d polylith-cli

pdm install

```

Next: create a Polylith workspace, with a basic Polylith folder structure.
The `poly` command is now available in the local virtual environment.
You can run commands in the context of `pdm run` to make Polylith aware of the development environment.

``` shell
pdm run poly create workspace --name my_namespace --theme loose
```

### Ready for coding!

Add components, bases and projects:

``` shell
pdm run poly create component --name my_component

pdm run poly create base --name my_example_endpoint

pdm run poly create project --name my_example_project
```

## Setup for Rye users
``` shell
rye init my_repo  # name your repo

cd my_repo

rye add polylith-cli --dev

rye sync  # create a virtual environment and lock files
```

Create a workspace, with a basic Polylith folder structure.

``` shell
rye run poly create workspace --name my_namespace --theme loose
```

## Setup for uv users
``` shell
uv init -name my_repo  # name your repo

cd my_repo

uv add polylith-cli --dev

uv sync  # create a virtual environment and lock files
```

Create a workspace, with a basic Polylith folder structure.

``` shell
uv run poly create workspace --name my_namespace --theme loose
```

### Rye and uv users: edit the configuration
The default build backend for Rye and uv is Hatch. Add the `hatch-polylith-bricks` build hook plugin to the `pyproject.toml` file.

``` toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.polylith-bricks]
# this section is needed to enable the hook in the build process, even if empty.
```

Make Rye and uv (and Hatch) aware of the way Polylith organizes source code:
``` toml
[tool.hatch.build]
dev-mode-dirs = ["components", "bases", "development", "."]
```

Run the `sync` command to update the virtual environment:


Rye:
``` shell
rye sync
```

uv:
``` shell
uv sync
```

Finally, remove the `src` boilerplate code that was added by Rye and uv in the first step:
``` shell
rm -r src
```

### Rye and uv users: ready for coding!

Add components, bases and projects:

Rye:
``` shell
rye run poly create component --name my_component

rye run poly create base --name my_example_endpoint

rye run poly create project --name my_example_project
```

uv:
``` shell
uv run poly create component --name my_component

uv run poly create base --name my_example_endpoint

uv run poly create project --name my_example_project
```

For details, have a look at the [documentation](https://davidvujic.github.io/python-polylith-docs/).
There, you will find guides for setup, migration, packaging, available commands, code examples and more.
