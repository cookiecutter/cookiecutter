"""Module for setting up logging."""

from __future__ import annotations

import logging
import sys

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

LOG_FORMATS = {
    'DEBUG': '%(levelname)s %(name)s: %(message)s',
    'INFO': '%(levelname)s: %(message)s',
}


def configure_logger(
    stream_level: str = 'DEBUG', debug_file: str | None = None
) -> logging.Logger:
    """Configure logging for cookiecutter.

    Set up logging to stdout with given level. If ``debug_file`` is given set
    up logging to file with DEBUG level.
    """
    # Set up 'cookiecutter' logger
    logger = logging.getLogger('cookiecutter')
    logger.setLevel(logging.DEBUG)

    # Remove all attached handlers, in case there was
    # a logger with using the name 'cookiecutter'
    del logger.handlers[:]

    # Create a file handler if a log file is provided
    if debug_file is not None:
        debug_formatter = logging.Formatter(LOG_FORMATS['DEBUG'])
        file_handler = logging.FileHandler(debug_file)
        file_handler.setLevel(LOG_LEVELS['DEBUG'])
        file_handler.setFormatter(debug_formatter)
        logger.addHandler(file_handler)

    # Get settings based on the given stream_level
    log_formatter = logging.Formatter(LOG_FORMATS[stream_level])
    log_level = LOG_LEVELS[stream_level]

    # Create a stream handler
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(log_formatter)
    logger.addHandler(stream_handler)

    return logger
