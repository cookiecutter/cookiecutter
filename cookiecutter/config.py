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

if sys.version_info[:2] < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict

from .utils import unicode_open

# TODO: test on windows...
GLOB_SETTINGS_PATH = os.path.expanduser('~/.cookiecutter')

DEFAULT_SETTINGS = \
"""{{
	"template_dirs": [
		{template_dirs}
	],
	"default_context": {{
		"full_name": "{full_name}",
		"email": "{email}",
		"github_username": "{github_username}"
	}}
}}"""


def get_config(config_path=GLOB_SETTINGS_PATH):
	"""
	Retrieve the global settings and return them.
	"""
	if not os.path.exists(config_path):
		return create_config({
			'template_dirs': [],
			'full_name': '',
			'email': '',
			'github_username': ''	
		}, config_path)	# TODO: figure out some sane default values
	with unicode_open(config_path) as file_handle:
		#global_config = _json_parse(file_handle.read(), object_pairs_hook=OrderedDict)
		global_config = json.load(file_handle, object_pairs_hook=OrderedDict)

	return global_config

def create_config(params, path=GLOB_SETTINGS_PATH):
	"""
	Create a new config file at `path` with the default values defined in
	`params`.
	"""
	params['template_dirs'] = ',\n'.join(['"%s"' % p for p in params['template_dirs']])
	with unicode_open(path, 'w') as file_handle:
		file_handle.write(DEFAULT_SETTINGS.format(**params))
	return get_config(path)
