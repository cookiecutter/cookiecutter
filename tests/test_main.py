# -*- coding: utf-8 -*-

import os

import pytest

from cookiecutter.main import cookiecutter
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

@pytest.skip
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
