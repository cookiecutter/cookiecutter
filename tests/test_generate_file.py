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

import shutil

import os
import pytest
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from tests.utils import dir_tests


@pytest.fixture
def env(tmpdir):
    os.chdir(str(tmpdir))
    shutil.copytree(dir_tests('files'), str(tmpdir.join('files')))

    environment = Environment()
    environment.loader = FileSystemLoader(str(tmpdir))
    return environment


def test_generate_file(env, tmpdir):
    infile = 'files/{{generate_file}}.txt'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'generate_file': 'cheese'},
        env=env
    )
    assert os.path.isfile(str(tmpdir.join('files/cheese.txt')))
    with tmpdir.join('files/cheese.txt').open('rt') as f:
        generated_text = f.read()
        assert generated_text == 'Testing cheese'


def test_generate_file_with_false_condition(env):
    infile = 'files/{% if generate_file == \'y\' %}cheese.txt{% endif %}'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'generate_file': 'n'},
        env=env
    )
    assert not os.path.exists('tests/files/cheese.txt')


def test_generate_file_with_true_conditional(env, tmpdir):
    infile = 'files/{% if generate_file == \'y\' %}cheese.txt{% endif %}'
    generate.generate_file(
        project_dir=".",
        infile=infile,
        context={'generate_file': 'y'},
        env=env
    )
    assert os.path.isfile(str(tmpdir.join('files/cheese.txt')))
    with tmpdir.join('files/cheese.txt').open('rt') as f:
        generated_text = f.read()
        assert generated_text == 'Testing that generate_file was y'


@pytest.fixture
def expected_msg(tmpdir):
    msg = (
        'Missing end of comment tag\n'
        '  File "%s", line 1\n'
        '    I eat {{ syntax_error }} {# this comment is not closed}'
    ) % tmpdir.join('files/syntax_error.txt')
    return msg


def test_generate_file_verbose_template_syntax_error(env, expected_msg):
    try:
        generate.generate_file(
            project_dir=".",
            infile='files/syntax_error.txt',
            context={'syntax_error': 'syntax_error'},
            env=env
        )
    except TemplateSyntaxError as exception:
        assert str(exception) == expected_msg
    except Exception as exception:
        pytest.fail('Unexpected exception thrown: {0}'.format(exception))
    else:
        pytest.fail('TemplateSyntaxError not thrown')
