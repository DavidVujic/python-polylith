from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry.console.commands.command import Command


class TemporaryCommand(Command):
    name = "poly create workspace"

    def handle(self) -> int:
        self.line("Hello World from the Poetry Polylith Plugin")

        return 0


class PolylithPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.command_loader.register_factory(
            TemporaryCommand.name, TemporaryCommand
        )
