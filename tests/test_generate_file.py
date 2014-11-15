#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_file
------------------

Tests formerly known from a unittest residing in test_generate.py named
TestGenerateFile.test_generate_file
"""

from __future__ import unicode_literals
import os
import pytest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from cookiecutter import generate
from cookiecutter import utils


@pytest.fixture(scope='function')
def remove_cheese_file(request):
    """
    Remove the cheese text file which is created by the tests.
    """
    def fin_remove_cheese_file():
        if os.path.exists('tests/files/cheese.txt'):
            os.remove('tests/files/cheese.txt')
    request.addfinalizer(fin_remove_cheese_file)


@pytest.mark.usefixtures('remove_cheese_file')
def test_generate_file():
    env = Environment()
    env.loader = FileSystemLoader('.')
    infile = 'tests/files/{{generate_file}}.txt'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'generate_file': 'cheese'},
        env=env
    )
    assert os.path.isfile('tests/files/cheese.txt')
    with open('tests/files/cheese.txt', 'rt') as f:
        generated_text = f.read()
        assert generated_text == 'Testing cheese'
