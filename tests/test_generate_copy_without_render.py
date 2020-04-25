# -*- coding: utf-8 -*-

"""Verify correct work of `_copy_without_render` context option."""

from __future__ import unicode_literals
import os
import pytest

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture
def remove_test_dir():
    """Fixture. Remove the folder that is created by the test."""
    yield
    if os.path.exists('test_copy_without_render'):
        utils.rmtree('test_copy_without_render')


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_copy_without_render_extensions():
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
                ],
            }
        },
        repo_dir='tests/test-generate-copy-without-render',
    )

    dir_contents = os.listdir('test_copy_without_render')

    assert '{{cookiecutter.repo_name}}-not-rendered' in dir_contents
    assert 'test_copy_without_render-rendered' in dir_contents

    with open('test_copy_without_render/README.txt') as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/README.rst') as f:
        assert 'I have been rendered!' in f.read()

    with open(
        'test_copy_without_render/' 'test_copy_without_render-rendered/' 'README.txt'
    ) as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open(
        'test_copy_without_render/' 'test_copy_without_render-rendered/' 'README.rst'
    ) as f:
        assert 'I have been rendered' in f.read()

    with open(
        'test_copy_without_render/'
        '{{cookiecutter.repo_name}}-not-rendered/'
        'README.rst'
    ) as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/rendered/not_rendered.yml') as f:
        assert '{{cookiecutter.render_test}}' in f.read()
