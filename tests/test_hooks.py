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

from cookiecutter import hooks, utils

if sys.platform.startswith('win'):
    shell_script_hook = 'post_gen_project.bat'
    repo_path = os.path.abspath(os.path.join('tests', 'test-hooks-win'))
else:
    shell_script_hook = 'post_gen_project.sh'
    repo_path = os.path.abspath(os.path.join('tests', 'test-hooks-unix'))


class TestFindHooks(unittest.TestCase):


    def test_find_hooks(self):
        '''Getting the list of all defined hooks'''
        with utils.work_in(repo_path):
            self.assertEqual({
                'pre_gen_project': os.path.abspath('hooks/pre_gen_project.py'),
                'post_gen_project': os.path.abspath(os.path.join('hooks', shell_script_hook)),
            }, hooks.find_hooks())

    def test_no_hooks(self):
        '''find_hooks should return an empty dict if no hooks folder could be found. '''
        with utils.work_in('tests/fake-repo'):
            self.assertEqual({}, hooks.find_hooks())


class TestExternalHooks(unittest.TestCase):

    hooks_path = os.path.join(repo_path, 'hooks')

    def tearDown(self):
        if os.path.exists('python_pre.txt'):
            os.remove('python_pre.txt')
        if os.path.exists('shell_post.txt'):
            os.remove('shell_post.txt')
        if os.path.exists('tests/shell_post.txt'):
            os.remove('tests/shell_post.txt')
        if os.path.exists(os.path.join(repo_path, 'input{{hooks}}/python_pre.txt')):
            os.remove(os.path.join(repo_path, 'input{{hooks}}/python_pre.txt'))
        if os.path.exists(os.path.join(repo_path, 'input{{hooks}}/shell_post.txt')):
            os.remove(os.path.join(repo_path, 'input{{hooks}}/shell_post.txt'))

    def test_run_hook(self):
        '''execute a hook script, independently of project generation'''
        hooks._run_hook(os.path.join(self.hooks_path, shell_script_hook))
        self.assertTrue(os.path.isfile('shell_post.txt'))

    def test_run_hook_cwd(self):
        '''Change directory before running hook'''
        hooks._run_hook(os.path.join(self.hooks_path, shell_script_hook), 
                        'tests')
        self.assertTrue(os.path.isfile('tests/shell_post.txt'))
        self.assertFalse('tests' in os.getcwd())
        
    def test_public_run_hook(self):
        '''Execute hook from specified template in specified output directory'''
        tests_dir = 'input{{hooks}}'
        with utils.work_in(repo_path):
            hooks.run_hook('pre_gen_project', tests_dir)
            self.assertTrue(os.path.isfile(os.path.join(tests_dir, 'python_pre.txt')))

            hooks.run_hook('post_gen_project', tests_dir)
            self.assertTrue(os.path.isfile(os.path.join(tests_dir, 'shell_post.txt')))


if __name__ == '__main__':
    unittest.main()
