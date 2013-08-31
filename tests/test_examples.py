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
import sys
import unittest

PY3 = sys.version > '3'
if PY3:
    import subprocess
    from unittest.mock import patch
    input_str = 'builtins.input'
    from io import StringIO
else:
    import subprocess32 as subprocess
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO

#if sys.version_info[:3] < (2, 7, 5):
    #import unittest2 as unittest
    #import subprocess32 as subprocess
#else:
    #import subprocess
    #import unittest

try:
    travis = os.environ[u'TRAVIS']
except KeyError:
    travis = False


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestPyPackage(unittest.TestCase):

    def test_cookiecutter_pypackage(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-pypackage.git works.
        """

        with subprocess.Popen(
            'git clone https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:
            proc.wait()

        with subprocess.Popen(
            'cookiecutter cookiecutter-pypackage/',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:
            proc.wait()

        self.assertTrue(os.path.isfile('cookiecutter-pypackage/boilerplate/README.rst'))

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestJQuery(unittest.TestCase):

    def test_cookiecutter_jquery(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-jquery.git works.
        """

        with subprocess.Popen(
            'git clone https://github.com/audreyr/cookiecutter-jquery.git',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:
            proc.wait()

        with subprocess.Popen(
            'cookiecutter cookiecutter-jquery/',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:
            proc.wait()

        self.assertTrue(os.path.isfile('cookiecutter-jquery/boilerplate/README.md'))

    def tearDown(self):
        if os.path.isdir('cookiecutter-jquery'):
            shutil.rmtree('cookiecutter-jquery')

@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestExamplesRepoArg(unittest.TestCase):

    def test_cookiecutter_pypackage_git(self):
        with subprocess.Popen(
            'cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:

            # Just skip all the prompts
            proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')

        self.assertTrue(os.path.isfile('boilerplate/README.rst'))

    def tearDown(self):
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestGitBranch(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

    def test_branch(self):
        with subprocess.Popen(
            'cookiecutter -c console-script https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:

            # Just skip all the prompts
            proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')

        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.isfile('boilerplate/boilerplate/main.py'))

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')


if __name__ == '__main__':
    unittest.main()
