#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs_prompt
---------------
"""

import os
import pytest

from cookiecutter import utils, vcs
from tests.skipif_markers import skipif_no_network


@pytest.fixture(autouse=True)
def clean_cookiecutter_dirs(request):
    if os.path.isdir('cookiecutter-pypackage'):
        utils.rmtree('cookiecutter-pypackage')
    os.mkdir('cookiecutter-pypackage/')
    if os.path.isdir('cookiecutter-trytonmodule'):
        utils.rmtree('cookiecutter-trytonmodule')
    os.mkdir('cookiecutter-trytonmodule/')

    def remove_cookiecutter_dirs():
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')
    request.addfinalizer(remove_cookiecutter_dirs)


@skipif_no_network
def test_git_clone_overwrite(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.vcs.read_user_yes_no',
        lambda question, default: True
    )
    repo_dir = vcs.clone(
        'https://github.com/audreyr/cookiecutter-pypackage.git'
    )
    assert repo_dir == 'cookiecutter-pypackage'
    assert os.path.isfile('cookiecutter-pypackage/README.rst')


@skipif_no_network
def test_git_clone_overwrite_with_no_prompt():
    repo_dir = vcs.clone(
        'https://github.com/audreyr/cookiecutter-pypackage.git',
        no_input=True
    )
    assert repo_dir == 'cookiecutter-pypackage'
    assert os.path.isfile('cookiecutter-pypackage/README.rst')


@skipif_no_network
def test_git_clone_cancel(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.vcs.read_user_yes_no',
        lambda question, default: False
    )

    with pytest.raises(SystemExit):
        vcs.clone('https://github.com/audreyr/cookiecutter-pypackage.git')


@skipif_no_network
def test_hg_clone_overwrite(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.vcs.read_user_yes_no',
        lambda question, default: True
    )
    repo_dir = vcs.clone(
        'https://bitbucket.org/pokoli/cookiecutter-trytonmodule'
    )
    assert repo_dir == 'cookiecutter-trytonmodule'
    assert os.path.isfile('cookiecutter-trytonmodule/README.rst')


@skipif_no_network
def test_hg_clone_cancel(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.vcs.read_user_yes_no',
        lambda question, default: False
    )

    with pytest.raises(SystemExit):
        vcs.clone('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
