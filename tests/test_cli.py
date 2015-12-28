import functools
import os
import json
import pytest

from click.testing import CliRunner

from cookiecutter.cli import main





# @pytest.fixture
# def remove_fake_project_dir(request):
#     """
#     Remove the fake project directory created during the tests.
#     """
#     def fin_remove_fake_project_dir():
#         if os.path.isdir('fake-project'):
#             utils.rmtree('fake-project')
#     request.addfinalizer(fin_remove_fake_project_dir)
#
#
# @pytest.fixture
# def make_fake_project_dir(request):
#     """Create a fake project to be overwritten in the according tests."""
#     os.makedirs('fake-project')
from tests.utils import dir_tests


@pytest.fixture
def user_config_path(tmpdir):
    return str(tmpdir.join('home', '.cookiecutterrc'))


@pytest.fixture
def fake_project(tmpdir):
    os.chdir(str(tmpdir))
    tmpdir.mkdir('fake-project')

@pytest.fixture
def runner(monkeypatch):
    env_home = {'HOME': os.environ['HOME']}
    _runner = CliRunner(env=env_home)
    _invoke = functools.partial(_runner.invoke, env=env_home)
    monkeypatch.setattr(_runner, 'invoke', _invoke)
    return _runner


@pytest.fixture(params=['-V', '--version'])
def version_cli_flag(request):
    return request.param


def test_cli_version(version_cli_flag, runner):
    result = runner.invoke(main, [version_cli_flag])
    assert result.exit_code == 0
    assert result.output.startswith('Cookiecutter')


@pytest.mark.usefixtures('fake_project')
def test_cli_error_on_existing_output_directory( runner):
    result = runner.invoke(main, [dir_tests('fake-repo-pre'), '--no-input'])
    assert result.exit_code != 0
    expected_error_msg = 'Error: "fake-project" directory already exists\n'
    assert result.output == expected_error_msg


def test_cli( runner):
    result = runner.invoke(main, [dir_tests('fake-repo-pre'), '--no-input'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


def test_cli_verbose( runner):
    result = runner.invoke(main, [dir_tests('fake-repo-pre'), '--no-input', '-v'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')

def test_cli_replay(mocker, runner, user_config_path):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = dir_tests('fake-repo-pre')
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
        output_dir='.',
        config_file=user_config_path
    )


def test_cli_exit_on_noinput_and_replay(mocker, runner, user_config_path):
    from cookiecutter.main import cookiecutter

    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter',
        side_effect=cookiecutter
    )

    template_path = dir_tests('fake-repo-pre')
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
        output_dir='.',
        config_file=user_config_path
    )


@pytest.fixture(params=['-f', '--overwrite-if-exists'])
def overwrite_cli_flag(request):
    return request.param

@pytest.mark.xfail
@pytest.mark.usefixtures('fake_project')
def test_run_cookiecutter_on_overwrite_if_exists_and_replay(
        mocker, overwrite_cli_flag, runner, user_config_path, tmpdir):
    from cookiecutter.main import cookiecutter

    assert os.path.isdir(dir_tests('fake-repo-pre'))
    assert os.path.isdir(str(tmpdir.join('fake-project')))

    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter',
        side_effect=cookiecutter
    )

    template_path = dir_tests('fake-repo-pre')
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
        output_dir='.',
        config_file=user_config_path
    )


def test_cli_overwrite_if_exists_when_output_dir_does_not_exist(
        overwrite_cli_flag, runner, tmpdir):
    result = runner.invoke(main, [
        dir_tests('fake-repo-pre'), '--no-input', overwrite_cli_flag
    ])

    assert result.exit_code == 0
    expected_output_dir = str(tmpdir.join('fake-project'))
    assert os.path.isdir(expected_output_dir)


@pytest.mark.usefixtures('fake_project')
def test_cli_overwrite_if_exists_when_output_dir_exists(overwrite_cli_flag, runner, tmpdir):
    result = runner.invoke(main, [
        dir_tests('fake-repo-pre'), '--no-input', overwrite_cli_flag
    ])

    assert result.exit_code == 0
    expected_output_dir = str(tmpdir.join('fake-project'))
    assert os.path.isdir(expected_output_dir)


@pytest.fixture(params=['-o', '--output-dir'])
def output_dir_flag(request):
    return request.param


@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir.mkdir('output'))


def test_cli_output_dir(mocker, output_dir_flag, output_dir, runner, user_config_path):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = dir_tests('fake-repo-pre/')
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
        output_dir=output_dir,
        config_file=user_config_path
    )


@pytest.fixture(params=['-h', '--help', 'help'])
def help_cli_flag(request):
    return request.param


def test_cli_help(help_cli_flag, runner):
    result = runner.invoke(main, [help_cli_flag])
    assert result.exit_code == 0
    assert result.output.startswith('Usage')


def test_user_config(mocker, runner):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = dir_tests('fake-repo-pre/')
    result = runner.invoke(main, [
        template_path,
        '--config-file',
        dir_tests('config.yaml')
    ])

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=dir_tests('config.yaml')
    )


def test_default_user_config_overwrite(mocker, runner):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = dir_tests('fake-repo-pre/')
    result = runner.invoke(main, [
        template_path,
        '--config-file',
        dir_tests('config.yaml'),
        '--default-config'
    ])

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=None
    )


def test_default_user_config(mocker, runner):
    mock_cookiecutter = mocker.patch(
        'cookiecutter.cli.cookiecutter'
    )

    template_path = dir_tests('fake-repo-pre/')
    result = runner.invoke(main, [
        template_path,
        '--default-config'
    ])

    assert result.exit_code == 0
    mock_cookiecutter.assert_called_once_with(
        template_path,
        None,
        False,
        replay=False,
        overwrite_if_exists=False,
        output_dir='.',
        config_file=None
    )


def test_echo_undefined_variable_error(tmpdir, runner):
    output_dir = str(tmpdir.mkdir('output'))
    template_path = dir_tests('undefined-variable/file-name/')

    result = runner.invoke(main, [
        '--no-input',
        '--default-config',
        '--output-dir',
        output_dir,
        template_path,
    ])

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
