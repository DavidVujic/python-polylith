from pathlib import Path

from polylith.pdm.hooks.bricks import build_initialize


def pdm_build_initialize(context):
    context.ensure_build_dir()

    build_dir = Path(context.build_dir)

    build_initialize(context.config.root, context.config.data, build_dir)
