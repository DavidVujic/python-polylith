from hatchling.plugin import hookimpl

from polylith.hatch_bricks_build_hook.plugin import PolylithBricksHook


@hookimpl
def hatch_register_build_hook():
    return PolylithBricksHook
