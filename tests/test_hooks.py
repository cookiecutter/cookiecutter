#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hooks
------------

Tests for `cookiecutter.hooks` module.
"""

import os
import shutil
import unittest

from cookiecutter import hooks


class TestFindHooks(unittest.TestCase):

    def test_find_hooks(self):
        '''Getting the list of all defined hooks'''
        repo_path = 'tests/fake-repo-hooks'
        self.assertEqual({
            'pre_gen_project': os.path.abspath(
                os.path.join(repo_path, 'hooks', 'pre_gen_project.py')),
            'post_gen_project': os.path.abspath(
                os.path.join(repo_path, 'hooks', 'post_gen_project.sh')),
        }, hooks.find_hooks(repo_path))

    def test_no_hooks(self):
        '''find_hooks should return an empty dict if no hooks folder could be found. '''
        self.assertEqual({}, hooks.find_hooks('tests/fake-repo'))


class TestHooks(unittest.TestCase):

    repo_path = 'tests/fake-repo-hooks'
