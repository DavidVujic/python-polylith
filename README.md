# poetry-polylith-plugin

This is a Python `Poetry` plugin, adding CLI support for the Polylith architecture.


## Polylith?
From the [official docs](https://polylith.gitbook.io/polylith/):
"... Polylith is a software architecture that applies functional thinking at the system scale.
It helps us build simple, maintainable, testable, and scalable backend systems. ..."

There seems to be an ongoing trend in software development towards using __monorepos__.

This trend is something especially seen in the __Clojure__ community. Polylith is an architecture, and a tool built for Clojure.


__This Poetry Plugin brings Polylith to Python!__


## Polylith - a monorepo architecture
Polylith is using a components-first architecture. Similar to LEGO, components are building blocks.
A component can be shared across apps, tools, libraries, serverless functions and services. 


## Usage
This plugin depends on the latest version - a preview - of [Poetry](https://python-poetry.org/)
with functionality for adding custom Plugins. Have a look at the [official Poetry preview docs](https://python-poetry.org/docs/master/) for how to install it.

### Install Poetry & plugins
With the latest `Poetry` version installed, you can add plugins.

Add the [Multiproject](https://github.com/DavidVujic/poetry-multiproject-plugin) plugin, that will enable the very important __workspace__ support to Poetry.
``` shell
poetry plugin add poetry-multiproject-plugin
```

Add the Polylith plugin:
``` shell
poetry plugin add poetry-polylith-plugin
```

Done!

### Commands
Creating a new repo.

``` shell
# create a directory for your code
mkdir my-repo-folder
cd my-repo-folder
git init

# This command will create a basic pyproject.toml file.
poetry init

# This command will create a Polylith workspace, with the basic Polylith folder structure and
# define a top namespace to be used when creating components and bases.
poetry poly create workspace --name my_namespace
```

Add a component:

``` shell
# This command will create a component - i.e. a Python package in a namespaced folder.
poetry poly create component --name my_component
```

Add a base:

``` shell
# This command will create a base - i.e. a Python package in a namespaced folder.
poetry poly create base --name my_example_aws_lambda
```

Add a project:

``` shell
# This command will create a project - i.e. a pyproject.toml in a project folder. No code in this folder.
poetry poly create project --name my_example_aws_lambada_project
```

## Differences between the Clojure & Python implementations
First, this plugin only has the very basic features (yet). Functionality will be added, step by step.

In the [official docs](https://polylith.gitbook.io/polylith/) - and in the `components` section in particular,
there is a `interface.clj` file, used to separate an API from the implementation of a component.

The Python implementation uses the `__init__.py` to accomplish that.

In the Python implementation, the `pyproject.toml` is used to define bases and components.

In particular, the `packages` property is used for that.

This is the top level `pyproject.toml` used during development.
``` shell
 packages = [
    {include = "dev", from = "development/src"},
    {include = "my_namespace/my_component", from = "components/my_component/src"},
    {include = "my_namespace/my_example_aws_lambda", from = "bases/my_example_lambda/src"},
]
```

When creating a project, the project specific `pyproject.toml` will include all the used components and bases.
Note that the packages are referenced relative to the project. This is enabled by the `Multiproject` plugin.
``` shell
 packages = [
    {include = "my_namespace/my_component", from = "../../components/my_component/src"},
    {include = "my_namespace/my_example_aws_lambda", from = "../../bases/my_example_lambda/src"},
]
``` 
