# Python CLI for Polylith

Python CLI support for the Polylith Architecture.

# WIP
__TODO:__ add docs, with hatch as an example

## Documentation
Have a look at the [documentation](https://davidvujic.github.io/python-polylith-docs/).
You will find installation, setup, usage guides and more.

## Quick start

Create a directory for your code, initialize it with __git__:

``` shell
git init
```

Next: create a Polylith workspace, with a basic Polylith folder structure.

``` shell
poly create workspace --name my_namespace --theme loose
```

Time to start coding. Add components, bases and projects:

``` shell
poly create component --name my_component

poly create base --name my_example_endpoint

poly create project --name my_example_project
```

For details, have a look at the [documentation](https://davidvujic.github.io/python-polylith-docs/).
There, you will find guides for setup, migration, packaging, available commands, code examples and more.
