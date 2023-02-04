"""Collection of tests around cookiecutter's replay feature."""
import collections
import os
import shutil

from cookiecutter.main import cookiecutter


def test_replay_dump_template_name(
    monkeypatch, mocker, user_config_data, user_config_file
):
    """Check that replay_dump is called with a valid template_name.

    Template name must not be a relative path.

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
    monkeypatch, mocker, user_config_data, user_config_file
):
    """Check that replay_load is called correctly.

    Calls require valid template_name that is not a relative path.

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


def test_version_2_load_context_call(monkeypatch, mocker, user_config_file):
    """Check that the version 2 load_context() is called.

    Change the current working directory temporarily to
    'tests/test-generate-context-v2/min-v2-cookiecutter'
    for this test and call cookiecutter with '.' for the target template.
    """
    monkeypatch.chdir('tests/test-generate-context-v2/min-v2-cookiecutter')
    if os.path.exists('test-repo'):
        shutil.rmtree('test-repo')
    mock_replay_dump = mocker.patch('cookiecutter.main.dump')

    counts = {}

    def patch_load_context(counts):
        counts['load_context'] = 0

        def load_context(json_object, no_input=False, verbose=True, counts=counts):
            counts["load_context"] += 1
            return collections.OrderedDict(
                {
                    'repo_name': 'test-repo',
                }
            )

        return load_context

    def patch_prompt_for_config(counts):
        counts['prompt_for_config'] = 0

        def prompt_for_config(context, no_input=False):
            counts["prompt_for_config"] += 1
            return {}

    mocker.patch('cookiecutter.main.prompt_for_config', patch_prompt_for_config(counts))
    mocker.patch('cookiecutter.main.load_context', patch_load_context(counts))

    cookiecutter(
        '.',
        no_input=True,
        replay=False,
        config_file=user_config_file,
    )

    if os.path.exists('test-repo'):
        shutil.rmtree('test-repo')
    assert mock_replay_dump.call_count == 1
    assert counts["load_context"] == 1
    assert counts["prompt_for_config"] == 0


def test_custom_replay_file(monkeypatch, mocker, user_config_file):
    """Check that reply.load is called with the custom replay_file."""
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_load = mocker.patch('cookiecutter.main.load')
    mocker.patch('cookiecutter.main.generate_files')

    cookiecutter(
        '.',
        replay='./custom-replay-file',
        config_file=user_config_file,
    )

    mock_replay_load.assert_called_once_with(
        '.',
        'custom-replay-file',
    )
