# Python tools for the Polylith Architecture

This is a repo containing tooling support for using the Polylith Architecture in Python.

[![DavidVujic](https://circleci.com/gh/DavidVujic/poetry-polylith-plugin.svg?style=svg)](https://app.circleci.com/pipelines/github/DavidVujic/poetry-polylith-plugin?branch=main&filter=all)

## What's Polylith?
From the [official docs](https://polylith.gitbook.io/polylith/):
"... Polylith is a software architecture that applies functional thinking at the system scale.
It helps us build simple, maintainable, testable, and scalable backend systems. ..."

Polylith is an architecture (with tooling support) originally built for Clojure.

__The code in this repo brings Polylith to Python!__

### A monorepo architecture
Polylith is using a components-first architecture. Similar to LEGO, components are building blocks.
A component can be shared across apps, tools, libraries, serverless functions and services.

## Python Polylith tools
Currently, this repo contains a Poetry plugin, that will add Polylith specific tooling support to Poetry.

Have a look in the [Poetry Polylith Plugin project folder](projects/poetry_polylith_plugin/README.md) for more info.

## Differences between the Clojure & Python implementations
First, the code here contains the very basic features (so far). Functionality will be added, step by step.

In the [official docs](https://polylith.gitbook.io/polylith/) - and in the `components` section in particular,
there is a `interface.clj` file, used to separate an API from the implementation of a component.

The Python implementation uses the `__init__.py` to accomplish that.

In the Python implementation, the `pyproject.toml` is used to define bases and components. In particular, the `packages` property is used for that.

This is the top level `pyproject.toml` used during development.
``` shell
 packages = [
    {include = "development"},
    {include = "my_namespace/my_component", from = "components"},
    {include = "my_namespace/my_example_aws_lambda", from = "bases"},
]
```

When creating a project, the project specific `pyproject.toml` will include all the used components and bases.
Note that the packages are referenced relative to the project. This is enabled by the `Multiproject` plugin.
``` shell
 packages = [
    {include = "my_namespace/my_component", from = "../../components"},
    {include = "my_namespace/my_example_aws_lambda", from = "../../bases"},
]
``` 
