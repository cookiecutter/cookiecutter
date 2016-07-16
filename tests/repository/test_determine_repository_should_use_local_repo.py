# -*- coding: utf-8 -*-
from cookiecutter import repository, exceptions

import pytest


def test_finds_local_repo(tmpdir):
    """A valid local repository should be returned."""
    project_dir = repository.determine_repo_dir(
        'tests/fake-repo',
        abbreviations={},
        clone_to_dir=str(tmpdir),
        checkout=None,
        no_input=True
    )

    assert 'tests/fake-repo' == project_dir


def test_local_repo_with_no_context_raises(tmpdir):
    """A local repository without a cookiecutter.json should raise a
    `RepositoryNotFound` exception.
    """
    with pytest.raises(exceptions.RepositoryNotFound) as err:
        repository.determine_repo_dir(
            'tests/fake-repo-bad',
            abbreviations={},
            clone_to_dir=str(tmpdir),
            checkout=None,
            no_input=True
        )

    assert str(err.value) == (
        'The repository tests/fake-repo-bad could not be located or does not '
        'contain a "cookiecutter.json" file.'
    )


def test_local_repo_typo(tmpdir):
    """An unknown local repository should raise a `RepositoryNotFound`
    exception.
    """
    with pytest.raises(exceptions.RepositoryNotFound) as err:
        repository.determine_repo_dir(
            'tests/unknown-repo',
            abbreviations={},
            clone_to_dir=str(tmpdir),
            checkout=None,
            no_input=True
        )

    assert str(err.value) == (
        'The repository tests/unknown-repo could not be located or does not '
        'contain a "cookiecutter.json" file.'
    )
