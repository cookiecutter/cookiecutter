#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_main
---------

Tests for `cookiecutter.main` module.
"""

import logging
import os
import unittest

from cookiecutter.compat import patch
from cookiecutter import main, utils
from tests import CookiecutterCleanSystemTestCase

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False

# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestCookiecutterLocalWithInput(CookiecutterCleanSystemTestCase):

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_cookiecutter_local_with_input(self):
        main.cookiecutter('tests/fake-repo-pre/', no_input=False)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_cookiecutter_input_extra_context(self):
        """ `Call cookiecutter()` with `no_input=False` and `extra_context` """
        main.cookiecutter(
            'tests/fake-repo-pre',
            no_input=True,
            extra_context={'repo_name': 'fake-project-input-extra'}
        )
        self.assertTrue(os.path.isdir('fake-project-input-extra'))

    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-input-extra'):
            utils.rmtree('fake-project-input-extra')


class TestAbbreviationExpansion(unittest.TestCase):

    def test_abbreviation_expansion(self):
        template = main.expand_abbreviations('foo', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(template, 'bar')

    def test_abbreviation_expansion_not_an_abbreviation(self):
        template = main.expand_abbreviations('baz', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(template, 'baz')

    def test_abbreviation_expansion_prefix(self):
        template = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<{0}>'}})
        self.assertEqual(template, '<a>')

    def test_abbreviation_expansion_builtin(self):
        template = main.expand_abbreviations('gh:a', {})
        self.assertEqual(template, 'https://github.com/a.git')

    def test_abbreviation_expansion_override_builtin(self):
        template = main.expand_abbreviations('gh:a', {'abbreviations': {'gh': '<{0}>'}})
        self.assertEqual(template, '<a>')

    def test_abbreviation_expansion_prefix_ignores_suffix(self):
        template = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<>'}})
        self.assertEqual(template, '<>')

    def test_abbreviation_expansion_prefix_not_0_in_braces(self):
        self.assertRaises(
            IndexError,
            main.expand_abbreviations,
            'xx:a',
            {'abbreviations': {'xx': '{1}'}}
        )


if __name__ == '__main__':
    unittest.main()
