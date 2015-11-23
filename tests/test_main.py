# -*- coding: utf-8 -*-

import json
import os
import pytest

from cookiecutter.main import is_repo_url, expand_abbreviations, cookiecutter


def test_is_repo_url():
    """Verify is_repo_url works."""
    assert is_repo_url('gitolite@server:team/repo') is True
    assert is_repo_url('git@github.com:audreyr/cookiecutter.git') is True
    assert is_repo_url('https://github.com/audreyr/cookiecutter.git') is True
    assert is_repo_url('https://bitbucket.org/pokoli/cookiecutter.hg') is True

    assert is_repo_url('/audreyr/cookiecutter.git') is False
    assert is_repo_url('/home/audreyr/cookiecutter') is False

    appveyor_temp_dir = (
        'c:\\users\\appveyor\\appdata\\local\\temp\\1\\pytest-0\\'
        'test_default_output_dir0\\template'
    )
    assert is_repo_url(appveyor_temp_dir) is False


def test_expand_abbreviations():
    template = 'gh:audreyr/cookiecutter-pypackage'

    # This is not a valid repo url just yet!
    # First `main.expand_abbreviations` needs to translate it
    assert is_repo_url(template) is False

    expanded_template = expand_abbreviations(template, {})
    assert is_repo_url(expanded_template) is True


@pytest.fixture(scope='session')
def user_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('user_dir')


@pytest.fixture(scope='session')
def user_config_data(user_dir):
    cookiecutters_dir = user_dir.mkdir('cookiecutters')
    replay_dir = user_dir.mkdir('cookiecutter_replay')

    return {
        'cookiecutters_dir': str(cookiecutters_dir),
        'replay_dir': str(replay_dir),
        'default_context': {}
    }


@pytest.fixture(scope='session')
def user_config_file(user_dir, user_config_data):
    config_file = user_dir.join('config')
    config_file.write(json.dumps(user_config_data))
    return str(config_file)


@pytest.fixture
def template_url():
    return 'https://github.com/pytest-dev/cookiecutter-pytest-plugin.git'


@pytest.fixture
def output_dir(tmpdir):
    return tmpdir.mkdir('output')


def test_cookiecutter_repository_url_should_clone(
        mocker, template_url, output_dir, user_config_file, user_config_data):
    mock_clone = mocker.patch(
        'cookiecutter.main.clone',
        return_value='tests/fake-repo-tmpl',
        autospec=True
    )

    project_dir = cookiecutter(
        template_url,
        no_input=True,
        output_dir=str(output_dir),
        config_file=user_config_file
    )

    mock_clone.assert_called_once_with(
        repo_url=template_url,
        checkout=None,
        clone_to_dir=user_config_data['cookiecutters_dir'],
        no_input=True
    )

    assert os.path.isdir(project_dir)
