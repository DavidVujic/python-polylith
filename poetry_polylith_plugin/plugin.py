from poetry.console.application import Application
from poetry.plugins.application_plugin import ApplicationPlugin

from poetry_polylith_plugin.commands import create_component, create_workspace


class PolylithPlugin(ApplicationPlugin):
    def activate(self, application: Application):
        application.command_loader.register_factory(
            create_workspace.command_name, create_workspace.CreateWorkspaceCommand
        )

        application.command_loader.register_factory(
            create_component.command_name, create_component.CreateComponentCommand
        )
