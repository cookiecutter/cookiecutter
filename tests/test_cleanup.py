#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cleanup
------------

Tests for `cookiecutter.cleanup` module.
"""

from __future__ import unicode_literals
import os
import shutil
import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
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


class TestCleanupUnicode(unittest.TestCase):

    def test_remove_repo_unicode(self):
        if os.path.supports_unicode_filenames:
            success = cleanup.remove_repo(
                repo_dir='tests/fake-repööö',
                generated_project='fake-pröööject'
            )
            self.assertTrue(success)
            self.assertTrue(os.path.isdir('tests/fake-pröööject'))
            self.assertTrue(os.path.isfile('tests/fake-pröööject/README.rst'))
            self.assertFalse(os.path.exists('tests/fake-repööö'))

    def tearDown(self):
        if os.path.supports_unicode_filenames:
            if not os.path.exists('tests/fake-repööö'):
                os.mkdir('tests/fake-repööö')
                shutil.move('tests/fake-pröööject', 'tests/fake-repööö/fake-pröööject')


if __name__ == '__main__':
    unittest.main()
