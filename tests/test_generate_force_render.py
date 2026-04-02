"""Verify correct work of `_force_render` context option."""

import os
from pathlib import Path

import pytest

from cookiecutter import generate, utils
from cookiecutter.generate import is_force_render_path

# ---------------------------------------------------------------------------
# Unit tests for is_force_render_path helper
# ---------------------------------------------------------------------------


def test_is_force_render_path_matches_pattern():
    """Return True when path matches a pattern in _force_render."""
    context = {'cookiecutter': {'_force_render': ['Makefile', '*.mk']}}
    assert is_force_render_path('Makefile', context) is True
    assert is_force_render_path('build.mk', context) is True


def test_is_force_render_path_no_match():
    """Return False when path does not match any _force_render pattern."""
    context = {'cookiecutter': {'_force_render': ['Makefile']}}
    assert is_force_render_path('README.rst', context) is False


def test_is_force_render_path_missing_key():
    """Return False when _force_render key is absent from context."""
    context = {'cookiecutter': {}}
    assert is_force_render_path('Makefile', context) is False


def test_is_force_render_path_empty_list():
    """Return False when _force_render list is empty."""
    context = {'cookiecutter': {'_force_render': []}}
    assert is_force_render_path('Makefile', context) is False


# ---------------------------------------------------------------------------
# Integration test: a file falsely detected as binary must still be rendered
# when listed in _force_render
# ---------------------------------------------------------------------------


@pytest.fixture
def remove_test_dir():
    """Remove the generated project directory after each test."""
    yield
    if os.path.exists('test_force_render'):
        utils.rmtree('test_force_render')


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_force_render_renders_false_binary_file() -> None:
    """_force_render causes a file detected as binary to be Jinja-rendered.

    The template contains a ``Makefile`` whose first word is ``PACKAGE_NAME``
    (starts with ``PACK``).  The ``binaryornot`` library misclassifies such
    files as binary (they look like git packfiles) and cookiecutter would
    normally copy them verbatim.  With ``_force_render`` the file must be
    rendered as a Jinja2 template.
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_force_render',
                'project_slug': 'my_project',
                '_force_render': ['Makefile'],
            }
        },
        repo_dir='tests/test-generate-force-render',
    )

    # README.rst is a normal text file; it should always be rendered.
    readme = Path('test_force_render/README.rst').read_text()
    assert 'my_project' in readme

    # Makefile starts with PACKAGE_NAME (PACK…), so binaryornot marks it as
    # binary. Without _force_render the template variable would not be
    # expanded. With _force_render it must be rendered.
    makefile = Path('test_force_render/Makefile').read_text()
    assert 'my_project' in makefile
    assert '{{' not in makefile
