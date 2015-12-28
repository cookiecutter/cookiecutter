#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_hooks
-------------------

Tests formerly known from a unittest residing in test_generate.py named
TestHooks.test_ignore_hooks_dirs
TestHooks.test_run_python_hooks
TestHooks.test_run_python_hooks_cwd
TestHooks.test_run_shell_hooks
"""

from __future__ import unicode_literals

import sys

import os
import stat

from cookiecutter import generate
from tests.utils import dir_tests


def test_ignore_hooks_dirs(tmpdir):
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir=dir_tests('test-pyhooks'),
        output_dir=str(tmpdir.join('test-pyhooks'))
    )
    assert not os.path.exists(dir_tests('test-pyhooks/inputpyhooks/hooks'))


def test_run_python_hooks(tmpdir):
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir=dir_tests('test-pyhooks'),
        output_dir=str(tmpdir.join('test-pyhooks'))
    )
    pre_file = str(tmpdir.join('test-pyhooks/inputpyhooks/python_pre.txt'))
    post_file = str(tmpdir.join('test-pyhooks/inputpyhooks/python_post.txt'))
    assert os.path.exists(pre_file)
    assert os.path.exists(post_file)


def test_run_python_hooks_cwd():
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir=dir_tests('test-pyhooks/')
    )
    assert os.path.exists('inputpyhooks/python_pre.txt')
    assert os.path.exists('inputpyhooks/python_post.txt')


def make_test_repo(name, tmpdir):
    repo = tmpdir.mkdir(name)
    repo_hooks = repo.mkdir('hooks')
    repo_template = repo.mkdir('input{{cookiecutter.shellhooks}}')

    with repo_template.join('README.rst').open('w') as f:
        f.write("foo\n===\n\nbar\n")

    if sys.platform.startswith('win'):
        filename = repo_hooks.join('pre_gen_project.bat')
        with filename.open('w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo pre generation hook\n")
            f.write("echo. >shell_pre.txt\n")

        filename = repo_hooks.join('post_gen_project.bat')
        with filename.open('w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        filename = repo_hooks.join('pre_gen_project.sh')
        with filename.open('w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'pre generation hook';\n")
            f.write("touch 'shell_pre.txt'\n")
        # Set the execute bit
        os.chmod(str(filename), os.stat(str(filename)).st_mode | stat.S_IXUSR)

        filename = repo_hooks.join('post_gen_project.sh')
        with filename.open('w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        os.chmod(str(filename), os.stat(str(filename)).st_mode | stat.S_IXUSR)


def test_run_shell_hooks(tmpdir):
    make_test_repo('test-shellhooks', tmpdir)
    generate.generate_files(
        context={
            'cookiecutter': {'shellhooks': 'shellhooks'}
        },
        repo_dir=str(tmpdir.join('test-shellhooks')),
        output_dir=str(tmpdir.join('test-shellhooks'))
    )
    pre_file = tmpdir.join('test-shellhooks/inputshellhooks/shell_pre.txt')
    post_file = tmpdir.join('test-shellhooks/inputshellhooks/shell_post.txt')
    assert os.path.exists(str(pre_file))
    assert os.path.exists(str(post_file))
