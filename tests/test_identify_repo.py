#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_identify_repo
------------------
"""

import pytest

from cookiecutter import exceptions, vcs


def test_identify_git_github():
    repo_url = 'https://github.com/audreyr/cookiecutter-pypackage.git'
    assert vcs.identify_repo(repo_url)[0] == 'git'


def test_identify_git_github_no_extension():
    repo_url = 'https://github.com/audreyr/cookiecutter-pypackage'
    assert vcs.identify_repo(repo_url)[0] == 'git'


def test_identify_git_gitorious():
    repo_url = (
        'git@gitorious.org:cookiecutter-gitorious/cookiecutter-gitorious.git'
    )
    assert vcs.identify_repo(repo_url)[0] == 'git'


def test_identify_hg_mercurial():
    repo_url = 'https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket'
    assert vcs.identify_repo(repo_url)[0] == 'hg'


def test_unknown_repo_type():
    repo_url = 'http://norepotypespecified.com'
    with pytest.raises(exceptions.UnknownRepoType):
        vcs.identify_repo(repo_url)[0]
