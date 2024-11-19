"""Collection of tests around cookiecutter's replay feature."""

import sys 

from cookiecutter.main import cookiecutter

from cookiecutter.main import _patch_import_path_for_repo



def test_original_cookiecutter_options_preserved_in__cookiecutter(
    monkeypatch,
    mocker,
    user_config_file,
) -> None:
    """Preserve original context options.

    Tests you can access the original context options via
    `context['_cookiecutter']`.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl-_cookiecutter')
    mock_generate_files = mocker.patch('cookiecutter.main.generate_files')
    cookiecutter(
        '.',
        no_input=True,
        replay=False,
        config_file=user_config_file,
    )
    assert mock_generate_files.call_args[1]['context']['_cookiecutter'][
        'test_list'
    ] == [1, 2, 3, 4]
    assert mock_generate_files.call_args[1]['context']['_cookiecutter'][
        'test_dict'
    ] == {"foo": "bar"}


def test_replay_dump_template_name(
    monkeypatch, mocker, user_config_data, user_config_file
) -> None:
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
) -> None:
    """Check that replay_load is called correctly.

    Calls require valid template_name that is not a relative path.

    Change the current working directory temporarily to 'tests/fake-repo-tmpl'
    for this test and call cookiecutter with '.' for the target template.
    """
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_load = mocker.patch('cookiecutter.main.load')
    mocker.patch('cookiecutter.main.generate_context').return_value = {
        'cookiecutter': {}
    }
    mocker.patch('cookiecutter.main.generate_files')
    mocker.patch('cookiecutter.main.dump')

    cookiecutter(
        '.',
        replay=True,
        config_file=user_config_file,
    )

    mock_replay_load.assert_called_once_with(
        user_config_data['replay_dir'],
        'fake-repo-tmpl',
    )


def test_custom_replay_file(monkeypatch, mocker, user_config_file) -> None:
    """Check that reply.load is called with the custom replay_file."""
    monkeypatch.chdir('tests/fake-repo-tmpl')

    mock_replay_load = mocker.patch('cookiecutter.main.load')
    mocker.patch('cookiecutter.main.generate_context').return_value = {
        'cookiecutter': {}
    }
    mocker.patch('cookiecutter.main.generate_files')
    mocker.patch('cookiecutter.main.dump')

    cookiecutter(
        '.',
        replay='./custom-replay-file',
        config_file=user_config_file,
    )

    mock_replay_load.assert_called_once_with(
        '.',
        'custom-replay-file',
    )

def test_patch_import_path_for_repo():
    """Test the _patch_import_path_for_repo context manager."""
    original_sys_path = sys.path[:]
    repo_dir = '/fake/repo/path'

    with _patch_import_path_for_repo(repo_dir):
        assert sys.path[-1] == repo_dir

    assert sys.path == original_sys_path


