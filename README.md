# :sparkles: Python tools for the Polylith Architecture :sparkles:

A repo containing tooling support for the Polylith Architecture in Python.

The main use case is to support having one or more microservices (or apps) in a Monorepo, and share code between the services.

[![DavidVujic](https://circleci.com/gh/DavidVujic/python-polylith.svg?style=svg)](https://app.circleci.com/pipelines/github/DavidVujic/python-polylith?branch=main&filter=all)

[![CodeScene Code Health](https://codescene.io/projects/36630/status-badges/code-health)](https://codescene.io/projects/36630)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=DavidVujic_python-polylith&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=DavidVujic_python-polylith)

[![Download Stats](https://img.shields.io/pypi/dm/poetry-polylith-plugin?label=Poetry%20plugin%20Downloads)](https://pypistats.org/packages/poetry-polylith-plugin)

[![Download Stats](https://img.shields.io/pypi/dm/polylith-cli?label=CLI%20Downloads)](https://pypistats.org/packages/polylith-cli)


## What's Polylith? :thinking:
>... Polylith is a software architecture that applies functional thinking at the system scale. It helps us build simple, maintainable, testable, and scalable backend systems. ...
(from the [Polylith Architecture docs](https://polylith.gitbook.io/polylith/))

Polylith is an architecture, with tooling support, that was originally built for Clojure.
This repo brings __Polylith to Python__.

Polylith is using a components-first architecture.
You can think of it as building blocks, very much like LEGO bricks.
All code lives in a Monorepo, available for reuse.
Python code - the bricks - is separated from the infrastructure and the actual building of artifacts.

### Use cases

#### Microservices and apps :thumbsup:
The main use case is to support having one or more microservices (or apps) in a Monorepo, and share code between the services.

#### Libraries
Polylith for Python has support for building libraries to be published at PyPI, even if it isn't the main use case.
More details about how to package libraries in the docs about [Packaging & deploying](https://davidvujic.github.io/python-polylith-docs/deployment/#packaging-a-library).

## Documentation :books:
Have a look at the [Python-specific documentation](https://davidvujic.github.io/python-polylith-docs/).
You will find installation, setup, usage guides, examples and more.

## Python Monorepos with Polylith :snake:
You can use Polylith with Poetry, Hatch, PDM, Rye, uv and Pantsbuild.
This repo contains a Poetry plugin, a standalone CLI and build hooks.

* [a Poetry Plugin](https://pypi.org/project/poetry-polylith-plugin)
* [a CLI](https://pypi.org/project/polylith-cli)
* [a Hatch Build Hook](https://pypi.org/project/hatch-polylith-bricks/)
* [a PDM Build Hook for projects](https://pypi.org/project/pdm-polylith-bricks/)
* [a PDM Build Hook for the workspace](https://pypi.org/project/pdm-polylith-workspace/)

The Poetry plugin adds tooling support to Poetry.
The CLI adds tooling support for several Package & Dependency Managers (such as Hatch, PDM, Rye and uv).

The Hatch Build Hook adds build-specific support (also for uv, Rye and Pantsbuild, using hatchling as the build backend).
The PDM Build Hook for _projects_ adds build-specific support for PDM.
The PDM Build Hook for the _workspace_ makes the virtual environment aware of the way Polylith organizes code (i.e. the bases and components folders).

## :sparkles: Examples and Production systems :sparkles:
There's example Polylith repositories for:
- [Poetry](https://github.com/DavidVujic/python-polylith-example)
- [Hatch](https://github.com/DavidVujic/python-polylith-example-hatch)
- [PDM](https://github.com/DavidVujic/python-polylith-example-pdm)
- [Rye](https://github.com/DavidVujic/python-polylith-example-rye)
- [Pants](https://github.com/DavidVujic/python-polylith-example-pants)
- [uv](https://github.com/DavidVujic/python-polylith-example-uv)

The repositories are example __Python__ setups of the Polylith Architecture.
You will find examples of sharing code between different kind of projects,
and developer tooling setup such as `mypy` and the `venv`.

There's more examples and production systems in the [documentation](https://davidvujic.github.io/python-polylith-docs/examples/).

## Videos
- Python with the Polylith Architecture - [an overview](https://youtu.be/3w2ffHZb6gc) (about 15 minutes)
- Python Poetry Polylith Plugin - [the tooling support & commands](https://youtu.be/AdKpTP9pjHI) (about 13 minutes)
- The Developer Experience
    - [developing a Dad Joke Service with Polylith](https://youtu.be/oG4OFEer3Tk) (about 27 minutes)
    - [the Polylith Dev Experience using Hatch and Rye](https://youtu.be/BXPQBXuiRwM?si=rQ70ESrY-hRDazBi) (about 7 minutes)
- The standalone Polylith CLI - [An intro to the polylith-cli - tooling support for Polylith with Python and Hatch](https://youtu.be/K__3Uah3by0)

## Talks
- __PyCon DE & PyData Berlin 2024__ - [Python Monorepos: The Polylith Developer Experience](https://youtu.be/wGWjt9GJLU4?si=1nOpThiwayc4Crvm) (about 29 minutes)
- __Python Web Conference 2023__ - Microservices, Monolith, Monorepos: the differences & how nicely Polylith solves the trade offs - [A Fresh Take on Monorepos in Python](https://youtu.be/HU61vjZPPfQ) (about 36 minutes)

## Podcasts
- __Talk Python To Me__: [Monorepos in Python](https://talkpython.fm/episodes/show/399/monorepos-in-python)

## Articles
- [The last Python Architecture you will ever need?](https://davidvujic.blogspot.com/2022/11/the-last-python-architecture-you-will-ever-need.html)
- [A Fresh Take on Monorepos in Python](https://davidvujic.blogspot.com/2022/02/a-fresh-take-on-monorepos-in-python.html)
- [A simple & scalable Python project structure](https://davidvujic.blogspot.com/2022/08/a-simple-scalable-python-project.html)
- [Aws CDK App with polylith code architecture](https://dev.to/ybenitezf/aws-cdk-app-with-polylith-code-architecture-30e3) by Yoel Benítez Fonseca
- [GCP Cloud Functions with Python and Polylith](https://davidvujic.blogspot.com/2023/07/gcp-cloud-functions-with-python-and-polylith.html)
- [Python FastAPI Microservices with Polylith](https://davidvujic.blogspot.com/2023/07/python-fastapi-microservices-with-polylith.html)
- [Kafka messaging with Python & Polylith](https://davidvujic.blogspot.com/2023/08/kafka-messaging-with-python-and-polylith.html)
- [Runestone Monorepo and Server Structure](https://medium.com/@thaopham03/runestone-monorepo-and-server-structure-0754dbc52f48) by Minh-Thao Pham
- [Python Monorepo Visualization](https://davidvujic.blogspot.com/2024/02/python-monorepo-visualization.html)

## Repo Visualization
A visualization of this repo (that itself is a Polylith workspace) using the `poly info` command.

<img width="698" alt="poly-info" src="https://github.com/DavidVujic/python-polylith/assets/301286/692581b6-e5ad-48b4-8fac-9a2aac83942f">

