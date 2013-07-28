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


# Log info and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


class TestCookiecutter(unittest.TestCase):

    def test_cookiecutter(self):
        main.cookiecutter('tests/fake-repo-pre/{{project.repo_name}}')
        self.assertTrue(os.path.isdir('tests/fake-repo-pre/fake-project'))
        self.assertTrue(os.path.isfile('tests/fake-repo-pre/fake-project/README.rst'))
        self.assertFalse(os.path.exists('tests/fake-repo-pre/fake-project/json/'))
    
    def tearDown(self):
        if os.path.isdir('tests/fake-repo-pre/fake-project'):
            shutil.rmtree('tests/fake-repo-pre/fake-project')

if __name__ == '__main__':
    unittest.main()
