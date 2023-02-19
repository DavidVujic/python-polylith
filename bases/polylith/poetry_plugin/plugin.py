from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin
from polylith.poetry.commands import (
    CheckCommand,
    CreateBaseCommand,
    CreateComponentCommand,
    CreateProjectCommand,
    CreateWorkspaceCommand,
    DiffCommand,
    InfoCommand,
    LibsCommand,
)

commands = [
    CheckCommand,
    CreateBaseCommand,
    CreateComponentCommand,
    CreateProjectCommand,
    CreateWorkspaceCommand,
    DiffCommand,
    InfoCommand,
    LibsCommand,
]


def register_command(application: Application, command) -> None:
    application.command_loader.register_factory(command.name, command)


def register_commands(application: Application) -> None:
    for command in commands:
        register_command(application, command)


class PolylithPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        register_commands(application)
