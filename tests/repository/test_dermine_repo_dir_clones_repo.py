# -*- coding: utf-8 -*-
import os

import pytest

from cookiecutter.repository import determine_repo_dir


@pytest.fixture
def template_url():
    """URL to example Cookiecutter template on GitHub.

    Note: when used, git clone is mocked.
    """
    return 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'


@pytest.fixture
def output_dir(tmpdir):
    """Given a temporary dir, create an `output` subdirectory inside it and
    return its path (not a str but a py.path instance).
    """
    return tmpdir.mkdir('output')


def test_determine_repository_url_should_clone(
        mocker, template_url, output_dir, user_config_file, user_config_data):
    """`clone()` should be called with correct args when `cookiecutter()` is
    called.
    """

    mock_clone = mocker.patch(
        'cookiecutter.repository.clone',
        return_value='tests/fake-repo-tmpl',
        autospec=True
    )

    project_dir = determine_repo_dir(
        template_url,
        abbreviations={},
        cookiecutters_dir=user_config_data['cookiecutters_dir'],
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
