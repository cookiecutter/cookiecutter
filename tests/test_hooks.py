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


class TestFindHooks(unittest.TestCase):

    def test_find_hooks(self):
        '''Getting the list of all defined hooks'''
        repo_path = 'tests/test-hooks/'
        with utils.work_in(repo_path):
            self.assertEqual({
                'pre_gen_project': os.path.abspath('hooks/pre_gen_project.py'),
                'post_gen_project': os.path.abspath('hooks/post_gen_project.sh'),
            }, hooks.find_hooks())

    def test_no_hooks(self):
        '''find_hooks should return an empty dict if no hooks folder could be found. '''
        with utils.work_in('tests/fake-repo'):
            self.assertEqual({}, hooks.find_hooks())


class TestExternalHooks(unittest.TestCase):

    repo_path  = os.path.abspath('tests/test-hooks/')
    hooks_path = os.path.abspath('tests/test-hooks/hooks')

    created_files = ['tests/test-hooks/input{{hooks}}/config_file.txt',
                     'tests/test-hooks/input{{hooks}}/shell_post.txt',
                     'tests/test-hooks/input{{hooks}}/yo_mama_file.txt',
                     'tests/test-hooks/input{{hooks}}/config_file.txt',
                     'tests/shell_post.txt',
                     'shell_post.txt',
                     'tests/test-hooks/input{{hooks}}/python_pre.txt',]

    def tearDown(self):
        for i in self.created_files:
            self._rm(i)

    def _rm(self, fname):
        if os.path.exists('%s' %fname):
            os.remove('%s' % fname)


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
        tests_dir = os.path.join(self.repo_path, 'input{{hooks}}')
        with utils.work_in(self.repo_path):
            hooks.run_hook('pre_gen_project', tests_dir)
            self.assertTrue(os.path.isfile(os.path.join(tests_dir, 'python_pre.txt')))

            config_file = os.path.join(self.repo_path, "../test-evaluate/cookiecutter.json")
            hooks.run_hook('post_gen_project', tests_dir, config_file)
            self.assertTrue(os.path.isfile(os.path.join(tests_dir, 'shell_post.txt')))
            self.assertTrue(os.path.isfile(config_file))
            self.assertIn("cookiecutter.json", file(os.path.join(tests_dir, 'config_file.txt')).read())
            self.assertIn("fat", file(os.path.join(tests_dir, 'yo_mama_file.txt')).read())


if __name__ == '__main__':
    unittest.main()
