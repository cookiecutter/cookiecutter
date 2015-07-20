#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cookiecutter_repo_arg
--------------------------

Tests formerly known from a unittest residing in test_main.py named
TestCookiecutterRepoArg.test_cookiecutter_git
TestCookiecutterRepoArg.test_cookiecutter_mercurial
"""

from __future__ import unicode_literals
import os
import pytest

from cookiecutter import main, utils
from tests.skipif_markers import skipif_no_network


@pytest.fixture(scope='function')
def remove_additional_folders(request):
    """
    Remove some special folders which are created by the tests.
    """
    def fin_remove_additional_folders():
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('boilerplate'):
            utils.rmtree('boilerplate')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')
        if os.path.isdir('module_name'):
            utils.rmtree('module_name')
    request.addfinalizer(fin_remove_additional_folders)


@skipif_no_network
@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_cookiecutter_git(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda var, default: default
    )
    main.cookiecutter('https://github.com/audreyr/cookiecutter-pypackage.git')
    clone_dir = os.path.join(
        os.path.expanduser('~/.cookiecutters'),
        'cookiecutter-pypackage'
    )
    assert os.path.exists(clone_dir)
    assert os.path.isdir('boilerplate')
    assert os.path.isfile('boilerplate/README.rst')
    assert os.path.exists('boilerplate/setup.py')


@skipif_no_network
@pytest.mark.usefixtures('clean_system', 'remove_additional_folders')
def test_cookiecutter_mercurial(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.prompt.read_user_variable',
        lambda var, default: default
    )

    main.cookiecutter('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
    clone_dir = os.path.join(
        os.path.expanduser('~/.cookiecutters'),
        'cookiecutter-trytonmodule'
    )
    assert os.path.exists(clone_dir)
    assert os.path.isdir('module_name')
    assert os.path.isfile('module_name/README')
    assert os.path.exists('module_name/setup.py')
