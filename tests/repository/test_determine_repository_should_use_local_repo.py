# -*- coding: utf-8 -*-
from cookiecutter import repository, exceptions

import pytest


def test_finds_local_repo():
    project_dir = repository.determine_repo_dir(
        'tests/fake-repo',
        abbreviations={},
        clone_to_dir=None,
        checkout=None,
        no_input=True
    )

    assert 'tests/fake-repo' == project_dir


def test_local_repo_with_no_context_raises(user_config_data):
    """A repository without a cookiecutter.json should raise a
    `RepositoryNotFound` exception.
    """
    with pytest.raises(exceptions.RepositoryNotFound):
        repository.determine_repo_dir(
            'tests/fake-repo-bad',
            abbreviations={},
            clone_to_dir=user_config_data['cookiecutters_dir'],
            checkout=None,
            no_input=True
        )
