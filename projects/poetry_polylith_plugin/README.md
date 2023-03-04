# Poetry Polylith Plugin

This is a Python `Poetry` plugin, adding CLI support for the Polylith Architecture.

## Usage

### Install Poetry & plugins
With the `Poetry` version 1.2 or later installed, you can add plugins.

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

### Commands
The `create workspace` command will create a Polylith workspace, with a basic Polylith folder structure.


#### Create
``` shell
poetry poly create workspace --name my_namespace --theme <tdd or loose>
```

*New:* `theme` is a new Python Polylith feature and defines what kind of component structure - or theme - to use.

`tdd` is the default and will set the structure according to the original Polylith Clojure implementation, such as:
`components/<package>/src/<namespace>/<package>` with a corresponding `test` folder.

`loose` is a new theme, for a more familiar structure for Python:
`components/<namespace>/<package>` and will put a `test` folder at the root of the repository.


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

##### Options
`--description`
Add a brick description. The description will be added as a docstring.
Also in the brick-specific README (when set to enabled in the `resources` section of the workspace config).


#### Info
Show info about the workspace:

``` shell
poetry poly info
```

#### Diff
Shows what has changed since the most recent stable point in time:

``` shell
poetry poly diff
```

The `diff` command will compare the current state of the repository, compared to a `git tag`.
The tool will look for the latest tag according to a certain pattern, such as `stable-*`.
The pattern can be configured in `workspace.toml`.

The `diff` command is useful in a CI environment, to determine if a project should be deployed or not.
The command has a `--short` flag to only print a comma separated list of changed projects to the standard output.


Useful for CI:
``` shell
poetry poly diff --short
```


#### Libs
Show info about the third-party libraries used in the workspace:

``` shell
poetry poly libs
```

**NOTE**: this feature relies on installed project dependencies, and expects a `poetry.lock` of a project to be present.
If missing, there is a Poetry command available: `poetry lock --directory path/to-project`.

The very nice dependency lookup features of `Poetry` is used behind the scenes by the `poly libs` command.


##### Options
`--directory` or `-C`

Show info about libraries used in a specific project.


#### Check
Validates the Polylith workspace, checking for any missing dependencies (bricks and third-party libraries):

``` shell
poetry poly check
```

**NOTE**: this feature is built on top of the `poetry poly libs` command,
and (just like the `poetry poly libs` command) it expects a `poetry.lock` of a project to be present.
If missing, there is a Poetry command available: `poetry lock --directory path/to-project`.


##### Options
`--directory` or `-C`

Show info about libraries used in a specific project.


#### Testing
The `create` commands will also create corresponding unit tests. It is possible to disable this behaviour
by setting `enabled = false` in the `workspace.toml` file.


#### Workspace configuration
An example of a workspace configuration:

``` toml
[tool.polylith]
namespace = "my_namespace"
git_tag_pattern = "stable-*"

[tool.polylith.structure]
theme = "loose"

[tool.polylith.resources]
brick_docs_enabled = false

[tool.polylith.test]
enabled = true
```
