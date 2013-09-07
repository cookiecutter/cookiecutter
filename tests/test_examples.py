#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_examples
--------------

Tests for the Cookiecutter example repos.
"""

from __future__ import unicode_literals
import errno
import os
import shutil
import sys

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

if sys.version_info[:3] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

try:
    travis = os.environ[u'TRAVIS']
except KeyError:
    travis = False

from cookiecutter import config, utils


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestPyPackage(unittest.TestCase):

    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)

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
            'cookiecutter --no-input cookiecutter-pypackage/',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:
            proc.wait()

        self.assertTrue(os.path.isdir('cookiecutter-pypackage'))
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestJQuery(unittest.TestCase):

    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

    def tearDown(self):
        if os.path.isdir('cookiecutter-jquery'):
            shutil.rmtree('cookiecutter-jquery')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)


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
            'cookiecutter --no-input cookiecutter-jquery/',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:
            proc.wait()

        self.assertTrue(os.path.isdir('cookiecutter-jquery'))
        self.assertTrue(os.path.isfile('boilerplate/README.md'))


@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestExamplesRepoArg(unittest.TestCase):

    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

    def tearDown(self):
        with utils.work_in(config.DEFAULT_CONFIG['cookiecutters_dir']):
            if os.path.isdir('cookiecutter-pypackage'):
                shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)

    def test_cookiecutter_pypackage_git(self):
        with subprocess.Popen(
            'cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git',
            stdin=subprocess.PIPE,
            shell=True
        ) as proc:

            # Just skip all the prompts
            proc.communicate(input=b'\n\n\n\n\n\n\n\n\n\n\n\n')
        
        self.assertTrue(os.path.isfile('boilerplate/README.rst'))



@unittest.skipIf(condition=travis, reason='Works locally with tox but fails on Travis.')
class TestGitBranch(unittest.TestCase):

    def setUp(self):
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

    def tearDown(self):
        with utils.work_in(config.DEFAULT_CONFIG['cookiecutters_dir']):
            if os.path.isdir('cookiecutter-pypackage'):
                shutil.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            shutil.rmtree('boilerplate')

        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)

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


if __name__ == '__main__':
    unittest.main()
