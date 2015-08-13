# -*- coding: utf-8 -*-

"""
cookiecutter.replay
-------------------
"""

from __future__ import unicode_literals

from .compat import is_string


def dump(template_name, context):
    if not is_string(template_name):
        raise TypeError('Template name is required to be of type str')

    if not isinstance(context, dict):
        raise TypeError('Context is required to be of type dict')
