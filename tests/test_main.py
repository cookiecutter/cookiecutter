#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_main
---------

Tests for `cookiecutter.main` module.
"""

import logging
import os

from cookiecutter.compat import patch, unittest
from cookiecutter import main, utils
from tests import CookiecutterCleanSystemTestCase

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False

# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestCookiecutterLocalNoInput(CookiecutterCleanSystemTestCase):

    def test_cookiecutter(self):
        main.cookiecutter('tests/fake-repo-pre/', no_input=True)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def test_cookiecutter_no_slash(self):
        main.cookiecutter('tests/fake-repo-pre', no_input=True)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def test_cookiecutter_no_input_extra_context(self):
        """ `Call cookiecutter()` with `no_input=True` and `extra_context` """
        main.cookiecutter(
            'tests/fake-repo-pre',
            no_input=True,
            extra_context={'repo_name': 'fake-project-extra'}
        )
        self.assertTrue(os.path.isdir('fake-project-extra'))

    def test_cookiecutter_templated_context(self):
        """
        `Call cookiecutter()` with `no_input=True` and templates in the
        cookiecutter.json file
        """
        main.cookiecutter(
            'tests/fake-repo-tmpl',
            no_input=True
        )
        self.assertTrue(os.path.isdir('fake-project-templated'))

    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-extra'):
            utils.rmtree('fake-project-extra')
        if os.path.isdir('fake-project-templated'):
            utils.rmtree('fake-project-templated')


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


class TestArgParsing(unittest.TestCase):

    def test_parse_cookiecutter_args(self):
        args = main.parse_cookiecutter_args(['project/'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, None)

    def test_parse_cookiecutter_args_with_branch(self):
        args = main.parse_cookiecutter_args(['project/', '--checkout', 'develop'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, 'develop')


class TestAbbreviationExpansion(unittest.TestCase):

    def test_abbreviation_expansion(self):
        input_dir = main.expand_abbreviations('foo', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(input_dir, 'bar')

    def test_abbreviation_expansion_not_an_abbreviation(self):
        input_dir = main.expand_abbreviations('baz', {'abbreviations': {'foo': 'bar'}})
        self.assertEqual(input_dir, 'baz')

    def test_abbreviation_expansion_prefix(self):
        input_dir = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<{0}>'}})
        self.assertEqual(input_dir, '<a>')

    def test_abbreviation_expansion_builtin(self):
        input_dir = main.expand_abbreviations('gh:a', {})
        self.assertEqual(input_dir, 'https://github.com/a.git')

    def test_abbreviation_expansion_override_builtin(self):
        input_dir = main.expand_abbreviations('gh:a', {'abbreviations': {'gh': '<{0}>'}})
        self.assertEqual(input_dir, '<a>')

    def test_abbreviation_expansion_prefix_ignores_suffix(self):
        input_dir = main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '<>'}})
        self.assertEqual(input_dir, '<>')

    def test_abbreviation_expansion_prefix_not_0_in_braces(self):
        self.assertRaises(
            IndexError,
            main.expand_abbreviations,
            'xx:a',
            {'abbreviations': {'xx': '{1}'}}
        )


@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub/Bitbucket.')
class TestCookiecutterRepoArg(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')
        if os.path.isdir('module_name'):
            utils.rmtree('module_name')
        super(TestCookiecutterRepoArg, self).tearDown()

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'')
    def test_cookiecutter_mercurial(self):
        main.cookiecutter('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        clone_dir = os.path.join(os.path.expanduser('~/.cookiecutters'), 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.exists(clone_dir))
        self.assertTrue(os.path.isdir('module_name'))
        self.assertTrue(os.path.isfile('module_name/README'))
        self.assertTrue(os.path.exists('module_name/setup.py'))


if __name__ == '__main__':
    unittest.main()
