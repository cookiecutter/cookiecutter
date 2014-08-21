#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.settings
---------------------

Handling of template settings files
"""

import os
import io
import sys

import yaml

from .exceptions import MultipleTemplateSettingsException, MissingTemplateSettingsException


if sys.version_info[:2] < (2, 7):
    import simplejson as json
    from ordereddict import OrderedDict
else:
    import json
    from collections import OrderedDict


def get_default_settings(version=2):
    return {'config': {'version': version}, 'context': {}}


def get_settings(name, default_context=None):
    """Get template settings from a YAML or JSON file"""

    stem = os.path.basename(name)
    yaml_file = name + '.yaml'
    json_file = name + '.json'

    # Check whether there is a YAML file or a JSON file, and load it.
    # Having both is an error, having neither gives the default.
    # TODO: Should having neither be an error?
    if os.path.exists(yaml_file) and os.path.exists(json_file):
        raise MultipleTemplateSettingsException
    elif os.path.exists(yaml_file):
        settings = get_yaml_settings(yaml_file)
    elif os.path.exists(json_file):
        settings = get_json_settings(json_file)
    else:
        raise MissingTemplateSettingsException

    # Use the default_context argument to override values in the context
    if default_context:
        settings['context'].update(default_context)

    # The context from the file should be under the filename stem as a key
    settings['context'] = {stem: settings['context']}

    return settings


def get_context_from_settings(settings):
    """Get the context part of the settings.

    Trivial at the moment, but will become more complex when we have context
    metadata like types and prompts.
    """
    return settings['context']


def get_yaml_settings(name):
    with open(name, 'rb') as f:
        return yaml.load(f)


def get_json_settings(name):
    with io.open(name, encoding='utf-8') as f:
        # The JSON file just contains the context.
        context = json.load(f, object_pairs_hook=OrderedDict)
        settings = get_default_settings(version=1)
        settings['context'] = context
        return settings
