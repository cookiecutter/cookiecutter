import os

from click.testing import CliRunner

from cookiecutter.cli import main

runner = CliRunner()


def test_cli_version():
    result = runner.invoke(main, ['-V'])
    assert result.exit_code == 0
    assert result.output.startswith('Cookiecutter')


def test_cli():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')


def test_cli_verbose():
    result = runner.invoke(main, ['tests/fake-repo-pre/', '--no-input', '-v'])
    assert result.exit_code == 0
    assert os.path.isdir('fake-project')
