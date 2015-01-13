#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter
------------

Main package for Cookiecutter.
"""
from .compat import OLD_PY2

__version__ = '0.9.0'

if OLD_PY2:
    msg = 'Python 2.6 support was removed from cookiecutter in release 1.0.0.'
    raise DeprecationWarning(msg)
