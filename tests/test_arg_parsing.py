#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_arg_parsing
----------------

Tests formerly known from a unittest residing in test_main.py named
TestArgParsing.test_parse_cookiecutter_args
TestArgParsing.test_parse_cookiecutter_args_with_branch
"""

from __future__ import unicode_literals

from cookiecutter import main


def test_parse_cookiecutter_args():
    args = main.parse_cookiecutter_args(['project/'])
    assert args.input_dir == 'project/'
    assert args.checkout is None


def test_parse_cookiecutter_args_with_branch():
    args = main.parse_cookiecutter_args(['project/', '--checkout', 'develop'])
    assert args.input_dir == 'project/'
    assert args.checkout == 'develop'
