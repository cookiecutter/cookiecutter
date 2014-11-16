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

from cookiecutter import generate


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
