# -*- coding: utf-8 -*-
import os

import pytest

from cookiecutter import repository, exceptions


@pytest.fixture
def template_url():
    """URL to example Cookiecutter template on GitHub.

    Note: when used, git clone is mocked.
    """
    return 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'


def test_repository_url_should_clone(
        mocker, template_url, user_config_data):
    """`clone()` should be called with correct args when
    `determine_repo_dir()` is passed a repository template url.
    """

    mock_clone = mocker.patch(
        'cookiecutter.repository.clone',
        return_value='tests/fake-repo-tmpl',
        autospec=True
    )

    project_dir = repository.determine_repo_dir(
        template_url,
        abbreviations={},
        clone_to_dir=user_config_data['cookiecutters_dir'],
        checkout=None,
        no_input=True
    )

    mock_clone.assert_called_once_with(
        repo_url=template_url,
        checkout=None,
        clone_to_dir=user_config_data['cookiecutters_dir'],
        no_input=True
    )

    assert os.path.isdir(project_dir)
    assert 'tests/fake-repo-tmpl' == project_dir


def test_repository_url_with_no_context_file(mocker, template_url):
    mocker.patch(
        'cookiecutter.repository.clone',
        return_value='tests/fake-repo-bad',
        autospec=True
    )

    with pytest.raises(exceptions.RepositoryNotFound) as err:
        repository.determine_repo_dir(
            template_url,
            abbreviations={},
            clone_to_dir=None,
            checkout=None,
            no_input=True
        )

    assert str(err.value) == (
        'The repository tests/fake-repo-bad could not be located or does not '
        'contain a "cookiecutter.json" file.'
    )
