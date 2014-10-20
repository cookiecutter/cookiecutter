#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_main
---------

Tests for `cookiecutter.main` module.
"""

import logging
import os
import sys

from cookiecutter.main import cookiecutter, main, parse_cookiecutter_args
from cookiecutter import utils
from tests import CookiecutterCleanSystemTestCase

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    from io import StringIO
else:
    from mock import patch
    from cStringIO import StringIO

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False

# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestCookiecutterMain(unittest.TestCase):

    def test_main_help(self):
        """ Test `cookiecutter` command line help. """
        expected = 'Create a project from a Cookiecutter project template.'
        with patch('sys.argv', ['cookiecutter', '-h']):
            with patch('sys.stdout', new_callable=StringIO) as out:
                try:
                    main()
                except SystemExit:
                    self.assertTrue(expected in out.getvalue())

    def test_main_with_options(self):
        """ Test `cookiecutter` cli with options. """
        expected = 'config_path is'
        argv = 'cookiecutter -v --no-input tests/fake-repo-pre/'.split(' ')
        with patch('sys.argv', argv):
            with patch('sys.stdout', new_callable=StringIO) as out:
                main()
                self.assertTrue(expected in out.getvalue())


class TestCookiecutterLocalNoInput(CookiecutterCleanSystemTestCase):

    def test_cookiecutter(self):
        """ Call `cookiecutter()` with `no_input=True`. """
        cookiecutter('tests/fake-repo-pre/', no_input=True)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    # FIXME: this test looks exactly the same as :points_up:?
    def test_cookiecutter_no_slash(self):
        cookiecutter('tests/fake-repo-pre', no_input=True)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def test_cookiecutter_no_input_extra_context(self):
        """ Call `cookiecutter()` with `no_input=True` and `extra_context` """
        cookiecutter(
            'tests/fake-repo-pre',
            no_input=True,
            extra_context={'repo_name': 'fake-project-extra'}
        )
        self.assertTrue(os.path.isdir('fake-project-extra'))

    def test_cookiecutter_no_input_checkout(self):
        """ Call `cookiecutter()` with `no_input=True` and `checkout` """
        cookiecutter(
            'tests/fake-repo-pre',
            no_input=True,
            checkout='test',
        )

    def tearDown(self):
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-extra'):
            utils.rmtree('fake-project-extra')


class TestCookiecutterLocalWithInput(CookiecutterCleanSystemTestCase):

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_cookiecutter_local_with_input(self):
        cookiecutter('tests/fake-repo-pre/', no_input=False)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'\n')
    def test_cookiecutter_input_extra_context(self):
        """ `Call cookiecutter()` with `no_input=False` and `extra_context` """
        cookiecutter(
            'tests/fake-repo-pre',
            no_input=False,
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
        args = parse_cookiecutter_args(['project/'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, None)

    def test_parse_cookiecutter_args_with_branch(self):
        args = parse_cookiecutter_args(['project/', '--checkout', 'develop'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, 'develop')


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
    def test_cookiecutter_git(self):
        cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        clone_dir = os.path.join(os.path.expanduser('~/.cookiecutters'), 'cookiecutter-pypackage')
        self.assertTrue(os.path.exists(clone_dir))
        self.assertTrue(os.path.isdir('boilerplate'))
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.exists('boilerplate/setup.py'))

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'')
    def test_cookiecutter_mercurial(self):
        cookiecutter('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        clone_dir = os.path.join(os.path.expanduser('~/.cookiecutters'), 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.exists(clone_dir))
        self.assertTrue(os.path.isdir('module_name'))
        self.assertTrue(os.path.isfile('module_name/README'))
        self.assertTrue(os.path.exists('module_name/setup.py'))


if __name__ == '__main__':
    unittest.main()
