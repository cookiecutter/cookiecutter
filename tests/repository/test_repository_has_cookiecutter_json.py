"""Tests for `repository_has_cookiecutter_json` function."""

import pytest

from cookiecutter.repository import repository_has_cookiecutter_json


def test_valid_repository() -> None:
    """Validate correct response if `cookiecutter.json` file exist."""
    assert repository_has_cookiecutter_json('tests/fake-repo')


@pytest.mark.parametrize(
    'invalid_repository', (['tests/fake-repo-bad', 'tests/unknown-repo'])
)
def test_invalid_repository(invalid_repository) -> None:
    """Validate correct response if `cookiecutter.json` file not exist."""
    assert not repository_has_cookiecutter_json(invalid_repository)
