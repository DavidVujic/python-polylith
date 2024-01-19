from hatchling.plugin import hookimpl

from polylith.hatch_hooks.bricks.plugin import PolylithBricksHook


@hookimpl
def hatch_register_build_hook():
    return PolylithBricksHook
