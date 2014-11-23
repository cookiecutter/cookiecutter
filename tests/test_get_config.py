#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_config
---------------

Tests formerly known from a unittest residing in test_config.py named
TestGetConfig.test_get_config
"""

from cookiecutter import config


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
