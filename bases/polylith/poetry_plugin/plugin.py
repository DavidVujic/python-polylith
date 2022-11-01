from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin
from polylith.poetry_command import (
    CreateBaseCommand,
    CreateComponentCommand,
    CreateProjectCommand,
    CreateWorkspaceCommand,
    InfoCommand,
)

commands = [
    CreateBaseCommand,
    CreateComponentCommand,
    CreateProjectCommand,
    CreateWorkspaceCommand,
    InfoCommand,
]


def register_command(application: Application, command: Command) -> None:
    application.command_loader.register_factory(command.name, command)


def register_commands(application: Application) -> None:
    for command in commands:
        register_command(application, command)


class PolylithPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        register_commands(application)
