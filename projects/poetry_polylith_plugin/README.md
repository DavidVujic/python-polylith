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

create a directory for your code and the basic Poetry setup

``` shell
mkdir my-repo-folder
cd my-repo-folder
git init

poetry init
```

This command will create a Polylith workspace, with a basic Polylith folder structure. 
Just define a __top namespace__ to be used when creating components and bases and the theme to use.

*new* `theme` is a new Python Polylith feature and defines what kind of component structure - or theme - to use.

`tdd` is the default and will set the structure according to the original Polylith Clojure implementation, such as:
`components/<package>/src/<namespace>/<package>` with a corresponding `test` folder.

`loose` is a new theme, for a more familiar structure for Python:
`components/<namespace>/<package>` and will put a `test` folder at the root of the repository.

#### Create
``` shell
poetry poly create workspace --name my_namespace --theme <tdd or loose>
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

#### Info
Show info about the workspace:

``` shell
poetry poly info
```

Shows what has changed since the most recent stable point in time:

``` shell
poetry poly diff
```

The `diff` command will compare the current state of the repository, compared to a `git tag`.
The tool will look for the latest tag according to a certain pattern, such as `stable-*`.
The pattern can be configured in `workspace.toml`.

#### Testing
The `create` commands will also create corresponding unit tests. It is possible to disable thi behaviour
by setting `enabled = false` in the `workspace.toml` file.


#### Workspace configuration
An example of a workspace configuration:

``` shell
[tool.polylith]
namespace = "my_namespace"
git_tag_pattern = "stable-*"

[tool.polylith.structure]
theme = "loose"

[tool.polylith.test]
enabled = true
```
