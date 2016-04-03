#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_file
------------------

Tests formerly known from a unittest residing in test_generate.py named
TestGenerateFile.test_generate_file
TestGenerateFile.test_generate_file_verbose_template_syntax_error
"""

from __future__ import unicode_literals
import os
import pytest

from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter.environment import StrictEnvironment


@pytest.fixture(scope='function')
def remove_cheese_file(request):
    """
    Remove the cheese text file which is created by the tests.
    """
    def fin_remove_cheese_file():
        if os.path.exists('tests/files/cheese.txt'):
            os.remove('tests/files/cheese.txt')
    request.addfinalizer(fin_remove_cheese_file)


@pytest.fixture
def env():
    environment = StrictEnvironment()
    environment.loader = FileSystemLoader('.')
    return environment


@pytest.mark.usefixtures('remove_cheese_file')
def test_generate_file(env):
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


@pytest.mark.usefixtures('remove_cheese_file')
def test_generate_file_with_false_condition(env):
    infile = 'tests/files/{% if generate_file == \'y\' %}cheese.txt{% endif %}'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'generate_file': 'n'},
        env=env
    )
    assert not os.path.exists('tests/files/cheese.txt')


@pytest.mark.usefixtures('remove_cheese_file')
def test_generate_file_with_true_conditional(env):
    infile = 'tests/files/{% if generate_file == \'y\' %}cheese.txt{% endif %}'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'generate_file': 'y'},
        env=env
    )
    assert os.path.isfile('tests/files/cheese.txt')
    with open('tests/files/cheese.txt', 'rt') as f:
        generated_text = f.read()
        assert generated_text == 'Testing that generate_file was y'


@pytest.fixture
def expected_msg():
    msg = (
        'Missing end of comment tag\n'
        '  File "./tests/files/syntax_error.txt", line 1\n'
        '    I eat {{ syntax_error }} {# this comment is not closed}'
    )
    return msg.replace("/", os.sep)


@pytest.mark.usefixtures('remove_cheese_file')
def test_generate_file_verbose_template_syntax_error(env, expected_msg):
    try:
        generate.generate_file(
            project_dir=".",
            infile='tests/files/syntax_error.txt',
            context={'syntax_error': 'syntax_error'},
            env=env
        )
    except TemplateSyntaxError as exception:
        assert str(exception) == expected_msg
    except Exception as exception:
        pytest.fail('Unexpected exception thrown: {0}'.format(exception))
    else:
        pytest.fail('TemplateSyntaxError not thrown')
