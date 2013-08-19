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

from cookiecutter import main

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


class TestCookiecutter(unittest.TestCase):

    def test_cookiecutter(self):
        main.cookiecutter('tests/fake-repo-pre/')
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isfile('tests/fake-repo-pre/fake-project/README.rst'))
        self.assertFalse(os.path.exists('tests/fake-repo-pre/fake-project/json/'))

    def test_cookiecutter_no_slash(self):
        main.cookiecutter('tests/fake-repo-pre')
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}'))
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isfile('tests/fake-repo-pre/fake-project/README.rst'))
        self.assertFalse(os.path.exists('tests/fake-repo-pre/fake-project/json/'))
        
    def tearDown(self):
        if os.path.isdir('tests/fake-repo-pre/fake-project'):
            shutil.rmtree('tests/fake-repo-pre/fake-project')


class TestArgParsing(unittest.TestCase):
    
    def test_parse_cookiecutter_args(self):
        args = main.parse_cookiecutter_args(['project/'])
        self.assertEqual(args.input_dir, 'project/')


class TestCookiecutterRepoArg(unittest.TestCase):

    @patch(input_str, lambda x: '')
    def test_cookiecutter_git(self):
        if not PY3:
            sys.stdin = StringIO('\n\n\n\n\n\n\n\n\n')
        main.cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        self.assertFalse(os.path.exists('cookiecutter-pypackage'))
        self.assertTrue(os.path.isdir('boilerplate'))
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.exists('boilerplate/setup.py'))
    
    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

if __name__ == '__main__':
    unittest.main()
