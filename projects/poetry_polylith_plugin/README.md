# poetry-polylith-plugin

This is a Python `Poetry` plugin, adding CLI support for the Polylith architecture.


## Usage

### Install Poetry & plugins
With the `Poetry` version 1.2 or later installed, you can add plugins.

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

Show info about the workspace:

``` shell
poetry poly info
```
__Note__: the `info` command currently displays the very basic workspace info. The feature is currently developed.
Stay tuned for upcoming versions!
