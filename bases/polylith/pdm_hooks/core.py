from polylith import pdm


def pdm_build_initialize(context):
    context.ensure_build_dir()

    pdm.hooks.bricks.build_initialize(context.config.data)
