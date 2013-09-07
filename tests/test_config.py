#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
-----------

Tests for `cookiecutter.config` module.
"""

import os
import sys
import unittest

import yaml

from cookiecutter import config
from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestConfig(unittest.TestCase):

    def test_get_config(self):
        """ Opening and reading config file """
        conf = config.get_config('tests/test-config/test-config.yaml')
        expected_conf = {
        	'template_dirs': [
        		'/home/raphi/dev'
        	],
        	'default_context': {
        		"full_name": "Raphi Gaziano",
        		"email": "r.gaziano@gmail.com",
        		"github_username": "raphigaziano"
        	}
        }
        self.assertEqual(conf, expected_conf)

    def test_get_config_does_not_exist(self):
        """
        Check that `exceptions.ConfigDoesNotExistException` is raised when
        attempting to get a non-existent config file.
        """
        self.assertRaises(
            ConfigDoesNotExistException,
            config.get_config,
            'tests/test-config/this-does-not-exist.yaml'
        )

    def test_invalid_config(self):
        """
        An invalid config file should raise an `InvalidConfiguration` exception.
        """
        self.assertRaises(InvalidConfiguration, config.get_config,
                          "tests/test-config/invalid-config.yaml")


if __name__ == '__main__':
    unittest.main()
