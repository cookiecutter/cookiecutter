"""Collection of tests around cookiecutter's replay feature."""

from pathlib import Path

import pytest

from cookiecutter.main import cookiecutter


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


@pytest.mark.parametrize(
    'url',
    [
        'https://example.com/template.zip?download=1',
        'http://example.com/template.zip#template',
        'https://example.com/template.zip?token=a/b#section/c',
    ],
)
def test_cookiecutter_zip_url(mocker, url, user_config_file, output_dir) -> None:
    """Generate a project from a ZIP URL with a query or fragment."""
    response = mocker.Mock()
    response.iter_content.return_value = [
        Path('tests/files/fake-repo-tmpl.zip').read_bytes()
    ]
    get = mocker.patch(
        'cookiecutter.zipfile.requests.get', return_value=response, autospec=True
    )

    project = cookiecutter(
        url, no_input=True, config_file=user_config_file, output_dir=output_dir
    )

    assert Path(project).name == 'fake-project-templated'
    readme = (Path(project) / 'README.rst').read_text()
    assert 'Fake Project' in readme
    get.assert_called_once_with(url, stream=True, timeout=100)
