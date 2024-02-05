# Development


## Build and install local version
Make sure to uninstall the properly installed version you have via Poetry:

``` shell
poetry self remove poetry-polylith-plugin
```

Build a wheel from your local folder:
``` shell
poetry build-project --directory projects/poetry_polylith_plugin
```

Install into the Poetry virtual environment (Mac OS X), with pip:
``` shell
~/Library/Application\ Support/pypoetry/venv/bin/pip install projects/poetry_polylith_plugin/dist/poetry_polylith_plugin-<INSERT-VERSION-HERE>-py3-none-any.whl
```

When done testing, don't forget to uninstall the local test version:
``` shell
~/Library/Application\ Support/pypoetry/venv/bin/pip uninstall poetry-polylith-plugin
```

## Packaging notes
Developer notes about how to package the artifacts, using custom top namespaces.

The Poetry plugin:
``` shell
poetry build-project --directory projects/poetry_polylith_plugin
```

The CLI:
``` shell
poetry build-project --directory projects/polylith_cli --with-top-namespace polylith_cli
```

The Hatch build hook:
``` shell
poetry build-project --directory projects/hatch_polylith_bricks --with-top-namespace hatch_polylith_bricks
```

The PDM project build hook:
``` shell
poetry build-project --directory projects/pdm_polylith_bricks --with-top-namespace pdm_polylith_bricks
```

The PDM Workspace build hook:
``` shell
poetry build-project --directory projects/pdm_polylith_workspace --with-top-namespace pdm_polylith_workspace
```

