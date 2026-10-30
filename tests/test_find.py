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


@pytest.mark.parametrize('start,end', [('{{', '}}'), ('{%{', '}%}')])
@pytest.mark.parametrize('has_directory', [False, True])
def test_find_template_ignores_matching_files(
    tmp_path, mocker, start, end, has_directory
):
    """Only directories can be selected as the project template."""
    name = f'{start}cookiecutter.repo_name{end}'
    matching_file = tmp_path / f'{name}.txt'
    matching_file.write_text('Not a project directory', encoding='utf-8')
    entries = [matching_file.name]
    if has_directory:
        (tmp_path / name).mkdir()
        entries.append(name)
    # A matching file must not hide a valid directory later in the listing.
    mocker.patch('cookiecutter.find.os.listdir', return_value=entries)
    env = create_env_with_context(
        {
            'cookiecutter': {
                '_jinja2_env_vars': {
                    'variable_start_string': start,
                    'variable_end_string': end,
                }
            }
        }
    )
    if has_directory:
        assert find.find_template(tmp_path, env) == tmp_path / name
    else:
        with pytest.raises(NonTemplatedInputDirException):
            find.find_template(tmp_path, env)
