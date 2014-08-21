#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_settings
-------------

Tests for `cookiecutter.settings` module.
"""

import sys

from cookiecutter import settings
from cookiecutter import exceptions

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class TestGetConfig(unittest.TestCase):

    def test_get_settings(self):
        """ Opening and reading settings file """
        stg = settings.get_settings('tests/test-settings/valid')
        expected_context = {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example'
        }
        self.assertTrue('config' in stg)
        self.assertTrue('context' in stg)
        self.assertEqual(stg['config'].get('version'), 2)
        self.assertEqual(stg['context'].get('valid'), expected_context)

    def test_get_settings_json(self):
        """ Opening and reading old-style JSON settings file """
        stg = settings.get_settings('tests/test-settings/valid-json')
        expected_context = {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example'
        }
        self.assertTrue('config' in stg)
        self.assertTrue('context' in stg)
        self.assertEqual(stg['config'].get('version'), 1)
        self.assertEqual(stg['context'].get('valid-json'), expected_context)

    def test_get_settings_does_not_exist(self):
        """
        Check that a missing settings file results in an exception.
        """
        self.assertRaises(
            exceptions.MissingTemplateSettingsException,
            settings.get_settings,
            'tests/test-settings/does-not-exist'
        )

    def test_get_settings_both_formats_exist(self):
        """
        Check that you cannot have both settings formats present.
        """
        self.assertRaises(
            exceptions.MultipleTemplateSettingsException,
            settings.get_settings,
            'tests/test-settings/both'
        )


if __name__ == '__main__':
    unittest.main()

