poetry_pyproject = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = "{description}"
authors = {authors}
license = ""

packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

hatch_pyproject = """\
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
authors = {authors}

requires-python = "{python_version}"

dependencies = []

[tool.hatch.build.hooks.polylith-bricks]

[tool.polylith.bricks]
"""

pdm_pyproject = """\
[build-system]
requires = ["pdm-backend", "pdm-polylith-bricks"]
build-backend = "pdm.backend"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
authors = {authors}

requires-python = "{python_version}"

dependencies = []

[tool.polylith.bricks]
"""
