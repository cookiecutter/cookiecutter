#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import locale
import logging
import os
import shutil
import subprocess
import sys
import unittest

PY3 = sys.version > '3'
if PY3:
    import subprocess
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    import subprocess32 as subprocess
    import __builtin__
    from mock import patch
    input_str = '__builtin__.raw_input'
    from cStringIO import StringIO

from cookiecutter import vcs


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
encoding = locale.getdefaultlocale()[1]


class TestVCS(unittest.TestCase):

    def test_git_clone(self):
        repo_dir = vcs.git_clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

    def test_git_clone_checkout(self):
        repo_dir = vcs.git_clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git',
            'console-script'
        )
        git_dir = 'cookiecutter-pypackage'
        self.assertEqual(repo_dir, git_dir)
        self.assertTrue(os.path.isfile(os.path.join('cookiecutter-pypackage', 'README.rst')))

        with subprocess.Popen(
            ['git', 'symbolic-ref', 'HEAD'],
            cwd=git_dir,
            stdout=subprocess.PIPE
        ) as proc:
            symbolic_ref = proc.communicate()[0]
            branch = symbolic_ref.decode(encoding).strip().split('/')[-1]
            self.assertEqual('console-script', branch)

        if os.path.isdir(git_dir):
            shutil.rmtree(git_dir)


class TestVCSPrompt(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')
        os.mkdir('cookiecutter-pypackage/')

    @patch(input_str, lambda: 'y')
    def test_git_clone_overwrite(self):
        if not PY3:
            sys.stdin = StringIO('y\n\n')
        repo_dir = vcs.git_clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))

    @patch(input_str, lambda: 'n')
    def test_git_clone_cancel(self):
        if not PY3:
            sys.stdin = StringIO('n\n\n')
        self.assertRaises(
            SystemExit,
            vcs.git_clone,
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')


if __name__ == '__main__':
    unittest.main()
