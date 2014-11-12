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


@pytest.mark.usefixtures("clean_system")
def test_generate_context():
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json'
    )
    assert context == {"test": {"1": 2, "some_key": "some_val"}}


@pytest.mark.usefixtures("clean_system")
def test_generate_context_with_default():
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json',
        default_context={"1": 3}
    )
    assert context == {"test": {"1": 3, "some_key": "some_val"}}


@pytest.mark.usefixtures("clean_system")
def test_generate_context_with_extra():
    """ Call `generate_context()` with extra_context. """
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json',
        extra_context={'1': 4},
    )
    assert context == {'test': {'1': 4, 'some_key': 'some_val'}}


@pytest.mark.usefixtures("clean_system")
def test_generate_context_with_default_and_extra():
    """ Call `generate_context()` with `default_context` and
        `extra_context`. """
    context = generate.generate_context(
        context_file='tests/test-generate-context/test.json',
        default_context={'1': 3},
        extra_context={'1': 5},
    )
    assert context == {'test': {'1': 5, 'some_key': 'some_val'}}
