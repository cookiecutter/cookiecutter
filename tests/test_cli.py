import os
import pytest

from click.testing import CliRunner

from cookiecutter.cli import main
from cookiecutter.main import cookiecutter
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
    """Create a fake project to be overwritten in the according tests."""
    os.makedirs('fake-project')


@pytest.fixture(params=['-V', '--version'])
def version_cli_flag(request):
    return request.param


def test_cli_version(version_cli_flag):
    result = runner.invoke(main, [version_cli_flag])
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


@pytest.mark.usefixtures('remove_fake_project_dir')
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
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=True,
        overwrite_if_exists=False,
        output_dir='.'
    )


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_exit_on_noinput_and_replay(mocker):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter',
        side_effect=cookiecutter
    )

    template_path = 'tests/fake-repo-pre/'
    result = runner.invoke(main, [
        template_path,
        '--no-input',
        '--replay',
        '-v'
    ])

    assert result.exit_code == 1

    expected_error_msg = (
        "You can not use both replay and no_input or extra_context "
        "at the same time."
    )

    assert expected_error_msg in result.output

    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        True,
        replay=True,
        overwrite_if_exists=False,
        output_dir='.'
    )


@pytest.fixture(params=['-f', '--overwrite-if-exists'])
def overwrite_cli_flag(request):
    return request.param


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_run_cookiecutter_on_overwrite_if_exists_and_replay(
        mocker, overwrite_cli_flag):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter',
        side_effect=cookiecutter
    )

    template_path = 'tests/fake-repo-pre/'
    result = runner.invoke(main, [
        template_path,
        '--replay',
        '-v',
        overwrite_cli_flag,
    ])

    assert result.exit_code == 0

    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=True,
        overwrite_if_exists=True,
        output_dir='.'
    )


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_overwrite_if_exists_when_output_dir_does_not_exist(
        overwrite_cli_flag):
    result = runner.invoke(main, [
        'tests/fake-repo-pre/', '--no-input', overwrite_cli_flag
    ])

    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.mark.usefixtures('make_fake_project_dir', 'remove_fake_project_dir')
def test_cli_overwrite_if_exists_when_output_dir_exists(overwrite_cli_flag):
    result = runner.invoke(main, [
        'tests/fake-repo-pre/', '--no-input', overwrite_cli_flag
    ])

    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.fixture(params=['-o', '--output-dir'])
def output_dir_flag(request):
    return request.param


@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir.mkdir('output'))


def test_cli_output_dir(mocker, output_dir_flag, output_dir):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = runner.invoke(main, [
        template_path,
        output_dir_flag,
        output_dir
    ])

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir=output_dir
    )
