# -*- coding: utf-8 -*-
from cookiecutter.main import cookiecutter


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


def test_version_2_load_context_call(
        monkeypatch, mocker, user_config_file):
    """Check that the version 2 load_context() is called.

    Change the current working directory temporarily to
    'tests/test-generate-context-v2/min-v2-cookiecutter'
    for this test and call cookiecutter with '.' for the target template.
    """
    monkeypatch.chdir('tests/test-generate-context-v2/min-v2-cookiecutter')

    mock_replay_dump = mocker.patch('cookiecutter.main.dump')

    mock_version_1_prompt_for_config = mocker.patch(
                                    'cookiecutter.main.prompt_for_config')
    mock_version_2_load_context = mocker.patch(
                                    'cookiecutter.main.load_context')

    mocker.patch('cookiecutter.main.generate_files')

    cookiecutter(
        '.',
        no_input=True,
        replay=False,
        config_file=user_config_file,
    )

    assert mock_version_1_prompt_for_config.call_count == 0
    assert mock_version_2_load_context.call_count == 1
    assert mock_replay_dump.call_count == 1
