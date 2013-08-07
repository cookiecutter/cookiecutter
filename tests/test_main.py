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
import unittest

from cookiecutter import main


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

class TestCookiecutterRepoArg(unittest.TestCase):

    def test_cookiecutter_git(self):
        main.cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
        logging.debug('Current dir is {0}'.format(os.getcwd()))
        self.assertFalse(os.path.exists('cookiecutter-pypackage'))
        self.assertTrue(os.path.isdir('alotofeffort'))
        self.assertTrue(os.path.isfile('alotofeffort/README.rst'))
        self.assertTrue(os.path.exists('alotofeffort/setup.py'))
    
    def tearDown(self):
        if os.path.isdir('alotofeffort'):
            shutil.rmtree('alotofeffort')

if __name__ == '__main__':
    unittest.main()
