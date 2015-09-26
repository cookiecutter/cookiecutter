# -*- coding: utf-8 -*-

"""
cookiecutter.replay
-------------------
"""

from __future__ import unicode_literals

import json
import os
from past.builtins import basestring

from .config import get_user_config
from .utils import make_sure_path_exists


def get_file_name(replay_dir, template_name):
    file_name = '{}.json'.format(template_name)
    return os.path.join(replay_dir, file_name)


def dump(template_name, context):
    if not isinstance(template_name, basestring):
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        raise TypeError('Context is required to be of type dict')

    if 'cookiecutter' not in context:
        raise ValueError('Context is required to contain a cookiecutter key')

    replay_dir = get_user_config()['replay_dir']

    if not make_sure_path_exists(replay_dir):
        raise IOError('Unable to create replay dir at {}'.format(replay_dir))

    replay_file = get_file_name(replay_dir, template_name)

    with open(replay_file, 'w') as outfile:
        json.dump(context, outfile)


def load(template_name):
    if not isinstance(template_name, basestring):
        raise TypeError('Template name is required to be of type str')

    replay_dir = get_user_config()['replay_dir']
    replay_file = get_file_name(replay_dir, template_name)

    with open(replay_file, 'r') as infile:
        context = json.load(infile)

    if 'cookiecutter' not in context:
        raise ValueError('Context is required to contain a cookiecutter key')

    return context
