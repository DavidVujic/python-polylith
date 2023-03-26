# Poetry Polylith Plugin

This is a Python `Poetry` plugin, adding CLI support for the Polylith Architecture.

## Documentation
Have a look at the [documentation](https://davidvujic.github.io/python-polylith-docs/).
You will find installation, setup, usage guides and more.

## Quick start

### Install Poetry & plugins
With the `Poetry` version 1.2 or later installed, you can add plugins.


Make sure that you have `Poetry` 1.2 or later installed.

Add the [Multiproject](https://github.com/DavidVujic/poetry-multiproject-plugin) plugin, that will enable the very important __workspace__ support (i.e. relative package includes) to Poetry.
``` shell
poetry self add poetry-multiproject-plugin
```

Add the Polylith plugin:
``` shell
poetry self add poetry-polylith-plugin
```

### Create a repository
Create a directory for your code, initialize it with __git__ and create a basic __Poetry__ setup:

``` shell
git init

poetry init
```

Next: create a Polylith workspace, with a basic Polylith folder structure.

``` shell
poetry poly create workspace --name my_namespace --theme loose
```

Time to start coding. Add a component:

``` shell
poetry poly create component --name my_component
```
This command will create a component - i.e. a Python package in a namespaced folder.

Add a base:

``` shell
poetry poly create base --name my_example_aws_lambda
```
This command will create a base - i.e. a Python package in a namespaced folder.

Add a project:

``` shell
poetry poly create project --name my_example_aws_lambada_project
```
This command will create a project - i.e. a pyproject.toml in a project folder. No code in this folder.

Make sure to read the [documentation](https://davidvujic.github.io/python-polylith-docs/).
There, you will find guides for setup, migrations, packaging, available commands and code examples.
