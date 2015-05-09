#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_output_folder
------------------

Test formerly known from a unittest residing in test_generate.py named
TestOutputFolder.test_output_folder
"""

from __future__ import unicode_literals
import os
import pytest

from cookiecutter import generate
from cookiecutter import utils
from cookiecutter.main import cookiecutter as _cookiecutter


@pytest.fixture(scope='function')
def remove_output_folder(request):
    """
    Remove the output folder in case it exists on disk.
    """
    def finalizer_remove_output_folder():
        if os.path.exists('output_folder'):
            utils.rmtree('output_folder')
    request.addfinalizer(finalizer_remove_output_folder)


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
@pytest.mark.parametrize("output_dir", [None, '.', 'output_folder/somewhere_else'])
def test_output_folder(output_dir):
    context = generate.generate_context(
        context_file='tests/test-output-folder/cookiecutter.json'
    )

    params = {
        "context": context,
        "repo_dir": 'tests/test-output-folder'
    }

    # test without, default, '.' catch regressions method sig is refactored
    if output_dir:
        params['output_dir'] = output_dir

    generate.generate_files(**params)

    prefix = output_dir if output_dir else ""

    something = """Hi!
My name is Audrey Greenfeld.
It is 2014."""
    something2 = open(os.path.join(prefix,'output_folder/something.txt')).read()
    assert something == something2

    in_folder = "The color is green and the letter is D."
    in_folder2 = open(
        os.path.join(prefix, 'output_folder/folder/in_folder.txt')
    ).read()
    assert in_folder == in_folder2

    assert os.path.isdir(
        os.path.join(prefix, 'output_folder/im_a.dir')
    )
    assert os.path.isfile(
        os.path.join(prefix, 'output_folder/im_a.dir/im_a.file.py')
    )


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
@pytest.mark.parametrize("output_dir", [None, '.', 'output_folder/somewhere_else'])
def test_cookiecutter_output_folder(output_dir):

    # test without, default, '.' catch regressions method sig is refactored
    params = {}

    if output_dir:
        params['output_dir'] = output_dir

    _cookiecutter('tests/test-output-folder', no_input=True, **params)

    prefix = output_dir if output_dir else ""

    something = """Hi!
My name is Audrey Greenfeld.
It is 2014."""
    something2 = open(os.path.join(prefix,'output_folder/something.txt')).read()
    assert something == something2

    in_folder = "The color is green and the letter is D."
    in_folder2 = open(
        os.path.join(prefix, 'output_folder/folder/in_folder.txt')
    ).read()
    assert in_folder == in_folder2

    assert os.path.isdir(
        os.path.join(prefix, 'output_folder/im_a.dir')
    )
    assert os.path.isfile(
        os.path.join(prefix, 'output_folder/im_a.dir/im_a.file.py')
    )
