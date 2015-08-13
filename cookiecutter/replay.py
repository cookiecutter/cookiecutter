# -*- coding: utf-8 -*-

"""
cookiecutter.replay
-------------------
"""

from __future__ import unicode_literals

from .compat import is_string
from .config import get_user_config
from .utils import make_sure_path_exists


def dump(template_name, context):
    if not is_string(template_name):
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        raise TypeError('Context is required to be of type dict')

    replay_dir = get_user_config()['replay_dir']

    if not make_sure_path_exists(replay_dir):
        raise IOError('Unable to create replay dir at {}'.format(replay_dir))
