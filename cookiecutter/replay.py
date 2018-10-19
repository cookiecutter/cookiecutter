# -*- coding: utf-8 -*-

"""All functions specific to Replay Project Generation are defined here."""

from __future__ import unicode_literals

import json
import os
from past.builtins import basestring

from .utils import make_sure_path_exists


def get_file_name(replay_dir, template_name):
    """Generate a JSON file name and return its absolute path."""
    file_name = '{}.json'.format(template_name)
    return os.path.join(replay_dir, file_name)


def dump(replay_dir, template_name, context):
    """Create a replay file to save user input for a template."""
    if not make_sure_path_exists(replay_dir):
        # Inform the user of the directory being non existent.
        raise IOError('Unable to create replay dir at {}'.format(replay_dir))

    if not isinstance(template_name, basestring):
        # Require the template name only in the form of a string.
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        # Require the context only in the form of a dictionary.
        raise TypeError('Context is required to be of type dict')

    if 'cookiecutter' not in context:
        # Throw an exception if the cookiecutter key is not in the context.
        raise ValueError('Context is required to contain a cookiecutter key')

    replay_file = get_file_name(replay_dir, template_name)

    # Write the context to JSON file.
    with open(replay_file, 'w') as outfile:
        json.dump(context, outfile)


def load(replay_dir, template_name):
    """Load the replay file and return its context."""
    if not isinstance(template_name, basestring):
        # Require the template name only in the form of a string.
        raise TypeError('Template name is required to be of type str')

    replay_file = get_file_name(replay_dir, template_name)

    # Load the context from JSON file
    with open(replay_file, 'r') as infile:
        context = json.load(infile)

    if 'cookiecutter' not in context:
        # Throw an exception if the cookiecutter key is not in the context.
        raise ValueError('Context is required to contain a cookiecutter key')

    return context
