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
    """Verify `_force_render` overrides binary detection.

    Files that are detected as binary (e.g. starting with "PACK")
    should still be rendered when matched by a `_force_render` pattern.
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_force_render',
                'project_slug': 'example-package',
                'render_test': 'I have been rendered!',
                '_force_render': [
                    'PACKAGE_NAME',
                ],
            }
        },
        repo_dir='tests/test-generate-force-render',
    )

    assert os.path.isdir('test_force_render')

    # The PACKAGE_NAME file should be fully rendered (not copied as binary)
    file_content = Path('test_force_render/PACKAGE_NAME').read_text()
    assert '{{' not in file_content, 'File should have been rendered'
    assert 'example-package' in file_content

    # README.rst should still render normally
    readme = Path('test_force_render/README.rst').read_text()
    assert 'I have been rendered!' in readme


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_force_render_without_setting_falls_back_to_binary() -> None:
    """Verify that without `_force_render`, binary files are copied without rendering.

    Files detected as binary should remain unrendered when `_force_render`
    is not configured.
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_force_render',
                'project_slug': 'example-package',
                'render_test': 'I have been rendered!',
                # No _force_render — binary detection applies
            }
        },
        repo_dir='tests/test-generate-force-render',
    )

    assert os.path.isdir('test_force_render')

    # The PACKAGE_NAME file should NOT be rendered (copied as binary)
    file_content = Path('test_force_render/PACKAGE_NAME').read_text()
    assert '{{' in file_content, 'File should have been copied without rendering'
    assert '{{ cookiecutter.project_slug }}' in file_content

    # README.rst should still render normally
    readme = Path('test_force_render/README.rst').read_text()
    assert 'I have been rendered!' in readme
