#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_find
------------

Tests for `cookiecutter.find` module.
"""

import os
import shutil
import unittest

from cookiecutter import find


class TestFind(unittest.TestCase):

    def test_find_template(self):
        os.system('git clone https://github.com/audreyr/cookiecutter-pypackage.git')
        template = find.find_template(repo_dir='cookiecutter-pypackage')
        self.assertEqual(template, 'cookiecutter-pypackage/{{cookiecutter.repo_name}}')
        self.assertNotEqual(template, 'cookiecutter-pypackage/{{cookiecutter.repo_name }}')
        self.assertNotEqual(template, 'cookiecutter-pypackage/{{ cookiecutter.repo_name }}')

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

class TestFind2(unittest.TestCase):

    def test_find_template2(self):
        os.system('git clone https://github.com/audreyr/cookiecutter-jquery.git')
        template = find.find_template(repo_dir='cookiecutter-jquery')
        self.assertEqual(template, 'cookiecutter-jquery/{{cookiecutter.repo_name}}')
        self.assertNotEqual(template, 'cookiecutter-jquery/{{cookiecutter.repo_name }}')
        self.assertNotEqual(template, 'cookiecutter-jquery/{{ cookiecutter.repo_name }}')

    def tearDown(self):
        if os.path.isdir('cookiecutter-jquery'):
            shutil.rmtree('cookiecutter-jquery')


if __name__ == '__main__':
    unittest.main()
