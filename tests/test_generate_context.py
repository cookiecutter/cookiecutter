#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate_context
---------------------

Tests formerly known from a unittest residing in test_generate.py named
TestGenerateContext.test_generate_context
TestGenerateContext.test_generate_context_with_default
TestGenerateContext.test_generate_context_with_extra
TestGenerateContext.test_generate_context_with_default_and_extra
"""

from __future__ import unicode_literals
import pytest
import os
import re
from collections import OrderedDict

from cookiecutter import generate
from cookiecutter.exceptions import ContextDecodingException


def context_data():
    context = (
        {
            'context_file': 'tests/test-generate-context/test.json'
        },
        {
            'test': {'1': 2, 'some_key': 'some_val'}
        }
    )

    context_with_default = (
        {
            'context_file': 'tests/test-generate-context/test.json',
            'default_context': {'1': 3}
        },
        {
            'test': {'1': 3, 'some_key': 'some_val'}
        }
    )

    context_with_extra = (
        {
            'context_file': 'tests/test-generate-context/test.json',
            'extra_context': {'1': 4},
        },
        {
            'test': {'1': 4, 'some_key': 'some_val'}
        }
    )

    context_with_default_and_extra = (
        {
            'context_file': 'tests/test-generate-context/test.json',
            'default_context': {'1': 3},
            'extra_context': {'1': 5},
        },
        {
            'test': {'1': 5, 'some_key': 'some_val'}
        }
    )

    yield context
    yield context_with_default
    yield context_with_extra
    yield context_with_default_and_extra


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data())
def test_generate_context(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    assert generate.generate_context(**input_params) == expected_context


@pytest.mark.usefixtures('clean_system')
def test_generate_context_with_json_decoding_error():
    with pytest.raises(ContextDecodingException) as excinfo:
        generate.generate_context(
            'tests/test-generate-context/invalid-syntax.json'
        )
    # original message from json module should be included
    pattern = (
        'Expecting \'{0,1}:\'{0,1} delimiter: '
        'line 1 column (19|20) \(char 19\)'
    )
    assert re.search(pattern, str(excinfo.value))
    # File name should be included too...for testing purposes, just test the
    # last part of the file. If we wanted to test the absolute path, we'd have
    # to do some additional work in the test which doesn't seem that needed at
    # this point.
    path = os.path.sep.join(
        ['tests', 'test-generate-context', 'invalid-syntax.json']
    )
    assert path in str(excinfo.value)


@pytest.fixture
def default_context():
    return {
        'not_in_template': 'foobar',
        'project_name': 'Kivy Project',
        'orientation': 'landscape'
    }


@pytest.fixture
def extra_context():
    return {
        'also_not_in_template': 'foobar2',
        'github_username': 'hackebrot',
    }


@pytest.fixture
def context_file():
    return 'tests/test-generate-context/choices_template.json'


def test_choices(context_file, default_context, extra_context):
    """Make sure that the default for list variables is based on the user
    config and the list as such is not changed to a single value.
    """
    expected_context = {
        'choices_template': OrderedDict([
            ('full_name', 'Raphael Pierzina'),
            ('github_username', 'hackebrot'),
            ('project_name', 'Kivy Project'),
            ('repo_name', '{{cookiecutter.project_name|lower}}'),
            ('orientation', ['landscape', 'all', 'portrait']),
        ])
    }

    generated_context = generate.generate_context(
        context_file, default_context, extra_context
    )

    assert generated_context == expected_context


@pytest.fixture
def template_context():
    return OrderedDict([
        ('full_name', 'Raphael Pierzina'),
        ('github_username', 'hackebrot'),
        ('project_name', 'Kivy Project'),
        ('repo_name', '{{cookiecutter.project_name|lower}}'),
        ('orientation', ['all', 'landscape', 'portrait']),
    ])


def test_apply_overwrites_does_include_unused_variables(template_context):
    generate.apply_overwrites_to_context(
        template_context,
        {'not in template': 'foobar'}
    )

    assert 'not in template' not in template_context


def test_apply_overwrites_sets_non_list_value(template_context):
    generate.apply_overwrites_to_context(
        template_context,
        {'repo_name': 'foobar'}
    )

    assert template_context['repo_name'] == 'foobar'


def test_apply_overwrites_does_not_modify_choices_for_invalid_overwrite(
        template_context):
    generate.apply_overwrites_to_context(
        template_context,
        {'orientation': 'foobar'}
    )

    assert template_context['orientation'] == ['all', 'landscape', 'portrait']


def test_apply_overwrites_sets_default_for_choice_variable(template_context):
    generate.apply_overwrites_to_context(
        template_context,
        {'orientation': 'landscape'}
    )

    assert template_context['orientation'] == ['landscape', 'all', 'portrait']
