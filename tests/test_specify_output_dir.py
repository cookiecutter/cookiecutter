"""Tests for cookiecutter's output directory customization feature."""

import pytest

from cookiecutter import main


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a cookiecutter.json."""
    return {
        'cookiecutter': {
            'email': 'raphael@hackebrot.de',
            'full_name': 'Raphael Pierzina',
            'github_username': 'hackebrot',
            'version': '0.1.0',
        }
    }


@pytest.fixture
def template(tmp_path):
    """Fixture to prepare test template directory."""
    template_dir = tmp_path.joinpath("template")
    template_dir.mkdir()
    template_dir.joinpath('cookiecutter.json').touch()
    return str(template_dir)


@pytest.fixture(autouse=True)
def mock_gen_context(mocker, context) -> None:
    """Fixture. Automatically mock cookiecutter's function with expected output."""
    mocker.patch('cookiecutter.main.generate_context', return_value=context)


@pytest.fixture(autouse=True)
def mock_prompt(mocker) -> None:
    """Fixture. Automatically mock cookiecutter's function with expected output."""
    mocker.patch('cookiecutter.main.prompt_for_config')


@pytest.fixture(autouse=True)
def mock_replay(mocker) -> None:
    """Fixture. Automatically mock cookiecutter's function with expected output."""
    mocker.patch('cookiecutter.main.dump')


def test_api_invocation(mocker, template, output_dir, context) -> None:
    """Verify output dir location is correctly passed."""
    mock_gen_files = mocker.patch('cookiecutter.main.generate_files')

    main.cookiecutter(template, output_dir=output_dir)

    mock_gen_files.assert_called_once_with(
        repo_dir=template,
        context=context,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
        output_dir=output_dir,
        accept_hooks=True,
        keep_project_on_failure=False,
    )


def test_default_output_dir(mocker, template, context) -> None:
    """Verify default output dir is current working folder."""
    mock_gen_files = mocker.patch('cookiecutter.main.generate_files')

    main.cookiecutter(template)

    mock_gen_files.assert_called_once_with(
        repo_dir=template,
        context=context,
        overwrite_if_exists=False,
        skip_if_file_exists=False,
        output_dir='.',
        accept_hooks=True,
        keep_project_on_failure=False,
    )
