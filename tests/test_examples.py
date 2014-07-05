#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_examples
--------------

Tests for the Cookiecutter example repos.
"""

from __future__ import unicode_literals
import errno
import logging
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

if sys.version_info[:3] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

try:
    travis = os.environ[u'TRAVIS']
except KeyError:
    travis = False

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False

from cookiecutter import config, utils
from tests import force_delete, CookiecutterCleanSystemTestCase


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub.')
class TestPyPackage(CookiecutterCleanSystemTestCase):


    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage', onerror=force_delete)
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate', onerror=force_delete)
        super(TestPyPackage, self).tearDown()

    def test_cookiecutter_pypackage(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-pypackage.git works.
        """

        proc = subprocess.Popen(
            'git clone https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        )
        proc.wait()

        proc = subprocess.Popen(
            'cookiecutter --no-input cookiecutter-pypackage/',
            stdin=subprocess.PIPE,
            shell=True
        )
        proc.wait()

        self.assertTrue(os.path.isdir('cookiecutter-pypackage'))
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub.')
class TestJQuery(CookiecutterCleanSystemTestCase):


    def tearDown(self):
        if os.path.isdir('cookiecutter-jquery'):
            shutil.rmtree('cookiecutter-jquery', onerror=force_delete)
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate', onerror=force_delete)
        super(TestJQuery, self).tearDown()

    def test_cookiecutter_jquery(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-jquery.git works.
        """

        proc = subprocess.Popen(
            'git clone https://github.com/audreyr/cookiecutter-jquery.git',
            stdin=subprocess.PIPE,
            shell=True
        )
        proc.wait()

        proc = subprocess.Popen(
            'cookiecutter --no-input cookiecutter-jquery/',
            stdin=subprocess.PIPE,
            shell=True
        )
        proc.wait()

        self.assertTrue(os.path.isdir('cookiecutter-jquery'))
        self.assertTrue(os.path.isfile('boilerplate/README.md'))


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub.')
class TestExamplesRepoArg(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        with utils.work_in(config.DEFAULT_CONFIG['cookiecutters_dir']):
            if os.path.isdir('cookiecutter-pypackage'):
                shutil.rmtree('cookiecutter-pypackage', onerror=force_delete)
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate', onerror=force_delete)
        super(TestExamplesRepoArg, self).tearDown()

    def test_cookiecutter_pypackage_git(self):
        proc = subprocess.Popen(
            'cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        )

        # Just skip all the prompts
        proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')
        
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))



@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub.')
class TestGitBranch(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        with utils.work_in(config.DEFAULT_CONFIG['cookiecutters_dir']):
            if os.path.isdir('cookiecutter-pypackage'):
                shutil.rmtree('cookiecutter-pypackage', onerror=force_delete)
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate', onerror=force_delete)
        super(TestGitBranch, self).tearDown()

    def test_branch(self):
        proc = subprocess.Popen(
            'cookiecutter -c console-script https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        )

        # Just skip all the prompts
        proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')

        self.assertTrue(os.path.isfile('boilerplate/README.rst'))
        self.assertTrue(os.path.isfile('boilerplate/boilerplate/main.py'))


if __name__ == '__main__':
    unittest.main()
