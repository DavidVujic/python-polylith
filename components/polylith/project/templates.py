poetry_pyproject_template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
{description}
{authors}
license = ""

packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

poetry_pep621_pyproject_template = """\
[tool.poetry]
packages = []

[project]
name = "{name}"
version = "0.1.0"
{description}
{authors}

requires-python = "{python_version}"

dependencies = []

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

hatch_pyproject_template = """\
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
{description}
{authors}

requires-python = "{python_version}"

dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["{namespace}"]

[tool.hatch.build.hooks.polylith-bricks]

[tool.polylith.bricks]
"""

pdm_pyproject_template = """\
[build-system]
requires = ["pdm-backend", "pdm-polylith-bricks"]
build-backend = "pdm.backend"

[project]
name = "{name}"
version = "0.1.0"
{description}
{authors}

requires-python = "{python_version}"

dependencies = []

[tool.polylith.bricks]
"""
poetry_pyproject_template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
{description}
{authors}
license = ""

packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

poetry_pep621_pyproject_template = """\
[tool.poetry]
packages = []

[project]
name = "{name}"
version = "0.1.0"
{description}
{authors}

requires-python = "{python_version}"

dependencies = []

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

hatch_pyproject_template = """\
[build-system]
requires = ["hatchling", "hatch-polylith-bricks"]
build-backend = "hatchling.build"

[project]
name = "{name}"
version = "0.1.0"
{description}
{authors}

requires-python = "{python_version}"

dependencies = []

[tool.hatch.build.targets.wheel]
packages = ["{namespace}"]

[tool.hatch.build.hooks.polylith-bricks]

[tool.polylith.bricks]
"""

pdm_pyproject_template = """\
[build-system]
requires = ["pdm-backend", "pdm-polylith-bricks"]
build-backend = "pdm.backend"

[project]
name = "{name}"
version = "0.1.0"
{description}
{authors}

requires-python = "{python_version}"

dependencies = []

[tool.polylith.bricks]
"""
