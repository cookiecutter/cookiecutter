# -*- coding: utf-8 -*-

"""
test_cookiecutter_local_with_input.

Tests formerly known from a unittest residing in test_main.py named
TestCookiecutterLocalWithInput.test_cookiecutter_local_with_input
TestCookiecutterLocalWithInput.test_cookiecutter_input_extra_context
"""

import os

import pytest

from cookiecutter import main, utils


@pytest.fixture(scope='function')
def remove_additional_dirs(request):
    """Remove special directories which are created during the tests."""
    def fin_remove_additional_dirs():
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
        if os.path.isdir('fake-project-input-extra'):
            utils.rmtree('fake-project-input-extra')
    request.addfinalizer(fin_remove_additional_dirs)


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_local_with_input(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda var, default: default
    )
    main.cookiecutter('tests/fake-repo-pre/', no_input=False)
    assert os.path.isdir('tests/fake-repo-pre/{{cookiecutter.repo_name}}')
    assert not os.path.isdir('tests/fake-repo-pre/fake-project')
    assert os.path.isdir('fake-project')
    assert os.path.isfile('fake-project/README.rst')
    assert not os.path.exists('fake-project/json/')


@pytest.mark.usefixtures('clean_system', 'remove_additional_dirs')
def test_cookiecutter_input_extra_context(monkeypatch):
    """Call `cookiecutter()` with `no_input=False` and `extra_context`."""
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda var, default: default
    )
    main.cookiecutter(
        'tests/fake-repo-pre',
        no_input=False,
        extra_context={'repo_name': 'fake-project-input-extra'}
    )
    assert os.path.isdir('fake-project-input-extra')
