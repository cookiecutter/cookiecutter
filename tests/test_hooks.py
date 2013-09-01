#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hooks
------------

Tests for `cookiecutter.hooks` module.
"""

import sys
import os
import unittest

from cookiecutter import hooks


class TestFindHooks(unittest.TestCase):

    def test_find_hooks(self):
        '''Getting the list of all defined hooks'''
        repo_path = 'tests/input{{hooks}}'
        self.assertEqual({
            'pre_gen_project': os.path.abspath(
                os.path.join(repo_path, 'hooks', 'pre_gen_project.py')),
            'post_gen_project': os.path.abspath(
                os.path.join(repo_path, 'hooks', 'post_gen_project.sh')),
        }, hooks.find_hooks(repo_path))

    def test_no_hooks(self):
        '''find_hooks should return an empty dict if no hooks folder could be found. '''
        self.assertEqual({}, hooks.find_hooks('tests/fake-repo'))


class TestExternalHooks(unittest.TestCase):

    repo_path  = os.path.abspath('tests/input{{hooks}}')
    hooks_path = os.path.join(repo_path, 'hooks')

    def tearDown(self):
        if os.path.exists('python_pre.txt'):
            os.remove('python_pre.txt')
        if os.path.exists('shell_post.txt'):
            os.remove('shell_post.txt')
        if os.path.exists('tests/python_pre.txt'):
            os.remove('tests/python_pre.txt')
        if os.path.exists('tests/shell_post.txt'):
            os.remove('tests/shell_post.txt')

    def test_run_hook(self):
        '''execute a hook script, independently of project generation'''
        hooks._run_hook(os.path.join(self.hooks_path, 'post_gen_project.sh'))
        self.assertTrue(os.path.isfile('shell_post.txt'))

    def test_run_hook_cwd(self):
        '''Change directory before running hook'''
        hooks._run_hook(os.path.join(self.hooks_path, 'post_gen_project.sh'), 
                        'tests')
        self.assertTrue(os.path.isfile('tests/shell_post.txt'))
        self.assertFalse('tests' in os.getcwd())
        
    def test_public_run_hook(self):
        '''Execute hook from specified template in specified output directory'''
        hooks.run_hook('pre_gen_project', self.repo_path, 'tests')
        self.assertTrue(os.path.isfile('tests/python_pre.txt'))

        hooks.run_hook('post_gen_project', self.repo_path, 'tests')
        self.assertTrue(os.path.isfile('tests/shell_post.txt'))


if __name__ == '__main__':
    unittest.main()
