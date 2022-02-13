from pathlib import Path

from poetry_polylith_plugin.components import log, repo


template = """\
# A Python Polylith repo
The top namespace is `{namespace}`.


## Docs
The official Polylith documentation:
[high-level documentation](https://polylith.gitbook.io/polylith)

A Python implementation of the Polylith tool:
[poetry-polylith-plugin](https://github.com/DavidVujic/poetry-polylith-plugin#poetry-polylith-plugin)
"""


logger = log.getLogger()


def create_workspace_readme(path: Path, namespace: str):
    fullpath = path / repo.readme_file

    if fullpath.exists():
        logger.info(f"A {repo.readme_file} already exists. Skipping this step.")
        return

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(template.format(namespace=namespace))
