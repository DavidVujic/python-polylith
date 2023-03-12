# :sparkles: Python tools for the Polylith Architecture :sparkles:

A repo containing tooling support for the Polylith Architecture in Python.

[![DavidVujic](https://circleci.com/gh/DavidVujic/python-polylith.svg?style=svg)](https://app.circleci.com/pipelines/github/DavidVujic/python-polylith?branch=main&filter=all)


[![CodeScene general](https://codescene.io/images/analyzed-by-codescene-badge.svg)](https://codescene.io/projects/36630)


## What's Polylith? :thinking:
Polylith is an architecture (with tooling support) originally built for Clojure. The code in this repo brings __Polylith to Python__.

From the [official Polylith Architecture docs](https://polylith.gitbook.io/polylith/):
>... Polylith is a software architecture that applies functional thinking at the system scale. It helps us build simple, maintainable, testable, and scalable backend systems. ...

Polylith is using a components-first architecture. Similar to LEGO, components are building blocks.
A component can be shared across apps, serverless functions and microservices.

## Documentation :books:
Have a look at the [Python-specific documentation](https://davidvujic.github.io/python-polylith-docs/).
You will find installation, setup, usage guides and more.

## Polylith for Python? :snake:
This repo contains a Poetry plugin, that you can install from [PyPI](https://pypi.org/project/poetry-polylith-plugin).
The plugin will add Polylith specific tooling support to Poetry.
Have a look in the [Poetry Polylith Plugin project folder](projects/poetry_polylith_plugin/README.md) with details about the Poetry plugin.

### Use cases

#### Microservices and apps :thumbsup:
The main use case is to support having one or more microservices (or apps) in a Monorepo, and share code between the services.

#### Libraries?
Polylith for Python isn't mainly for building libraries published to PyPI, even if it is supported.
Consider that the code in one library will share the same top namespace with other libraries that are
built from the same Polylith Monorepo. This will likely be a problem when _more than one_ of your libraries would be installed into the same virtual environment.

There is [solution](https://github.com/DavidVujic/poetry-multiproject-plugin#usage-for-libraries) avaiable for this. :smiley:

## :sparkles: Examples :sparkles:
Have a look at the [Python Polylith Examples](https://github.com/DavidVujic/python-polylith-example) repository.
It is a repository with an example __Python__ setup of the Polylith Architecture.
You will find examples of sharing code between different kind of projects, and developer tooling setup such as `mypy` and the `venv`.

## Videos
* Python with the Polylith Architecture - [an overview](https://youtu.be/3w2ffHZb6gc) (about 15 minutes)
* Python Poetry Polylith Plugin - [the tooling support & commands](https://youtu.be/AdKpTP9pjHI) (about 13 minutes)
<img width="640" alt="poly-info-example" src="https://user-images.githubusercontent.com/301286/203044825-b84371e8-caa8-4f85-8c94-4a5f3af887d6.png">
