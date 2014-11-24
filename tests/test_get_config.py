#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_config
---------------

Tests formerly known from a unittest residing in test_config.py named
TestGetConfig.test_get_config
TestGetConfig.test_get_config_does_not_exist
"""

import pytest

from cookiecutter import config
from cookiecutter.exceptions import ConfigDoesNotExistException


def test_get_config():
    """Opening and reading config file
    """
    conf = config.get_config('tests/test-config/valid-config.yaml')
    expected_conf = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'default_context': {
            "full_name": "Firstname Lastname",
            "email": "firstname.lastname@gmail.com",
            "github_username": "example"
        }
    }
    assert conf == expected_conf


def test_get_config_does_not_exist():
    """
    Check that `exceptions.ConfigDoesNotExistException` is raised when
    attempting to get a non-existent config file.
    """
    with pytest.raises(ConfigDoesNotExistException):
        config.get_config('tests/test-config/this-does-not-exist.yaml')
