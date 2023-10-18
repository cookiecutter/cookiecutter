"""Tests for `cookiecutter.find` module."""
from pathlib import Path

import pytest

from cookiecutter import find


@pytest.fixture(params=['fake-repo-pre', 'fake-repo-pre2'])
def repo_dir(request):
    """Fixture returning path for `test_find_template` test."""
    return Path('tests', request.param)


@pytest.mark.parametrize(
    "repo_name,context,expected",
    [
        ("fake-repo-pre", {}, '{{cookiecutter.repo_name}}'),
        (
            "fake-repo-pre2",
            {
                'cookiecutter': {
                    '_jinja2_env_vars': {
                        'variable_start_string': '{%{',
                        'variable_end_string': '}%}',
                    }
                }
            },
            '{%{cookiecutter.repo_name}%}',
        ),
    ],
)
def test_find_template(repo_name, context, expected):
    """Verify correctness of `find.find_template` path detection."""
    repo_dir = Path('tests', repo_name)

    template = find.find_template(repo_dir, context)

    test_dir = Path(repo_dir, expected)
    assert template == test_dir
