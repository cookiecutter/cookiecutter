#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_examples
--------------

Tests for the Cookiecutter example repos.
"""

import os
import shutil
import unittest


class TestExamples(unittest.TestCase):

    def test_cookiecutter_pypackage(self):
        """
        Tests that https://github.com/audreyr/cookiecutter-pypackage.git works.
        """

        os.system('git clone https://github.com/audreyr/cookiecutter-pypackage.git')
        os.chdir('cookiecutter-pypackage')
        os.system('cookiecutter {{project.repo_name}}')
        self.assertTrue(os.path.isfile('alotofeffort/README.rst'))
        os.chdir(os.pardir)

    def test_cookiecutter_pypackage_git(self):
        os.system('cookiecutter https://github.com/audreyr/cookiecutter-pypackage.git')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/alotofeffort/README.rst'))

    def tearDown(self):
        shutil.rmtree('cookiecutter-pypackage')
        
if __name__ == '__main__':
    unittest.main()
