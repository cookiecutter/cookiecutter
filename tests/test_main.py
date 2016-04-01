# -*- coding: utf-8 -*-

import json
import os

import pytest

from cookiecutter.main import is_repo_url, expand_abbreviations, cookiecutter


@pytest.fixture(params=[
    'gitolite@server:team/repo',
    'git@github.com:audreyr/cookiecutter.git',
    'https://github.com/audreyr/cookiecutter.git',
    'git+https://private.com/gitrepo',
    'hg+https://private.com/mercurialrepo',
    'https://bitbucket.org/pokoli/cookiecutter.hg',
])
def remote_repo_url(request):
    return request.param


def test_is_repo_url_for_remote_urls(remote_repo_url):
    """Verify is_repo_url works."""
    assert is_repo_url(remote_repo_url) is True


@pytest.fixture(params=[
    '/audreyr/cookiecutter.git',
    '/home/audreyr/cookiecutter',
    (
        'c:\\users\\appveyor\\appdata\\local\\temp\\1\\pytest-0\\'
        'test_default_output_dir0\\template'
    ),
])
def local_repo_url(request):
    return request.param


def test_is_repo_url_for_local_urls(local_repo_url):
    """Verify is_repo_url works."""
    assert is_repo_url(local_repo_url) is False


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
