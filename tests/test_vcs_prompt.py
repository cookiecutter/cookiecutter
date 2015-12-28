#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs_prompt
---------------
"""

import os
import pytest

from cookiecutter import vcs
from tests.skipif_markers import skipif_no_network, skipif_no_hg


@pytest.fixture(autouse=True)
def setup(tmpdir):
    tmpdir.mkdir('cookiecutter-pypackage/')
    tmpdir.mkdir('cookiecutter-trytonmodule/')


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


@skipif_no_hg
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


@skipif_no_hg
@skipif_no_network
def test_hg_clone_cancel(monkeypatch):
    monkeypatch.setattr(
        'cookiecutter.vcs.read_user_yes_no',
        lambda question, default: False
    )

    with pytest.raises(SystemExit):
        vcs.clone('https://bitbucket.org/pokoli/cookiecutter-trytonmodule')
