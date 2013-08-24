#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_examples
--------------

Tests for the Cookiecutter example repos.
"""

import errno
import os
import shutil
import subprocess
import sys

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
    from io import StringIO
else:
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO

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

class TestGitBranch(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

    def test_branch(self):
        p = subprocess.Popen(
            'cookiecutter -c console-script https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        )

        # Just skip all the prompts
        p.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')

        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.isfile('boilerplate/boilerplate/main.py'))

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')


if __name__ == '__main__':
    unittest.main()
