#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.config
-------------------

Global configuration handling
"""

from __future__ import unicode_literals
import copy
import logging
import os
import io

import yaml

from .exceptions import ConfigDoesNotExistException
from .exceptions import InvalidConfiguration


logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    'cookiecutters_dir': os.path.expanduser('~/.cookiecutters/'),
    'default_context': {}
}

# TODO: test on windows...
USER_CONFIG_PATH = '~/.cookiecutterrc'


def get_config(config_path):
    """
    Retrieve the config from the specified path, returning it as a config dict.
    """

    if not os.path.exists(config_path):
        raise ConfigDoesNotExistException

    logger.debug('config_path is {0}'.format(config_path))
    with io.open(config_path, encoding='utf-8') as file_handle:
        try:
            yaml_dict = yaml.safe_load(file_handle)
        except yaml.scanner.ScannerError:
            raise InvalidConfiguration(
                '{0} is no a valid YAML file'.format(config_path))

    config_dict = copy.copy(DEFAULT_CONFIG)
    config_dict.update(yaml_dict)

    return config_dict


def get_user_config(rc_file=USER_CONFIG_PATH):
    """
    Retrieve config from the given path, if it exists.
    Otherwise, return a deep copy of the defaults.

    :param rc_file: Path to the user configuration file
    """
    rc_file = os.path.expanduser(rc_file or '')
    if rc_file and os.path.exists(rc_file):
        return get_config(rc_file)
    else:
        return copy.copy(DEFAULT_CONFIG)
