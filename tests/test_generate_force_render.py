"""Verify correct work of `_force_render` context option."""

import os
from pathlib import Path

import pytest

from cookiecutter import generate, utils


@pytest.fixture
def remove_test_dir():
    """Fixture. Remove the folder that is created by the test."""
    yield
    if os.path.exists('test_force_render'):
        utils.rmtree('test_force_render')


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_force_render_overrides_binary_detection() -> None:
    """Verify that `_force_render` forces rendering of false-positive binary files.

    Files starting with ``PACK`` (e.g. ``PACKAGE_NAME := ...``) are
    misclassified as binary by the ``binaryornot`` library.  The
    ``_force_render`` option should override this detection and render
    the file as text.
    """
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

    # The Makefile starts with "PACK..." which triggers false binary detection.
    # With _force_render, it should be rendered as text.
    makefile = Path('test_force_render/Makefile').read_text()
    assert 'PACKAGE_NAME := my-project' in makefile
    assert '{{ cookiecutter.project_slug }}' not in makefile

    # README.rst is a normal text file, should be rendered as usual.
    readme = Path('test_force_render/README.rst').read_text()
    assert 'I have been rendered!' in readme


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_force_render_with_glob_pattern() -> None:
    """Verify that `_force_render` supports glob patterns."""
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
    """Verify that without `_force_render`, binary-detected files are copied as-is."""
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

    # Without _force_render, the Makefile that starts with PACK may be
    # copied as binary (unrendered) due to binaryornot false positive.
    makefile = Path('test_force_render/Makefile').read_text()
    # The template variable should NOT have been rendered
    assert '{{ cookiecutter.project_slug }}' in makefile
