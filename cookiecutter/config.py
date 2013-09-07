#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.config
-------------------

Global configuration handling
"""

import logging
import os
import sys

import yaml

from .exceptions import ConfigDoesNotExistException
from .utils import unicode_open
from .exceptions import InvalidConfiguration


# TODO: figure out some sane default values, or if this is needed
DEFAULT_SETTINGS = {
	'template_dirs': [],
	'default_context': {}
}


def get_config(config_path):
    """
    Retrieve the config from the specified path, and return it as a config dict.
    """

    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException

    with unicode_open(config_path) as file_handle:
        try:
            global_config = yaml.load(file_handle)
        except yaml.scanner.ScannerError:
            raise InvalidConfiguration(
                "%s is no a valid YAML file" % config_path)

    return global_config


def get_user_config():
    """
    Retrieve config from the user's ~/.cookiecutterrc, if it exists.
    Otherwise, return None.
    """
    
    # TODO: test on windows...
    USER_CONFIG_PATH = os.path.expanduser('~/.cookiecutter')

    if os.path.exists(USER_CONFIG_PATH):
        return get_config(USER_CONFIG_PATH)
    return None
