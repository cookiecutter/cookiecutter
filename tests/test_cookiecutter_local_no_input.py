#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cookiecutter_local_no_input
--------------------------------

Tests formerly known from a unittest residing in test_main.py named
TestCookiecutterLocalNoInput.test_cookiecutter
TestCookiecutterLocalNoInput.test_cookiecutter_no_slash
TestCookiecutterLocalNoInput.test_cookiecutter_no_input_extra_context
TestCookiecutterLocalNoInput.test_cookiecutter_templated_context
"""

import os
import pytest

from cookiecutter import main
from tests.utils import dir_tests


@pytest.fixture(params=[
    dir_tests('fake-repo-pre'),
    dir_tests('fake-repo-pre2')
])
def bake(request, tmpdir):
    """
    Run cookiecutter with the given input_dir path.
    """
    os.chdir(str(tmpdir))

    main.cookiecutter(request.param, no_input=True)


@pytest.mark.usefixtures('bake')
def test_cookiecutter():
    assert os.path.isdir(dir_tests('fake-repo-pre/{{cookiecutter.repo_name}}'))
    assert not os.path.isdir(dir_tests('fake-repo-pre/fake-project'))
    assert os.path.isdir('fake-project')
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')


def test_cookiecutter_no_input_extra_context():
    """
    `Call cookiecutter()` with `no_input=True` and `extra_context
    """

    main.cookiecutter(
        dir_tests('fake-repo-pre'),
        no_input=True,
        extra_context={'repo_name': 'fake-project-extra'}
    )
    assert os.path.isdir('fake-project-extra')


def test_cookiecutter_templated_context():
    """
    `Call cookiecutter()` with `no_input=True` and templates in the
    cookiecutter.json file
    """

    main.cookiecutter(dir_tests('fake-repo-tmpl'), no_input=True)
    assert os.path.isdir('fake-project-templated')


def test_cookiecutter_no_input_return_project_dir():
    """Call `cookiecutter()` with `no_input=True`."""

    project_dir = main.cookiecutter(dir_tests('fake-repo-pre'), no_input=True)
    assert project_dir == os.path.abspath('fake-project')
