#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_compat
------------

Tests for `cookiecutter.compat` module.
"""

import os

from cookiecutter.compat import which


def test_existing_command():
    cmd = which('date')
    assert cmd
    assert os.path.exists(cmd)
    assert os.access(cmd, os.F_OK | os.X_OK)
    assert not os.path.isdir(cmd)


def test_non_existing_command():
    assert which('stringthatisntashellcommand') is None
