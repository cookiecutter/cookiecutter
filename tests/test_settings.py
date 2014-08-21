#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_settings
-------------

Tests for `cookiecutter.settings` module.
"""

import os
import sys
import tempfile
from contextlib import contextmanager

from cookiecutter import settings
from cookiecutter import exceptions


if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


@contextmanager
def temp(content=None, suffix='.yaml'):
    name = None
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            if content:
                f.write(content.encode('utf-8'))
            name = f.name
        yield name[:-len(suffix)]
    finally:
        if name and os.path.exists(name):
            os.unlink(name)


class TestGetConfig(unittest.TestCase):

    def test_get_settings(self):
        """ Opening and reading settings file """
        template_settings = settings.get_settings(name='tests/test-settings/valid')
        expected_context = {
            'valid': {
                'full_name': 'Firstname Lastname',
                'email': 'firstname.lastname@gmail.com',
                'github_username': 'example'
            }
        }
        self.assertEqual(settings.get_context_from_settings(template_settings), expected_context)

    def test_get_settings_json(self):
        """ Opening and reading old-style JSON settings file """
        template_settings = settings.get_settings('tests/test-settings/valid-json')
        expected_context = {
            'valid-json': {
                'full_name': 'Firstname Lastname',
                'email': 'firstname.lastname@gmail.com',
                'github_username': 'example'
            }
        }
        self.assertEqual(settings.get_context_from_settings(template_settings), expected_context)

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

    def test_version_of_empty_yaml_is_2(self):
        """
        Check that an empty YAML file is reported as version 2
        """
        with temp('') as name:
            template_settings = settings.get_settings(name)
            self.assertEqual(settings.get_version_from_settings(template_settings), 2)

    def test_version_is_read_from_yaml(self):
        """
        Check that an explicit version is read from a YAML file
        """
        with temp('config:\n    version: 3') as name:
            template_settings = settings.get_settings(name)
            self.assertEqual(settings.get_version_from_settings(template_settings), 3)

    def test_json_version_is_1(self):
        """
        Check that a JSON format file is reported as version 1
        """
        with temp('{}', suffix='.json') as name:
            template_settings = settings.get_settings(name)
            self.assertEqual(settings.get_version_from_settings(template_settings), 1)


if __name__ == '__main__':
    unittest.main()

