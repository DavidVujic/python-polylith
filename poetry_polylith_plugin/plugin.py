from poetry.console.application import Application
from poetry.console.commands.command import Command
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_polylith_plugin.commands import (
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


def register_command(application: Application, command: Command):
    application.command_loader.register_factory(command.name, command)


def register_commands(application: Application):
    for command in commands:
        register_command(application, command)


class PolylithPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        register_commands(application)
