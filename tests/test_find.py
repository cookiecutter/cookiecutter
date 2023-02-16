"""Tests for `cookiecutter.find` module."""
from pathlib import Path

import pytest

from cookiecutter import find


@pytest.fixture(params=['fake-repo-pre', 'fake-repo-pre2'])
def repo_dir(request):
    """Fixture returning path for `test_find_templates` test."""
    return Path('tests', request.param)


def test_find_template(repo_dir):
    """Verify correctness of `find.find_templates` path detection."""
    templates = find.find_templates(repo_dir=repo_dir)

    test_dir = Path(repo_dir, '{{cookiecutter.repo_name}}')
    assert test_dir in templates
