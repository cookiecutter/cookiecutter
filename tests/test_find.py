"""Tests for `cookiecutter.find` module."""
from pathlib import Path

import pytest

from cookiecutter import find
from pymonad.effects import IO

@pytest.fixture
def mock_logger(mocker):
    """Fixture to mock the logger."""
    return mocker.patch("cookiecutter.find.logger")

@pytest.fixture(params=['fake-repo-pre', 'fake-repo-pre2'])
def repo_dir(request):
    """Fixture returning path for `test_find_template` test."""
    return Path('tests', request.param)


def test_find_template(repo_dir):
    """Verify correctness of `find.find_template` path detection."""
    effect = find.find_template(repo_dir=repo_dir)
    template = effect.run()[1]  # Get the second element of the result tuple

    test_dir = Path(repo_dir, '{{cookiecutter.repo_name}}')
    assert template == test_dir

def test_find_template_logging(repo_dir, mock_logger):
    """Verify the logging behavior of `find.find_template`."""
    effect = find.find_template(repo_dir=repo_dir)
    result = effect.run()

    assert result[1] == repo_dir / "{{cookiecutter.repo_name}}"
    mock_logger.debug.assert_called_once_with(
        "Searching %s for the project template.", repo_dir
    )
    mock_logger.debug.assert_called_with(
        "The project template appears to be %s", repo_dir / "{{cookiecutter.repo_name}}"
    )