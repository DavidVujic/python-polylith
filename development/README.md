# Development


## Build and install local version
Make sure to uninstall the properly installed version (via Poetry):

``` shell
poetry self remove poetry-polylith-plugin
```

Build version from your local folder:
``` shell
poetry build-project --directory projects/poetry_polylith_plugin
```

Install into the Poetry virtual environment (Mac OS X) with pip:
``` shell
~/Library/Application\ Support/pypoetry/venv/bin/pip install projects/poetry_polylith_plugin/dist/poetry_polylith_plugin-<INSERT-VERSION-HERE>-py3-none-any.whl
```

When done testing, don't forget to uninstall the local test version:
``` shell
~/Library/Application\ Support/pypoetry/venv/bin/pip uninstall poetry-polylith-plugin
```

