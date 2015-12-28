#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
utils
--------

Contains test utilities.
"""

import os


def dir_tests(*paths):
    dirname = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(dirname, *paths))
