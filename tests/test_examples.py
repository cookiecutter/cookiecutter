#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_examples
--------------

Tests for the Cookiecutter example repos.
"""

import os
import shutil
import sys
import unittest

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


@unittest.skip(reason='Works locally with tox but fails on Travis.')
class TestPyPackage(unittest.TestCase):

    def test_cookiecutter_pypackage(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-pypackage.git works.
        """

        os.system('git clone https://github.com/audreyr/cookiecutter-pypackage.git')
        os.system('cookiecutter cookiecutter-pypackage/')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/alotofeffort/README.rst'))

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

@unittest.skip(reason='Works locally with tox but fails on Travis.')
class TestJQuery(unittest.TestCase):

    def test_cookiecutter_jquery(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-jquery.git works.
        """

        os.system('git clone https://github.com/audreyr/cookiecutter-jquery.git')
        os.system('cookiecutter cookiecutter-jquery/')
        self.assertTrue(os.path.isfile('cookiecutter-jquery/boilerplate/README.md'))

    def tearDown(self):
        if os.path.isdir('cookiecutter-jquery'):
            shutil.rmtree('cookiecutter-jquery')

@unittest.skip(reason='Works locally with tox but fails on Travis.')
class TestExamplesRepoArg(unittest.TestCase):
    
    def test_cookiecutter_pypackage_git(self):
        os.system('cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git')
        self.assertTrue(os.path.isfile('alotofeffort/README.rst'))

    def tearDown(self):
        if os.path.isdir('alotofeffort'):
            shutil.rmtree('alotofeffort')

        
if __name__ == '__main__':
    unittest.main()
