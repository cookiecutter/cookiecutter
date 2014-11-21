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


def test_find_template():
    repo_dir = os.path.join('tests', 'fake-repo-pre')
    template = find.find_template(repo_dir=repo_dir)

    test_dir = os.path.join(repo_dir, '{{cookiecutter.repo_name}}')
    assert template == test_dir

    test_dir = os.path.join(repo_dir, '{{cookiecutter.repo_name }}')
    assert template != test_dir

    test_dir = os.path.join(repo_dir, '{{ cookiecutter.repo_name }}')
    assert template != test_dir


class TestFindTemplate2(unittest.TestCase):

    def test_find_template(self):
        template = find.find_template(repo_dir='tests/fake-repo-pre2'.replace("/", os.sep))
        test_dir = 'tests/fake-repo-pre2/{{cookiecutter.repo_name}}'.replace("/", os.sep)
        self.assertEqual(template, test_dir)
        test_dir = 'tests/fake-repo-pre2/{{cookiecutter.repo_name }}'.replace("/", os.sep)
        self.assertNotEqual(template, test_dir)
        test_dir = 'tests/fake-repo-pre2/{{ cookiecutter.repo_name }}'.replace("/", os.sep)
        self.assertNotEqual(template, test_dir)


if __name__ == '__main__':
    unittest.main()
