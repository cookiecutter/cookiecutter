"""Tests for `cookiecutter.find` module."""
from pathlib import Path

import pytest

from cookiecutter import find


@pytest.fixture(params=['fake-multi-repo-dir'])
def repo_dir(request):
    """Fixture returning path for `test_find_template` test."""
    return Path('tests', request.param)


def test_find_templates(repo_dir):
    """Verify correctness of `find.find_templates` path detection."""
    templates = find.find_templates(repo_dir=repo_dir)

    test_dirs = [
        Path(repo_dir, '{{cookiecutter.repo_name}}'),
        Path(repo_dir, '{{cookiecutter.other_repo_name}}'),
    ]
    assert all([test_dir in templates for test_dir in test_dirs])
