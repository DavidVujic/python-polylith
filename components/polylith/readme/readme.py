from pathlib import Path

from polylith import log, repo

template = """\
# A Python Polylith repo

## Docs
The official Polylith documentation:
[high-level documentation](https://polylith.gitbook.io/polylith)

A Python implementation of the Polylith tool:
[python-polylith](https://github.com/DavidVujic/python-polylith)
"""


logger = log.getLogger()


def create_workspace_readme(path: Path, namespace: str) -> None:
    fullpath = path / repo.readme_file

    if fullpath.exists():
        logger.info(f"A {repo.readme_file} already exists. Skipping this step.")
        return

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(template.format(namespace=namespace))
