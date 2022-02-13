import logging


def getHandler():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(name)s: %(message)s")

    handler.setFormatter(formatter)

    return handler


def getLogger(name="poetry-polylith-plugin"):
    logger = logging.getLogger(name)

    if not logger.hasHandlers():
        handler = getHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
