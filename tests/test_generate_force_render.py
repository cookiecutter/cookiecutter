"""Verify correct work of `_force_render` context option."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from cookiecutter import generate, utils


@pytest.fixture
def remove_test_dir():
    """Fixture. Remove the folder that is created by the test."""
    yield
    if os.path.exists('test_force_render'):
        utils.rmtree('test_force_render')


def _fake_is_binary_makefile(path):
    """Pretend every Makefile is binary (simulates the binaryornot false positive)."""
    return os.path.basename(path) == 'Makefile'


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_force_render_overrides_binary_detection() -> None:
    """Verify that `_force_render` forces rendering of false-positive binary files.

    We mock ``is_binary`` so the Makefile is always reported as binary,
    regardless of the platform or ``binaryornot`` version.  The
    ``_force_render`` option should override this detection and render
    the file as text.
    """
    with patch(
        'cookiecutter.generate.is_binary', side_effect=_fake_is_binary_makefile
    ):
        generate.generate_files(
            context={
                'cookiecutter': {
                    'repo_name': 'test_force_render',
                    'project_slug': 'my-project',
                    'render_test': 'I have been rendered!',
                    '_force_render': [
                        'Makefile',
                    ],
                }
            },
            repo_dir='tests/test-generate-force-render',
        )

    dir_contents = os.listdir('test_force_render')
    assert 'Makefile' in dir_contents
    assert 'README.rst' in dir_contents

    # The Makefile is reported as binary, but _force_render overrides that.
    makefile = Path('test_force_render/Makefile').read_text()
    assert 'PACKAGE_NAME := my-project' in makefile
    assert '{{ cookiecutter.project_slug }}' not in makefile

    # README.rst is not flagged as binary, should be rendered as usual.
    readme = Path('test_force_render/README.rst').read_text()
    assert 'I have been rendered!' in readme


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_force_render_with_glob_pattern() -> None:
    """Verify that `_force_render` supports glob patterns."""
    with patch(
        'cookiecutter.generate.is_binary', side_effect=_fake_is_binary_makefile
    ):
        generate.generate_files(
            context={
                'cookiecutter': {
                    'repo_name': 'test_force_render',
                    'project_slug': 'my-project',
                    'render_test': 'I have been rendered!',
                    '_force_render': [
                        'Make*',
                    ],
                }
            },
            repo_dir='tests/test-generate-force-render',
        )

    makefile = Path('test_force_render/Makefile').read_text()
    assert 'PACKAGE_NAME := my-project' in makefile
    assert '{{ cookiecutter.project_slug }}' not in makefile


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_without_force_render() -> None:
    """Verify that without `_force_render`, binary-detected files are copied as-is.

    We mock ``is_binary`` so the Makefile is always reported as binary,
    ensuring deterministic behaviour across platforms and library versions.
    """
    with patch(
        'cookiecutter.generate.is_binary', side_effect=_fake_is_binary_makefile
    ):
        generate.generate_files(
            context={
                'cookiecutter': {
                    'repo_name': 'test_force_render',
                    'project_slug': 'my-project',
                    'render_test': 'I have been rendered!',
                }
            },
            repo_dir='tests/test-generate-force-render',
        )

    # Without _force_render, the Makefile is treated as binary (mocked) and
    # copied without rendering -- the template variable stays intact.
    makefile = Path('test_force_render/Makefile').read_text()
    assert '{{ cookiecutter.project_slug }}' in makefile
