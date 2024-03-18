"""Verify correct work of `_copy_without_render` context option."""

import os
from pathlib import Path

import pytest

from cookiecutter import generate, utils


@pytest.fixture
def remove_test_dir():
    """Fixture. Remove the folder that is created by the test."""
    yield
    if os.path.exists('test_copy_without_render'):
        utils.rmtree('test_copy_without_render')


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_copy_without_render_extensions() -> None:
    """Verify correct work of `_copy_without_render` context option.

    Some files/directories should be rendered during invocation,
    some just copied, without any modification.
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_copy_without_render',
                'render_test': 'I have been rendered!',
                '_copy_without_render': [
                    '*not-rendered',
                    'rendered/not_rendered.yml',
                    '*.txt',
                    '{{cookiecutter.repo_name}}-rendered/README.md',
                ],
            }
        },
        repo_dir='tests/test-generate-copy-without-render',
    )

    dir_contents = os.listdir('test_copy_without_render')

    assert 'test_copy_without_render-not-rendered' in dir_contents
    assert 'test_copy_without_render-rendered' in dir_contents

    file_1 = Path('test_copy_without_render/README.txt').read_text()
    assert '{{cookiecutter.render_test}}' in file_1

    file_2 = Path('test_copy_without_render/README.rst').read_text()
    assert 'I have been rendered!' in file_2

    file_3 = Path(
        'test_copy_without_render/test_copy_without_render-rendered/README.txt'
    ).read_text()
    assert '{{cookiecutter.render_test}}' in file_3

    file_4 = Path(
        'test_copy_without_render/test_copy_without_render-rendered/README.rst'
    ).read_text()
    assert 'I have been rendered' in file_4

    file_5 = Path(
        'test_copy_without_render/'
        'test_copy_without_render-not-rendered/'
        'README.rst'
    ).read_text()
    assert '{{cookiecutter.render_test}}' in file_5

    file_6 = Path('test_copy_without_render/rendered/not_rendered.yml').read_text()
    assert '{{cookiecutter.render_test}}' in file_6

    file_7 = Path(
        'test_copy_without_render/' 'test_copy_without_render-rendered/' 'README.md'
    ).read_text()
    assert '{{cookiecutter.render_test}}' in file_7
