"""Tests for `cookiecutter.find` module."""

from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest

from cookiecutter import find
from cookiecutter.exceptions import NonTemplatedInputDirException
from cookiecutter.utils import create_env_with_context


@pytest.fixture(params=['fake-repo-pre', 'fake-repo-pre2'])
def repo_dir(request):
    """Fixture returning path for `test_find_template` test."""
    return Path('tests', request.param)


@pytest.fixture()
def env(context):
    """Fixture return the env generated from context."""
    return create_env_with_context(context)


@pytest.mark.parametrize(
    "repo_name,context,error_expectation,expected",
    [
        ("fake-repo-pre", {}, does_not_raise(), '{{cookiecutter.repo_name}}'),
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
            does_not_raise(),
            '{%{cookiecutter.repo_name}%}',
        ),
        (
            "fake-repo-pre",
            {
                'cookiecutter': {
                    '_jinja2_env_vars': {
                        'variable_start_string': '{%{',
                        'variable_end_string': '}%}',
                    }
                }
            },
            pytest.raises(NonTemplatedInputDirException),
            None,
        ),
        ("fake-repo-bad", {}, pytest.raises(NonTemplatedInputDirException), None),
    ],
    ids=[
        'template with default jinja strings',
        'template with custom jinja strings',
        'template with custom jinja strings but folder with default jinja strings',
        'template missing folder',
    ],
)
def test_find_template(repo_name, env, error_expectation, expected) -> None:
    """Verify correctness of `find.find_template` path detection."""
    repo_dir = Path('tests', repo_name)

    with error_expectation:
        template = find.find_template(repo_dir, env)

        test_dir = Path(repo_dir, expected)
        assert template == test_dir
