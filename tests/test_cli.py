# -*- coding: utf-8 -*-

import os
import json

from click.testing import CliRunner
import pytest

from cookiecutter.__main__ import main
from cookiecutter.main import cookiecutter
from cookiecutter import utils, config


@pytest.fixture(scope='session')
def cli_runner():
    """Fixture that returns a helper function to run the cookiecutter cli."""
    runner = CliRunner()

    def cli_main(*cli_args):
        """Run cookiecutter cli main with the given args."""
        return runner.invoke(main, cli_args)

    return cli_main


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


def test_cli_version(cli_runner, version_cli_flag):
    result = cli_runner(version_cli_flag)
    assert result.exit_code == 0
    assert result.output.startswith('Cookiecutter')


@pytest.mark.usefixtures('make_fake_project_dir', 'remove_fake_project_dir')
def test_cli_error_on_existing_output_directory(cli_runner):
    result = cli_runner('tests/fake-repo-pre/', '--no-input')
    assert result.exit_code != 0
    expected_error_msg = 'Error: "fake-project" directory already exists\n'
    assert result.output == expected_error_msg


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli(cli_runner):
    result = cli_runner('tests/fake-repo-pre/', '--no-input')
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')
    with open(os.path.join('fake-project', 'README.rst')) as f:
        assert 'Project name: **Fake Project**' in f.read()


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_verbose(cli_runner):
    result = cli_runner('tests/fake-repo-pre/', '--no-input', '-v')
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')
    with open(os.path.join('fake-project', 'README.rst')) as f:
        assert 'Project name: **Fake Project**' in f.read()


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_replay(mocker, cli_runner):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(template_path, '--replay', '-v')

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=True,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=config.USER_CONFIG_PATH,
        extra_context=None
    )


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_exit_on_noinput_and_replay(mocker, cli_runner):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter',
        side_effect=cookiecutter
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(template_path, '--no-input', '--replay', '-v')

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
        output_dir='.',
        config_file=config.USER_CONFIG_PATH,
        extra_context=None
    )


@pytest.fixture(params=['-f', '--overwrite-if-exists'])
def overwrite_cli_flag(request):
    return request.param


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_run_cookiecutter_on_overwrite_if_exists_and_replay(
        mocker, cli_runner, overwrite_cli_flag):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter',
        side_effect=cookiecutter
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(template_path, '--replay', '-v', overwrite_cli_flag)

    assert result.exit_code == 0

    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=True,
        overwrite_if_exists=True,
        output_dir='.',
        config_file=config.USER_CONFIG_PATH,
        extra_context=None
    )


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_overwrite_if_exists_when_output_dir_does_not_exist(
        cli_runner, overwrite_cli_flag):

    result = cli_runner(
        'tests/fake-repo-pre/',
        '--no-input',
        overwrite_cli_flag,
    )

    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.mark.usefixtures('make_fake_project_dir', 'remove_fake_project_dir')
def test_cli_overwrite_if_exists_when_output_dir_exists(
        cli_runner, overwrite_cli_flag):

    result = cli_runner(
        'tests/fake-repo-pre/',
        '--no-input',
        overwrite_cli_flag,
    )
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


@pytest.fixture(params=['-o', '--output-dir'])
def output_dir_flag(request):
    return request.param


@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir.mkdir('output'))


def test_cli_output_dir(mocker, cli_runner, output_dir_flag, output_dir):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(template_path, output_dir_flag, output_dir)

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir=output_dir,
        config_file=config.USER_CONFIG_PATH,
        extra_context=None
    )


@pytest.fixture(params=['-h', '--help', 'help'])
def help_cli_flag(request):
    return request.param


def test_cli_help(cli_runner, help_cli_flag):
    result = cli_runner(help_cli_flag)
    assert result.exit_code == 0
    assert result.output.startswith('Usage')


@pytest.fixture
def user_config_path(tmpdir):
    return str(tmpdir.join('tests/config.yaml'))


def test_user_config(mocker, cli_runner, user_config_path):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(template_path, '--config-file', user_config_path)

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=user_config_path,
        extra_context=None
    )


def test_default_user_config_overwrite(mocker, cli_runner, user_config_path):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(
        template_path,
        '--config-file',
        user_config_path,
        '--default-config',
    )

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=None,
        extra_context=None
    )


def test_default_user_config(mocker, cli_runner):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = 'tests/fake-repo-pre/'
    result = cli_runner(template_path, '--default-config')

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=None,
        extra_context=None
    )


def test_echo_undefined_variable_error(tmpdir, cli_runner):
    output_dir = str(tmpdir.mkdir('output'))
    template_path = 'tests/undefined-variable/file-name/'

    result = cli_runner(
        '--no-input',
        '--default-config',
        '--output-dir',
        output_dir,
        template_path,
    )

    assert result.exit_code == 1

    error = "Unable to create file '{{cookiecutter.foobar}}'"
    assert error in result.output

    message = "Error message: 'dict object' has no attribute 'foobar'"
    assert message in result.output

    context = {
        'cookiecutter': {
            'github_username': 'hackebrot',
            'project_slug': 'testproject'
        }
    }
    context_str = json.dumps(context, indent=4, sort_keys=True)
    assert context_str in result.output


def test_echo_unknown_extension_error(tmpdir, cli_runner):
    output_dir = str(tmpdir.mkdir('output'))
    template_path = 'tests/test-extensions/unknown/'

    result = cli_runner(
        '--no-input',
        '--default-config',
        '--output-dir',
        output_dir,
        template_path,
    )

    assert result.exit_code == 1

    assert 'Unable to load extension: ' in result.output


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_extra_context(cli_runner):
    result = cli_runner(
        'tests/fake-repo-pre/',
        '--no-input',
        '-v',
        'project_name=Awesomez',
    )
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')
    with open(os.path.join('fake-project', 'README.rst')) as f:
        assert 'Project name: **Awesomez**' in f.read()


@pytest.mark.usefixtures('remove_fake_project_dir')
def test_cli_extra_context_invalid_format(cli_runner):
    result = cli_runner(
        'tests/fake-repo-pre/',
        '--no-input',
        '-v',
        'ExtraContextWithNoEqualsSoInvalid',
    )
    assert result.exit_code == 2
    assert 'Error: Invalid value for "extra_context"' in result.output
    assert 'should contain items of the form key=value' in result.output
