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


class TestFindTemplate(unittest.TestCase):
    
    def test_find_template(self):
        template = find.find_template(repo_dir='tests/fake-repo-pre')
        self.assertEqual(template, 'tests/fake-repo-pre/{{cookiecutter.repo_name}}')
        self.assertNotEqual(template, 'tests/fake-repo-pre/{{cookiecutter.repo_name }}')
        self.assertNotEqual(template, 'tests/fake-repo-pre/{{ cookiecutter.repo_name }}')

class TestFindTemplate2(unittest.TestCase):
    
    def test_find_template(self):
        template = find.find_template(repo_dir='tests/fake-repo-pre2')
        self.assertEqual(template, 'tests/fake-repo-pre2/{{cookiecutter.repo_name}}')
        self.assertNotEqual(template, 'tests/fake-repo-pre2/{{cookiecutter.repo_name }}')
        self.assertNotEqual(template, 'tests/fake-repo-pre2/{{ cookiecutter.repo_name }}')


if __name__ == '__main__':
    unittest.main()
