#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_compat
------------

Tests for `cookiecutter.compat` module.
"""

from cookiecutter.compat import which


def test_existing_command():
    assert which('cookiecutter')


def test_non_existing_command():
    assert not which('stringthatisntashellcommand')
