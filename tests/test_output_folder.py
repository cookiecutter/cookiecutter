# -*- coding: utf-8 -*-

"""
tests_output_folder.

Test formerly known from a unittest residing in test_generate.py named
TestOutputFolder.test_output_folder
"""

from __future__ import unicode_literals

import os

import pytest

from cookiecutter import exceptions
from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_output_folder(request):
    """Remove the output folder in case it exists on disk."""
    def finalizer_remove_output_folder():
        if os.path.exists('output_folder'):
            utils.rmtree('output_folder')
    request.addfinalizer(finalizer_remove_output_folder)


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
def test_output_folder():
    context = generate.generate_context(
        context_file='tests/test-output-folder/cookiecutter.json'
    )
    generate.generate_files(
        context=context,
        repo_dir='tests/test-output-folder'
    )

    something = """Hi!
My name is Audrey Greenfeld.
It is 2014."""
    something2 = open('output_folder/something.txt').read()
    assert something == something2

    in_folder = "The color is green and the letter is D."
    in_folder2 = open('output_folder/folder/in_folder.txt').read()
    assert in_folder == in_folder2

    assert os.path.isdir('output_folder/im_a.dir')
    assert os.path.isfile('output_folder/im_a.dir/im_a.file.py')


@pytest.mark.usefixtures('clean_system', 'remove_output_folder')
def test_exception_when_output_folder_exists():
    context = generate.generate_context(
        context_file='tests/test-output-folder/cookiecutter.json'
    )
    output_folder = context['cookiecutter']['test_name']

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with pytest.raises(exceptions.OutputDirExistsException):
        generate.generate_files(
            context=context,
            repo_dir='tests/test-output-folder'
        )
