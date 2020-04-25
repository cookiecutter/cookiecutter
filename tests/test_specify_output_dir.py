# -*- coding: utf-8 -*-

"""Tests for cookiecutter's output directory customization feature."""

import pytest

from cookiecutter import main


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a cookiecutter.json."""
    return {
        u'cookiecutter': {
            u'email': u'raphael@hackebrot.de',
            u'full_name': u'Raphael Pierzina',
            u'github_username': u'hackebrot',
            u'version': u'0.1.0',
        }
    }


@pytest.fixture
def output_dir(tmpdir):
    """Fixture to prepare test output directory."""
    return str(tmpdir.mkdir('output'))


@pytest.fixture
def template(tmpdir):
    """Fixture to prepare test template directory."""
    template_dir = tmpdir.mkdir('template')
    template_dir.join('cookiecutter.json').ensure(file=True)
    return str(template_dir)


@pytest.fixture(autouse=True)
def mock_gen_context(mocker, context):
    """Fixture. Automatically mock cookiecutter's function with expected output."""
    mocker.patch('cookiecutter.main.generate_context', return_value=context)


@pytest.fixture(autouse=True)
def mock_prompt(mocker):
    """Fixture. Automatically mock cookiecutter's function with expected output."""
    mocker.patch('cookiecutter.main.prompt_for_config')


@pytest.fixture(autouse=True)
def mock_replay(mocker):
    """Fixture. Automatically mock cookiecutter's function with expected output."""
    mocker.patch('cookiecutter.main.dump')


def test_api_invocation(mocker, template, output_dir, context):
    """Verify output dir location is correctly passed."""
    mock_gen_files = mocker.patch('cookiecutter.main.generate_files')

    main.cookiecutter(template, output_dir=output_dir)

    mock_gen_files.assert_called_once_with(
        repo_dir=template,
        context=context,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
        output_dir=output_dir,
    )


def test_default_output_dir(mocker, template, context):
    """Verify default output dir is current working folder."""
    mock_gen_files = mocker.patch('cookiecutter.main.generate_files')

    main.cookiecutter(template)

    mock_gen_files.assert_called_once_with(
        repo_dir=template,
        context=context,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
        output_dir='.',
    )
