#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
-----------

Tests for `cookiecutter.config` module.
"""

import os
import shutil

from cookiecutter.compat import unittest
from cookiecutter import config
from cookiecutter.exceptions import ConfigDoesNotExistException, InvalidConfiguration


class TestGetUserConfig(unittest.TestCase):

    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )

        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

    def tearDown(self):
        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)

    def test_get_user_config_invalid(self):
        """ Get config from an invalid ~/.cookiecutterrc file """
        shutil.copy('tests/test-config/invalid-config.yaml', self.user_config_path)
        self.assertRaises(InvalidConfiguration, config.get_user_config)

    def test_get_user_config_nonexistent(self):
        """ Get config from a nonexistent ~/.cookiecutterrc file """
        self.assertEqual(config.get_user_config(), config.DEFAULT_CONFIG)


if __name__ == '__main__':
    unittest.main()
