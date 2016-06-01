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
from cookiecutter.exceptions import MissingRequiredMethod


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


def test_force_delete(mocker):
    path = 'foo'
    func = mocker.MagicMock(return_value=path)
    os.mkdir(path)
    make_readonly(path)
    utils.force_delete(func, path, None)
    mode = os.stat(path).st_mode
    func.assert_called_once_with(path)
    assert bool(mode & stat.S_IWRITE)
    os.rmdir(path)


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


@pytest.fixture
def get_api_checker_fixtures():
    """
    helper method to provide some classes needed for api checker testing
    """
    class Conform(object):
        def method1(self):
            return

        def method2(self):
            return

    class MissingMethod1(object):
        def method2(self):
            return

    class MissingMethod2(object):
        def method1(self):
            return

    return {
        'conform': Conform,
        'method1': MissingMethod1,
        'method2': MissingMethod2
    }


def test_api_checker():
    fixtures = get_api_checker_fixtures()
    api = ['method1', 'method2']
    checker = utils.ApiChecker(*api)

    checker.implements_api(fixtures['conform'])

    for method in api:
        with pytest.raises(MissingRequiredMethod) as excinfo:
            checker.implements_api(fixtures[method])

        assert method in excinfo.value.message
