#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_hooks
------------

Tests for `cookiecutter.hooks` module.
"""

import sys
import os
import stat
import unittest

from cookiecutter import hooks, utils

def make_test_repo(name):
    hooks = os.path.join(name, 'hooks')
    template = os.path.join(name, 'input{{hooks}}')
    os.mkdir(name)
    os.mkdir(hooks)
    os.mkdir(template)

    with open(os.path.join(template, 'README.rst'), 'w') as f:
        f.write("foo\n===\n\nbar\n")

    with open(os.path.join(hooks, 'pre_gen_project.py'), 'w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("from __future__ import print_function\n")
        f.write("\n")
        f.write("print('pre generation hook')\n")
        f.write("f = open('python_pre.txt', 'w')\n")
        f.write("f.close()\n")

    if sys.platform.startswith('win'):
        post = 'post_gen_project.bat'
        with open(os.path.join(hooks, post), 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        post = 'post_gen_project.sh'
        filename = os.path.join(hooks, post)
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

    return post


class TestFindHooks(unittest.TestCase):

    repo_path = 'tests/test-hooks'

    def setUp(self):
        self.post_hook = make_test_repo(self.repo_path)

    def tearDown(self):
        utils.rmtree(self.repo_path)

    def test_find_hooks(self):
        '''Getting the list of all defined hooks'''
        with utils.work_in(self.repo_path):
            self.assertEqual({
                'pre_gen_project': os.path.abspath('hooks/pre_gen_project.py'),
                'post_gen_project': os.path.abspath(os.path.join('hooks', self.post_hook)),
            }, hooks.find_hooks())

    def test_no_hooks(self):
        '''find_hooks should return an empty dict if no hooks folder could be found. '''
        with utils.work_in('tests/fake-repo'):
            self.assertEqual({}, hooks.find_hooks())


class TestExternalHooks(unittest.TestCase):

    repo_path  = os.path.abspath('tests/test-hooks/')
    hooks_path = os.path.abspath('tests/test-hooks/hooks')

    def setUp(self):
        self.post_hook = make_test_repo(self.repo_path)

    def tearDown(self):
        utils.rmtree(self.repo_path)

        if os.path.exists('python_pre.txt'):
            os.remove('python_pre.txt')
        if os.path.exists('shell_post.txt'):
            os.remove('shell_post.txt')
        if os.path.exists('tests/shell_post.txt'):
            os.remove('tests/shell_post.txt')
        if os.path.exists('tests/test-hooks/input{{hooks}}/python_pre.txt'):
            os.remove('tests/test-hooks/input{{hooks}}/python_pre.txt')
        if os.path.exists('tests/test-hooks/input{{hooks}}/shell_post.txt'):
            os.remove('tests/test-hooks/input{{hooks}}/shell_post.txt')

    def test_run_hook(self):
        '''execute a hook script, independently of project generation'''
        hooks._run_hook(os.path.join(self.hooks_path, self.post_hook))
        self.assertTrue(os.path.isfile('shell_post.txt'))

    def test_run_hook_cwd(self):
        '''Change directory before running hook'''
        hooks._run_hook(os.path.join(self.hooks_path, self.post_hook), 
                        'tests')
        self.assertTrue(os.path.isfile('tests/shell_post.txt'))
        self.assertFalse('tests' in os.getcwd())
        
    def test_public_run_hook(self):
        '''Execute hook from specified template in specified output directory'''
        tests_dir = os.path.join(self.repo_path, 'input{{hooks}}')
        with utils.work_in(self.repo_path):
            hooks.run_hook('pre_gen_project', tests_dir)
            self.assertTrue(os.path.isfile(os.path.join(tests_dir, 'python_pre.txt')))

            hooks.run_hook('post_gen_project', tests_dir)
            self.assertTrue(os.path.isfile(os.path.join(tests_dir, 'shell_post.txt')))


if __name__ == '__main__':
    unittest.main()
