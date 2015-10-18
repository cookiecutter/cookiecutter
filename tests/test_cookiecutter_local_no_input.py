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

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """
    Remove special directories which are created during the tests.
    """
    def fin_remove_additional_dirs():
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-extra'):
            utils.rmtree('fake-project-extra')
        if os.path.isdir('fake-project-templated'):
            utils.rmtree('fake-project-templated')
    request.addfinalizer(fin_remove_additional_dirs)


@pytest.fixture(params=['tests/fake-repo-pre/', 'tests/fake-repo-pre'])
def bake(request):
    """
    Run cookiecutter with the given input_dir path.
    """
    main.cookiecutter(request.param, no_input=True)


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs', 'bake')
def test_cookiecutter():
    assert os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}')
    assert not os.path.isdir('tests/fake-repo-pre/fake-project')
    assert os.path.isdir('fake-project')
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_no_input_extra_context():
    """
    `Call cookiecutter()` with `no_input=True` and `extra_context
    """
    main.cookiecutter(
        'tests/fake-repo-pre',
        no_input=True,
        extra_context={'repo_name': 'fake-project-extra'}
    )
    assert os.path.isdir('fake-project-extra')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_templated_context():
    """
    `Call cookiecutter()` with `no_input=True` and templates in the
    cookiecutter.json file
    """
    main.cookiecutter(
        'tests/fake-repo-tmpl',
        no_input=True
    )
    assert os.path.isdir('fake-project-templated')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_no_input_return_project_dir():
    """Call `cookiecutter()` with `no_input=True`."""
    project_dir = main.cookiecutter('tests/fake-repo-pre', no_input=True)
    assert project_dir == os.path.abspath('fake-project')
