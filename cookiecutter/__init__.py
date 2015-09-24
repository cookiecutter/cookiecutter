#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter
------------

Main package for Cookiecutter.
"""
import sys

__version__ = '1.0.0'

if sys.version_info[:2] < (2, 7):
    msg = 'Python 2.6 support was removed from cookiecutter in release 1.0.0.'
    raise DeprecationWarning(msg)
