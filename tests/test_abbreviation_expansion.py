#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_abbreviation_expansion
---------------------------

Tests formerly known from a unittest residing in test_main.py named
TestAbbreviationExpansion.test_abbreviation_expansion
TestAbbreviationExpansion.test_abbreviation_expansion_not_an_abbreviation
TestAbbreviationExpansion.test_abbreviation_expansion_prefix
TestAbbreviationExpansion.test_abbreviation_expansion_builtin
TestAbbreviationExpansion.test_abbreviation_expansion_override_builtin
TestAbbreviationExpansion.test_abbreviation_expansion_prefix_ignores_suffix
TestAbbreviationExpansion.test_abbreviation_expansion_prefix_not_0_in_braces
"""

from __future__ import unicode_literals
import pytest

from cookiecutter import main


def test_abbreviation_expansion():
    input_dir = main.expand_abbreviations(
        'foo', {'abbreviations': {'foo': 'bar'}}
    )
    assert input_dir == 'bar'


def test_abbreviation_expansion_not_an_abbreviation():
    input_dir = main.expand_abbreviations(
        'baz', {'abbreviations': {'foo': 'bar'}}
    )
    assert input_dir == 'baz'


def test_abbreviation_expansion_prefix():
    input_dir = main.expand_abbreviations(
        'xx:a', {'abbreviations': {'xx': '<{0}>'}}
    )
    assert input_dir == '<a>'


def test_abbreviation_expansion_builtin():
    input_dir = main.expand_abbreviations(
        'gh:a', {}
    )
    assert input_dir == 'https://github.com/a.git'


def test_abbreviation_expansion_override_builtin():
    input_dir = main.expand_abbreviations(
        'gh:a', {'abbreviations': {'gh': '<{0}>'}}
    )
    assert input_dir == '<a>'


def test_abbreviation_expansion_prefix_ignores_suffix():
    input_dir = main.expand_abbreviations(
        'xx:a', {'abbreviations': {'xx': '<>'}}
    )
    assert input_dir == '<>'


def test_abbreviation_expansion_prefix_not_0_in_braces():
    with pytest.raises(IndexError):
        main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '{1}'}})
