# Hatch Build Hook for Polylith

A plugin for [Hatch](https://github.com/pypa/hatch) and the Polylith Architecture.

This build hook will look for Polylith `bricks` in `pyproject.toml` and __optionally__ re-write the imports made in the source code.

## Installation
``` toml
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"
```

## But why re-write code?
Building libraries is supported in [the Python tools for the Polylith Architecture](https://davidvujic.github.io/python-polylith-docs),
but you will need to consider that code will share the same top namespace with any other library built from the same monorepo.

This can be a problem when more than one of your libraries are installed into the same virtual environment.
Python libraries by default are installed in a "flat" folder structure, two libraries with the same top namespace will collide.

The Solution: add a custom top namespace during packaging of the library with Hatch and this build hook plugin.

## How is this done?
The code in this repo uses __AST__ (Abstract Syntax Tree) parsing to modify source code.
The Python built-in `ast` module is used to parse and un-parse Python code.


### What's the output from this plugin?

Without any custom namespace in the configuration: no changes in the code. Building and packaging as-is.

#### With a Top Namespace configuration

``` toml
[tool.hatch.build.hooks.polylith-bricks]
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
| top-namespace | None | A custom top namespace. When set, Polylith bricks will be updated using this namespace. |


This Plugin expects to find Polylith Bricks in the `pyproject.toml`:

``` toml
[tool.polylith.bricks]
"../../bases/my_namespace/my_base" = "my_namespace/my_base"
"../../components/my_namespace/my_component" = "my_namespace/my_component
```

## Documentation
[the Python tools for the Polylith Architecture](https://davidvujic.github.io/python-polylith-docs)
