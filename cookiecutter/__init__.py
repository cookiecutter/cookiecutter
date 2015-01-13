#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter
------------

Main package for Cookiecutter.
"""
import warnings

from .compat import OLD_PY2


__version__ = '0.9.0'

if OLD_PY2:
    warnings.warn(
        'Python 2.6 support has been removed as of 1.0.0',
        DeprecationWarning
    )
