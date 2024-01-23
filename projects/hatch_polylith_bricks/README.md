# Hatch Build Hook for Polylith

A plugin for [Hatch](https://hatch.pypa.io/) and the Polylith Architecture.

This build hook will look for Polylith `bricks` in `pyproject.toml` and __optionally__ re-write the imports made in the source code.

## Installation
``` toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[tool.hatch.build.hooks.polylith-bricks]
# NOTE: this section is needed to enable the hook in the build process, even if empty
```

This Build Hook has two main usages:
* identify the included Polylith bricks from the `pyproject.toml`, and hand them over to the Hatch build process.
* add support for building Python libraries by re-writing source code with a custom top namespace.

Bricks are added to a project with relative paths, from the `bases` and `components` folders in a Polylith Workspace.
The hook will add the bricks to the Hatch in-memory build config (`force-include`) provided by the Hatch build process.
This will make the built `wheel` and `sdist` include proper paths to the source code.

Polylith Bricks are defined in the `tool.polylith.bricks` section of the `pyproject.toml`:

``` toml
[tool.polylith.bricks]
"../../bases/my_namespace/my_base" = "my_namespace/my_base"
"../../components/my_namespace/my_component" = "my_namespace/my_component
```

### Polylith documentation
[the Python tools for the Polylith Architecture](https://davidvujic.github.io/python-polylith-docs)


## Why re-write code?
Building libraries is supported in [the Python tools for the Polylith Architecture](https://davidvujic.github.io/python-polylith-docs),
but you will need to consider that code will share the same top namespace with any other library built from the same monorepo.

This can be a problem when more than one of your libraries are installed into the same virtual environment.
Python libraries by default are installed in a "flat" folder structure, two libraries with the same top namespace will collide.

_A Solution_: add a custom top namespace during packaging of the library with Hatch and this build hook plugin.

## How is this done?
The code in this repo uses __AST__ (Abstract Syntax Tree) parsing to modify source code.
The Python built-in `ast` module is used to parse and un-parse Python code.


### What's the output from this plugin?

Without any custom namespace in the configuration: no changes in the code. Building and packaging as-is.

#### With a Top Namespace configuration

``` toml
[tool.polylith.build]
top-namespace = "my_custom_namespace"
```

```shell
my_custom_namespace/
    my_namespace/
        /my_package
           __init__.py
           my_module.py
```

Before:
```python
from my_namespace.my_package import my_function
```

After:
```python
from my_custom_namespace.my_namespace.my_package import my_function
```

## Usage
| Key | Default | Description |
| --- | ------- | ----------- |
| work-dir | .polylith_tmp | The temporary working directory for copying and re-writing source code. |


## Polylith documentation
[the Python tools for the Polylith Architecture](https://davidvujic.github.io/python-polylith-docs)
