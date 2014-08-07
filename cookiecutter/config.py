#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.config
-------------------

Global configuration handling
"""

from __future__ import unicode_literals
import copy
import os

from .exceptions import ConfigDoesNotExistException
from .utils import read_yaml_file


DEFAULT_CONFIG = {
    'cookiecutters_dir': os.path.expanduser('~/.cookiecutters/'),
    'default_context': {}
}


def get_config(config_path):
    """
    Retrieve the config from the specified path, returning it as a config dict.
    """

    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException

    print("config_path is {0}".format(config_path))

    yaml_dict = read_yaml_file(config_path)
    config_dict = copy.copy(DEFAULT_CONFIG)
    config_dict.update(yaml_dict)

    return config_dict


def get_user_config():
    """
    Retrieve config from the user's ~/.cookiecutterrc, if it exists.
    Otherwise, return None.
    """

    # TODO: test on windows...
    USER_CONFIG_PATH = os.path.expanduser('~/.cookiecutterrc')

    if os.path.exists(USER_CONFIG_PATH):
        return get_config(USER_CONFIG_PATH)
    return copy.copy(DEFAULT_CONFIG)
