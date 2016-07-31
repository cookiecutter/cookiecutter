# -*- coding: utf-8 -*-

import logging

LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL,
}

LOG_FORMATS = {
    'DEBUG': u'%(levelname)s [%(template)s] %(name)s: %(message)s',
    'INFO': u'%(levelname)s: %(message)s',
}


class ContextFilter(logging.Filter):
    """Logging filter that holds the name of the used template."""

    def __init__(self, template):
        super(ContextFilter, self).__init__()
        self.template = template

    def filter(self, record):
        """Add 'template' as extra information on a logging record."""
        record.template = self.template
        return record


def create_logger(template, level='DEBUG', log_file=None):
    # Get settings for given log level
    log_level = LOG_LEVELS[level]
    log_format = LOG_FORMATS[level]

    # Set up 'cookiecutter' logger
    logger = logging.getLogger('cookiecutter')
    logger.setLevel(log_level)

    # Remove all attached handlers, in case there was
    # a logger with using the name 'cookiecutter'
    del logger.handlers[:]

    # Add additional information to the logger
    context_filter = ContextFilter(template)

    # Create formatter based on the given level
    log_formatter = logging.Formatter(log_format)

    # Create a file handler if a log file is provided
    if log_file is not None:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(log_formatter)
        file_handler.addFilter(context_filter)
        logger.addHandler(file_handler)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(log_level)
    stream_handler.setFormatter(log_formatter)
    stream_handler.addFilter(context_filter)
    logger.addHandler(stream_handler)

    return logger
