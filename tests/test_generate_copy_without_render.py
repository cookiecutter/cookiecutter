# -*- coding: utf-8 -*-

"""
test_generate_copy_without_render
---------------------------------
"""

from __future__ import unicode_literals
import os
import pytest

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_test_dir(request):
    """
    Remove the folder that is created by the test.
    """
    def fin_remove_test_dir():
        if os.path.exists('test_copy_without_render'):
            utils.rmtree('test_copy_without_render')
    request.addfinalizer(fin_remove_test_dir)


@pytest.fixture(params=[True, False])
def overwrite_if_exists(request):
    return request.param


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_copy_without_render_extensions(overwrite_if_exists):

    if overwrite_if_exists:
        os.makedirs('test_copy_without_render/'
                    '{{cookiecutter.repo_name}}-not-render/'
                    'nested')
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_copy_without_render',
                'render_test': 'I have been rendered!',
                '_copy_without_render': [
                    '*not-rendered',
                    'rendered/not_rendered.yml',
                    '*.txt',
                ]}
        },
        repo_dir='tests/test-generate-copy-without-render',
        overwrite_if_exists=overwrite_if_exists,
    )

    dir_contents = os.listdir('test_copy_without_render')

    assert '{{cookiecutter.repo_name}}-not-rendered' in dir_contents
    assert 'test_copy_without_render-rendered' in dir_contents

    with open('test_copy_without_render/README.txt') as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/README.rst') as f:
        assert 'I have been rendered!' in f.read()

    with open('test_copy_without_render/'
              'test_copy_without_render-rendered/'
              'README.txt') as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/'
              'test_copy_without_render-rendered/'
              'README.rst') as f:
        assert 'I have been rendered' in f.read()

    with open('test_copy_without_render/'
              '{{cookiecutter.repo_name}}-not-rendered/'
              'README.rst') as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/'
              '{{cookiecutter.repo_name}}-not-rendered/'
              'nested/'
              'README.rst') as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/'
              '{{cookiecutter.repo_name}}-not-rendered/'
              'nested_linked/'
              'README.rst') as f:
        assert '{{cookiecutter.render_test}}' in f.read()

    with open('test_copy_without_render/rendered/not_rendered.yml') as f:
        assert '{{cookiecutter.render_test}}' in f.read()
