import logging

GLOBAL_LOGGING_LEVEL = logging.DEBUG


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(GLOBAL_LOGGING_LEVEL)

    handler = logging.FileHandler("warden.log")
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
