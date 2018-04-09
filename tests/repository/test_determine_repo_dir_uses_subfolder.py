# -*- coding: utf-8 -*-
import os

import pytest

from cookiecutter import repository


@pytest.fixture
def template_url():
    """URL to example Cookiecutter template on GitHub.

    Note: when used, git clone is mocked.
    """
    return 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'


@pytest.fixture
def subfolder():
    """Returns normalized subfolder path"""
    return os.path.normpath('tests/fake-repo-tmpl-sf/fake_template')


def test_subfolder_added_to_repo_dir(
        mocker, template_url, user_config_data):
    """`determine_repo_dir()` returns cloned repo path
    with subfolder attached.
    """

    mocker.patch(
        'cookiecutter.repository.clone',
        return_value='tests/fake-repo-tmpl-sf',
        autospec=True
    )

    project_dir, cleanup = repository.determine_repo_dir(
        template_url,
        abbreviations={},
        clone_to_dir=user_config_data['cookiecutters_dir'],
        checkout=None,
        no_input=True,
        subfolder='fake_template'
    )

    assert os.path.isdir(project_dir)
    assert subfolder() == project_dir
