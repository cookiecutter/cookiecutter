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

from cookiecutter import hooks, utils


def make_test_repo(name):
    """Helper function which is called in the test setup methods."""
    hook_dir = os.path.join(name, 'hooks')
    template = os.path.join(name, 'input{{hooks}}')
    os.mkdir(name)
    os.mkdir(hook_dir)
    os.mkdir(template)

    with open(os.path.join(template, 'README.rst'), 'w') as f:
        f.write("foo\n===\n\nbar\n")

    with open(os.path.join(hook_dir, 'pre_gen_project.py'), 'w') as f:
        f.write("#!/usr/bin/env python\n")
        f.write("# -*- coding: utf-8 -*-\n")
        f.write("from __future__ import print_function\n")
        f.write("\n")
        f.write("print('pre generation hook')\n")
        f.write("f = open('python_pre.txt', 'w')\n")
        f.write("f.close()\n")

    if sys.platform.startswith('win'):
        post = 'post_gen_project.bat'
        with open(os.path.join(hook_dir, post), 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        post = 'post_gen_project.sh'
        filename = os.path.join(hook_dir, post)
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

    return post


class TestFindHooks(object):

    repo_path = 'tests/test-hooks'

    def setup_method(self, method):
        self.post_hook = make_test_repo(self.repo_path)

    def teardown_method(self, method):
        utils.rmtree(self.repo_path)

    def test_find_hook(self):
        """Finds the specified hook."""

        with utils.work_in(self.repo_path):
            expected = {
                'pre_gen_project': os.path.abspath('hooks/pre_gen_project.py'),
                'post_gen_project': os.path.abspath(
                    os.path.join('hooks', self.post_hook)
                ),
            }
            assert expected == hooks.find_hooks()

    def test_no_hooks(self):
        """find_hooks should return None if the hook could not be found."""

        with utils.work_in('tests/fake-repo'):
            assert {} == hooks.find_hooks()


class TestExternalHooks(object):

    repo_path = os.path.abspath('tests/test-hooks/')
    hooks_path = os.path.abspath('tests/test-hooks/hooks')

    def setup_method(self, method):
        self.post_hook = make_test_repo(self.repo_path)

    def teardown_method(self, method):
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
        if os.path.exists('tests/context_post.txt'):
            os.remove('tests/context_post.txt')

    def test_run_script(self):
        """Execute a hook script, independently of project generation"""
        hooks.run_script(os.path.join(self.hooks_path, self.post_hook))
        assert os.path.isfile('shell_post.txt')

    def test_run_script_cwd(self):
        """Change directory before running hook"""
        hooks.run_script(
            os.path.join(self.hooks_path, self.post_hook),
            'tests'
        )
        assert os.path.isfile('tests/shell_post.txt')
        assert 'tests' not in os.getcwd()

    def test_run_script_with_context(self):
        """Execute a hook script, passing a context"""

        hook_path = os.path.join(self.hooks_path, 'post_gen_project.sh')

        if sys.platform.startswith('win'):
            post = 'post_gen_project.bat'
            with open(os.path.join(self.hooks_path, post), 'w') as f:
                f.write("@echo off\n")
                f.write("\n")
                f.write("echo post generation hook\n")
                f.write("echo. >{{cookiecutter.file}}\n")
        else:
            with open(hook_path, 'w') as fh:
                fh.write("#!/bin/bash\n")
                fh.write("\n")
                fh.write("echo 'post generation hook';\n")
                fh.write("touch 'shell_post.txt'\n")
                fh.write("touch '{{cookiecutter.file}}'\n")
                os.chmod(hook_path, os.stat(hook_path).st_mode | stat.S_IXUSR)

        hooks.run_script_with_context(
            os.path.join(self.hooks_path, self.post_hook),
            'tests',
            {
                'cookiecutter': {
                    'file': 'context_post.txt'
                }
            })
        assert os.path.isfile('tests/context_post.txt')
        assert 'tests' not in os.getcwd()

    def test_run_hook(self):
        """Execute hook from specified template in specified output
        directory.
        """
        tests_dir = os.path.join(self.repo_path, 'input{{hooks}}')
        with utils.work_in(self.repo_path):
            hooks.run_hook('pre_gen_project', tests_dir, {})
            assert os.path.isfile(os.path.join(tests_dir, 'python_pre.txt'))

            hooks.run_hook('post_gen_project', tests_dir, {})
            assert os.path.isfile(os.path.join(tests_dir, 'shell_post.txt'))
