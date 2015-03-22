#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_copy_without_render
---------------------------------
"""

from __future__ import unicode_literals
import os
import pytest
import shutil

from cookiecutter import generate


@pytest.fixture(scope='function')
def remove_test_dir(request):
    """
    Remove the folder that is created by the test.
    """
    def fin_remove_test_dir():
        if os.path.exists('test_copy_without_render'):
            utils.rmtree('test_copy_without_render')
    request.addfinalizer(fin_remove_test_dir)


@pytest.mark.usefixtures('remove_test_dir')
def test_generate_copy_without_render_extensions():
    generate.generate_files(
        context={
            'cookiecutter': {
                "repo_name": "test_copy_without_render",
                "render_test": "I have been rendered!",
                "_copy_without_render": [
                    "*not-rendered",
                    "rendered/not_rendered.yml",
                    "*.txt",
                ]}
        },
        repo_dir='tests/test-generate-copy-without-render'
    )

    assert "{{cookiecutter.repo_name}}-not-rendered" in os.listdir("test_copy_without_render")
    assert "test_copy_without_render-rendered" in os.listdir("test_copy_without_render")

    with open("test_copy_without_render/README.txt") as f:
        assert "{{cookiecutter.render_test}}" in f.read()

    with open("test_copy_without_render/README.rst") as f:
        assert "I have been rendered!" in f.read()

    with open("test_copy_without_render/test_copy_without_render-rendered/README.txt") as f:
        assert "{{cookiecutter.render_test}}" in f.read()

    with open("test_copy_without_render/test_copy_without_render-rendered/README.rst") as f:
        assert "I have been rendered" in f.read()

    with open("test_copy_without_render/{{cookiecutter.repo_name}}-not-rendered/README.rst") as f:
        assert "{{cookiecutter.render_test}}" in f.read()

    with open("test_copy_without_render/rendered/not_rendered.yml") as f:
        assert "{{cookiecutter.render_test}}" in f.read()

    if os.path.exists('test_copy_without_render'):
        shutil.rmtree('test_copy_without_render')
