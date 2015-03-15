#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_utils
------------

Tests for `cookiecutter.utils` module.
"""

import os
import pytest
import stat
import sys

from cookiecutter import utils


def make_readonly(path):
    """Helper function that is called in the tests to change the access
    permissions of the given file.
    """
    mode = os.stat(path).st_mode
    os.chmod(path, mode & ~stat.S_IWRITE)


def test_rmtree():
    os.mkdir('foo')
    with open('foo/bar', "w") as f:
        f.write("Test data")
    make_readonly('foo/bar')
    utils.rmtree('foo')
    assert not os.path.exists('foo')


def test_make_sure_path_exists():
    if sys.platform.startswith('win'):
        existing_directory = os.path.abspath(os.curdir)
        uncreatable_directory = 'a*b'
    else:
        existing_directory = '/usr/'
        uncreatable_directory = '/this-doesnt-exist-and-cant-be-created/'

    assert utils.make_sure_path_exists(existing_directory)
    assert utils.make_sure_path_exists('tests/blah')
    assert utils.make_sure_path_exists('tests/trailingslash/')
    assert not utils.make_sure_path_exists(uncreatable_directory)
    utils.rmtree('tests/blah/')
    utils.rmtree('tests/trailingslash/')


def test_workin():
    cwd = os.getcwd()
    ch_to = 'tests/files'

    class TestException(Exception):
        pass

    def test_work_in():
        with utils.work_in(ch_to):
            test_dir = os.path.join(cwd, ch_to).replace("/", os.sep)
            assert test_dir == os.getcwd()
            raise TestException()

    # Make sure we return to the correct folder
    assert cwd == os.getcwd()

    # Make sure that exceptions are still bubbled up
    with pytest.raises(TestException):
        test_work_in()
