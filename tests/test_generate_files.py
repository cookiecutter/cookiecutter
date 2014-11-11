#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_files
-------------------

Test formerly known from a unittest residing in test_generate.py named
TestGenerateFiles.test_generate_files_nontemplated_exception
TestGenerateFiles.test_generate_files
"""

from __future__ import unicode_literals
import os
import io
import pytest

from cookiecutter import generate
from cookiecutter import exceptions
from cookiecutter import utils


@pytest.fixture(scope="function")
def clean_system_remove_additional_folders(request, clean_system):
    """
    Use the global clean_system fixture and run additional teardown code to
    remove some special folders.

    For a better understanding - order of fixture calls:
    clean_system setup code
    clean_system_remove_additional_folders setup code
    clean_system_remove_additional_folders teardown code
    clean_system teardown code
    """
    def remove_additional_folders():
        if os.path.exists('inputpizzä'):
            utils.rmtree('inputpizzä')
        if os.path.exists('inputgreen'):
            utils.rmtree('inputgreen')
        if os.path.exists('inputbinary_files'):
            utils.rmtree('inputbinary_files')
        if os.path.exists('tests/custom_output_dir'):
            utils.rmtree('tests/custom_output_dir')
        if os.path.exists('inputpermissions'):
            utils.rmtree('inputpermissions')
    request.addfinalizer(remove_additional_folders)


@pytest.mark.usefixtures("clean_system_remove_additional_folders")
def test_generate_files_nontemplated_exception():
    with pytest.raises(exceptions.NonTemplatedInputDirException):
        generate.generate_files(
            context={
                'cookiecutter': {'food': 'pizza'}
            },
            repo_dir='tests/test-generate-files-nontemplated'
        )


@pytest.mark.usefixtures("clean_system_remove_additional_folders")
def test_generate_files():
    generate.generate_files(
        context={
            'cookiecutter': {'food': 'pizzä'}
        },
        repo_dir='tests/test-generate-files'
    )

    simple_file = 'inputpizzä/simple.txt'
    assert os.path.isfile(simple_file)

    simple_text = io.open(simple_file, 'rt', encoding='utf-8').read()
    assert simple_text == u'I eat pizzä'


@pytest.mark.usefixtures("clean_system_remove_additional_folders")
def test_generate_files_with_trailing_newline():
    generate.generate_files(
        context={
            'cookiecutter': {'food': 'pizzä'}
        },
        repo_dir='tests/test-generate-files'
    )

    newline_file = 'inputpizzä/simple-with-newline.txt'
    assert os.path.isfile(newline_file)

    with io.open(newline_file, 'r', encoding='utf-8') as f:
        simple_text = f.read()
    assert simple_text == u'I eat pizzä\n'
