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
        'A valid repository for "{}" could not be found in the following '
        'locations:\n{}'.format(
            'tests/fake-repo-bad',
            '\n'.join([
                'tests/fake-repo-bad',
                str(tmpdir / 'tests/fake-repo-bad')
            ]),
        )
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
        'A valid repository for "{}" could not be found in the following '
        'locations:\n{}'.format(
            'tests/unknown-repo',
            '\n'.join([
                'tests/unknown-repo',
                str(tmpdir / 'tests/unknown-repo')
            ]),
        )
    )
