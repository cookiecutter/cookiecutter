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

from .utils import unicode_open
from .exceptions import InvalidConfiguration

_CONFIG = {}

# TODO: test on windows...
GLOB_SETTINGS_PATH = os.path.expanduser('~/.cookiecutter')

# TODO: figure out some sane default values
DEFAULT_SETTINGS = {
	'template_dirs': [],
	'default_context': {
  		'full_name': '{full_name}',
  		'email': '{email}',
  		'github_username': '{github_username}',
  	}
}

def get_config(config_path=GLOB_SETTINGS_PATH):
    """
    Retrieve the global settings and return them.
    """
    global _CONFIG
    if _CONFIG:
        return _CONFIG
    if not os.path.exists(config_path):
        create_config({}, config_path)	
    with unicode_open(config_path) as file_handle:
        try:
            global_config = yaml.load(file_handle)
        except yaml.scanner.ScannerError:
            raise InvalidConfiguration(
                "%s is no a valid YAML file" % config_path)

    return global_config

def create_config(params, path=GLOB_SETTINGS_PATH):
	"""
	Create a new config file at `path` with the default values defined in
	`params`.
	"""
	settings = DEFAULT_SETTINGS
	settings['template_dirs'] = params.pop('template_dirs', [])
	settings['default_context'].update(params)
	with unicode_open(path, 'w') as file_handle:
		file_handle.write(yaml.dump(settings, default_flow_style=False))
