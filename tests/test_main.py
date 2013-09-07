#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_main
---------

Tests for `cookiecutter.main` module.
"""

import logging
import os
import shutil
import sys
import unittest

from cookiecutter import config, main

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


class TestCookiecutterLocalNoInput(unittest.TestCase):

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

    def tearDown(self):
        if os.path.isdir('fake-project'):
            shutil.rmtree('fake-project')


class TestCookiecutterLocalWithInput(unittest.TestCase):

    @patch(input_str, lambda x: '\n')
    def test_cookiecutter_local_with_input(self):
        if not PY3:
            sys.stdin = StringIO("\n\n\n\n\n\n\n\n\n\n\n\n")

        main.cookiecutter('tests/fake-repo-pre/', no_input=False)
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertFalse(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isdir('fake-project'))
        self.assertTrue(os.path.isfile('fake-project/README.rst'))
        self.assertFalse(os.path.exists('fake-project/json/'))

    def tearDown(self):
        if os.path.isdir('fake-project'):
            shutil.rmtree('fake-project')


class TestArgParsing(unittest.TestCase):

    def test_parse_cookiecutter_args(self):
        args = main.parse_cookiecutter_args(['project/'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, None)

    def test_parse_cookiecutter_args_with_branch(self):
        args = main.parse_cookiecutter_args(['project/', '--checkout', 'develop'])
        self.assertEqual(args.input_dir, 'project/')
        self.assertEqual(args.checkout, 'develop')


class TestCookiecutterRepoArg(unittest.TestCase):
    def setUp(self):
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

        # If the default cookiecutters_dir is pre-existing, move it to a
        # temp location
        self.cookiecutters_dir = config.DEFAULT_CONFIG['cookiecutters_dir']
        self.cookiecutters_dir_backup = os.path.expanduser('~/.cookiecutters.backup')
        if os.path.isdir(self.cookiecutters_dir):
            shutil.copytree(self.cookiecutters_dir, self.cookiecutters_dir_backup)
        if os.path.isdir(self.cookiecutters_dir_backup):
            shutil.rmtree(self.cookiecutters_dir)

    def tearDown(self):
        # Delete the created ~/.cookiecutters dir as long as a backup exists
        if os.path.isdir(self.cookiecutters_dir) and os.path.isdir(self.cookiecutters_dir_backup):
            shutil.rmtree(self.cookiecutters_dir)
    
        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)
        
        # Restore the user's default cookiecutters_dir contents
        if os.path.isdir(self.cookiecutters_dir_backup):
            shutil.copytree(self.cookiecutters_dir_backup, self.cookiecutters_dir)
        if os.path.isdir(self.cookiecutters_dir):
            shutil.rmtree(self.cookiecutters_dir_backup)

        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

    @patch(input_str, lambda x: '')
    def test_cookiecutter_git(self):
        if not PY3:
            sys.stdin = StringIO('\n\n\n\n\n\n\n\n\n')
        main.cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        clone_dir = os.path.join(
            config.DEFAULT_CONFIG['cookiecutters_dir'],
            'cookiecutter-pypackage'
        )
        self.assertTrue(os.path.exists(clone_dir))
        self.assertTrue(os.path.isdir('boilerplate'))
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.exists('boilerplate/setup.py'))


if __name__ == '__main__':
    unittest.main()
