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
import os
import sys
import stat
import pytest

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_additional_folders(request):
    """
    Remove some special folders which are created by the tests.
    """
    def fin_remove_additional_folders():
        if os.path.exists('tests/test-pyhooks/inputpyhooks'):
            utils.rmtree('tests/test-pyhooks/inputpyhooks')
        if os.path.exists('inputpyhooks'):
            utils.rmtree('inputpyhooks')
        if os.path.exists('tests/test-shellhooks'):
            utils.rmtree('tests/test-shellhooks')
    request.addfinalizer(fin_remove_additional_folders)


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_ignore_hooks_dirs():
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir='tests/test-pyhooks/',
        output_dir='tests/test-pyhooks/'
    )
    assert not os.path.exists('tests/test-pyhooks/inputpyhooks/hooks')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_python_hooks():
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir='tests/test-pyhooks/'.replace("/", os.sep),
        output_dir='tests/test-pyhooks/'.replace("/", os.sep)
    )
    assert os.path.exists('tests/test-pyhooks/inputpyhooks/python_pre.txt')
    assert os.path.exists('tests/test-pyhooks/inputpyhooks/python_post.txt')


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_python_hooks_cwd():
    generate.generate_files(
        context={
            'cookiecutter': {'pyhooks': 'pyhooks'}
        },
        repo_dir='tests/test-pyhooks/'
    )
    assert os.path.exists('inputpyhooks/python_pre.txt')
    assert os.path.exists('inputpyhooks/python_post.txt')


def make_test_repo(name):
    hooks = os.path.join(name, 'hooks')
    template = os.path.join(name, 'input{{cookiecutter.shellhooks}}')
    os.mkdir(name)
    os.mkdir(hooks)
    os.mkdir(template)

    with open(os.path.join(template, 'README.rst'), 'w') as f:
        f.write("foo\n===\n\nbar\n")

    if sys.platform.startswith('win'):
        filename = os.path.join(hooks, 'pre_gen_project.bat')
        with open(filename, 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo pre generation hook\n")
            f.write("echo. >shell_pre.txt\n")

        filename = os.path.join(hooks, 'post_gen_project.bat')
        with open(filename, 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        filename = os.path.join(hooks, 'pre_gen_project.sh')
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'pre generation hook';\n")
            f.write("touch 'shell_pre.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

        filename = os.path.join(hooks, 'post_gen_project.sh')
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)


@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_run_shell_hooks():
    make_test_repo('tests/test-shellhooks')
    generate.generate_files(
        context={
            'cookiecutter': {'shellhooks': 'shellhooks'}
        },
        repo_dir='tests/test-shellhooks/',
        output_dir='tests/test-shellhooks/'
    )
    shell_pre_file = 'tests/test-shellhooks/inputshellhooks/shell_pre.txt'
    shell_post_file = 'tests/test-shellhooks/inputshellhooks/shell_post.txt'
    assert os.path.exists(shell_pre_file)
    assert os.path.exists(shell_post_file)
