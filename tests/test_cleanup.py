#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cleanup
------------

Tests for `cookiecutter.cleanup` module.
"""

import os
import shutil
import unittest

from cookiecutter import cleanup, exceptions


class TestCleanup(unittest.TestCase):

    def test_remove_repo(self):
        success = cleanup.remove_repo(
            repo_dir='tests/fake-repo',
            generated_project='fake-project'
        )
        self.assertTrue(success)
        self.assertTrue(os.path.isdir('tests/fake-project'))
        self.assertTrue(os.path.isfile('tests/fake-project/README.rst'))
        self.assertFalse(os.path.exists('tests/fake-repo'))

    def test_remove_repo_bad(self):
        self.assertRaises(
            exceptions.MissingProjectDir,
            cleanup.remove_repo,
            repo_dir='tests/fake-repo-bad',
            generated_project='fake-project'
        )

    def tearDown(self):
        if not os.path.exists('tests/fake-repo'):
            os.mkdir('tests/fake-repo')
            shutil.move('tests/fake-project', 'tests/fake-repo/fake-project')

if __name__ == '__main__':
    unittest.main()
