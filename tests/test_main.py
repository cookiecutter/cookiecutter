# -*- coding: utf-8 -*-

import os

import pytest

from cookiecutter.main import is_repo_url, expand_abbreviations, cookiecutter

USER_CONFIG = u"""
cookiecutters_dir: "{cookiecutters_dir}"
replay_dir: "{replay_dir}"
"""


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
    """Fixture that simulates the user's home directory"""
    return tmpdir_factory.mktemp('user_dir')


@pytest.fixture(scope='session')
def user_config_data(user_dir):
    """Fixture that creates 2 Cookiecutter user config dirs in the user's home
    directory:
    * `cookiecutters_dir`
    * `cookiecutter_replay`

    :returns: Dict with name of both user config dirs
    """
    cookiecutters_dir = user_dir.mkdir('cookiecutters')
    replay_dir = user_dir.mkdir('cookiecutter_replay')

    return {
        'cookiecutters_dir': str(cookiecutters_dir),
        'replay_dir': str(replay_dir),
    }


@pytest.fixture(scope='session')
def user_config_file(user_dir, user_config_data):
    """Fixture that creates a config file called `config` in the user's home
    directory, with YAML from `user_config_data`.

    :param user_dir: Simulated user's home directory
    :param user_config_data: Dict of config values
    :returns: String of path to config file
    """
    config_file = user_dir.join('config')

    config_text = USER_CONFIG.format(**user_config_data)
    config_file.write(config_text)
    return str(config_file)


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


def test_cookiecutter_repository_url_should_clone(
        mocker, template_url, output_dir, user_config_file, user_config_data):
    """`clone()` should be called with correct args when `cookiecutter()` is
    called.
    """
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


def test_replay_dump_template_name(
        monkeypatch, mocker, user_config_data, user_config_file):
    """Check that replay_dump is called with a valid template_name that is
    not a relative path.

    Otherwise files such as ``..json`` are created, which are not just cryptic
    but also later mistaken for replay files of other templates if invoked with
    '.' and '--replay'.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call cookiecutter with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_dump = mocker.patch('cookiecutter.main.dump')
    mocker.patch('cookiecutter.main.generate_files')

    cookiecutter(
        '.',
        no_input=True,
        replay=False,
        config_file=user_config_file,
    )

    mock_replay_dump.assert_called_once_with(
        user_config_data['replay_dir'],
        'fake-repo-tmpl',
        mocker.ANY,
    )


def test_replay_load_template_name(
        monkeypatch, mocker, user_config_data, user_config_file):
    """Check that replay_load is called with a valid template_name that is
    not a relative path.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call cookiecutter with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_load = mocker.patch('cookiecutter.main.load')
    mocker.patch('cookiecutter.main.generate_files')

    cookiecutter(
        '.',
        replay=True,
        config_file=user_config_file,
    )

    mock_replay_load.assert_called_once_with(
        user_config_data['replay_dir'],
        'fake-repo-tmpl',
    )
