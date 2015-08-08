import os
import pytest

from click.testing import CliRunner

from cookiecutter.cli import main
from cookiecutter import utils

runner = CliRunner()


@pytest.fixture
def remove_fake_project_dir(request):
    """
    Remove the fake project directory created during the tests.
    """
    def fin_remove_fake_project_dir():
        if os.path.isdir('fake-project'):
            utils.rmtree('fake-project')
    request.addfinalizer(fin_remove_fake_project_dir)


@pytest.fixture
def make_fake_project_dir(request):
    """
    Create the fake project directory created during the tests.
    """
    if not os.path.isdir('fake-project'):
        os.makedirs('fake-project')


def test_cli_version():
    result = runner.invoke(main, ['-V'])
    assert result.exit_code == 0
    assert result.output.startswith('Cookiecutter')


@pytest.mark.usefixtures('make_fake_project_dir', 'remove_fake_project_dir')
def test_cli_error_on_existing_output_directory():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input'])
    assert result.exit_code != 0
    expected_error_msg = 'Error: "fake-project" directory already exists\n'
    assert result.output == expected_error_msg


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_verbose():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input', '-v'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


def test_cli_replay(mocker):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = runner.invoke(main, [
        template_path,
        '--replay',
        '-v'
    ])

    assert result.exit_code == 0
    mock_cookiecutter.assert_once_called_with(
        template_path,
        None,
        False,
        True
    )


def test_cli_exit_on_noinput_and_replay(capsys, mocker):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = runner.invoke(main, [
        template_path,
        '--no-input',
        '--replay',
        '-v'
    ])

    mock_cookiecutter.assert_once_called_with(
        template_path,
        None,
        True,
        True
    )

    assert result.exit_code == 1

    out, err = capsys.readouterr()
    expected_error_msg = (
        "You can not use both --no-input and --replay at the same time!"
    )
    assert expected_error_msg in out
