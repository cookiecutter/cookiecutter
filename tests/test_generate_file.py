# -*- coding: utf-8 -*-

"""Tests for `generate_file` function, part of `generate_files` function workflow."""

from __future__ import unicode_literals

import json
import os

import pytest
from jinja2 import FileSystemLoader
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter.environment import StrictEnvironment


@pytest.fixture(scope='function', autouse=True)
def tear_down():
    """
    Fixture. Remove the test text file which is created by the tests.

    Used for all tests in this file.
    """
    yield
    if os.path.exists('tests/files/cheese.txt'):
        os.remove('tests/files/cheese.txt')


@pytest.fixture
def env():
    """Fixture. Set Jinja2 environment settings for other tests."""
    environment = StrictEnvironment()
    environment.loader = FileSystemLoader('.')
    return environment


def test_generate_file(env):
    """Verify simple file is generated with rendered context data."""
    infile = 'tests/files/{{generate_file}}.txt'
    generate.generate_file(
        project_dir=".", infile=infile, context={'generate_file': 'cheese'}, env=env
    )
    assert os.path.isfile('tests/files/cheese.txt')
    with open('tests/files/cheese.txt', 'rt') as f:
        generated_text = f.read()
        assert generated_text == 'Testing cheese'


def test_generate_file_jsonify_filter(env):
    """Verify jsonify filter works during files generation process."""
    infile = 'tests/files/{{cookiecutter.jsonify_file}}.txt'
    data = {'jsonify_file': 'cheese', 'type': 'roquefort'}
    generate.generate_file(
        project_dir=".", infile=infile, context={'cookiecutter': data}, env=env
    )
    assert os.path.isfile('tests/files/cheese.txt')
    with open('tests/files/cheese.txt', 'rt') as f:
        generated_text = f.read()
        assert json.loads(generated_text) == data


@pytest.mark.parametrize("length", (10, 40))
@pytest.mark.parametrize("punctuation", (True, False))
def test_generate_file_random_ascii_string(env, length, punctuation):
    """Verify correct work of random_ascii_string extension on file generation."""
    infile = 'tests/files/{{cookiecutter.random_string_file}}.txt'
    data = {'random_string_file': 'cheese'}
    context = {"cookiecutter": data, "length": length, "punctuation": punctuation}
    generate.generate_file(project_dir=".", infile=infile, context=context, env=env)
    assert os.path.isfile('tests/files/cheese.txt')
    with open('tests/files/cheese.txt', 'rt') as f:
        generated_text = f.read()
        assert len(generated_text) == length


def test_generate_file_with_true_condition(env):
    """Verify correct work of boolean condition in file name on file generation.

    This test has positive answer, so file should be rendered.
    """
    infile = 'tests/files/{% if generate_file == \'y\' %}cheese.txt{% endif %}'
    generate.generate_file(
        project_dir=".", infile=infile, context={'generate_file': 'y'}, env=env
    )
    assert os.path.isfile('tests/files/cheese.txt')
    with open('tests/files/cheese.txt', 'rt') as f:
        generated_text = f.read()
        assert generated_text == 'Testing that generate_file was y'


def test_generate_file_with_false_condition(env):
    """Verify correct work of boolean condition in file name on file generation.

    This test has negative answer, so file should not be rendered.
    """
    infile = 'tests/files/{% if generate_file == \'y\' %}cheese.txt{% endif %}'
    generate.generate_file(
        project_dir=".", infile=infile, context={'generate_file': 'n'}, env=env
    )
    assert not os.path.isfile('tests/files/cheese.txt')


@pytest.fixture
def expected_msg():
    """Fixture. Used to ensure that exception generated text contain full data."""
    msg = (
        'Missing end of comment tag\n'
        '  File "./tests/files/syntax_error.txt", line 1\n'
        '    I eat {{ syntax_error }} {# this comment is not closed}'
    )
    return msg.replace("/", os.sep)


def test_generate_file_verbose_template_syntax_error(env, expected_msg):
    """Verify correct exception raised on syntax error in file before generation."""
    with pytest.raises(TemplateSyntaxError) as exception:
        generate.generate_file(
            project_dir=".",
            infile='tests/files/syntax_error.txt',
            context={'syntax_error': 'syntax_error'},
            env=env,
        )
    assert str(exception.value) == expected_msg
