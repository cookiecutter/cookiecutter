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


def expansion_data():
    """
    Fixture for test_abbreviation_expansion providing several parameters for
    main.expand_abbreviations (input_dir, config_dict) as well as a
    corresponding expected return value (exp_dir).
    """
    regular_data = (
        'foo',
        {'abbreviations': {'foo': 'bar'}},
        'bar'
    )

    not_an_abbreviation_data = (
        'baz',
        {'abbreviations': {'foo': 'bar'}},
        'baz'
    )

    prefix_data = (
        'xx:a',
        {'abbreviations': {'xx': '<{0}>'}},
        '<a>'
    )

    builtin_data = (
        'gh:a',
        {},
        'https://github.com/a.git'
    )

    override_builtin_data = (
        'gh:a',
        {'abbreviations': {'gh': '<{0}>'}},
        '<a>'
    )

    prefix_ignores_suffix_data = (
        'xx:a',
        {'abbreviations': {'xx': '<>'}},
        '<>'
    )

    yield regular_data
    yield not_an_abbreviation_data
    yield prefix_data
    yield builtin_data
    yield override_builtin_data
    yield prefix_ignores_suffix_data


@pytest.mark.parametrize('input_dir, config_dict, exp_dir', expansion_data())
def test_abbreviation_expansion(input_dir, config_dict, exp_dir):
    expanded_input_dir = main.expand_abbreviations(input_dir, config_dict)
    assert expanded_input_dir == exp_dir


def test_abbreviation_expansion_prefix_not_0_in_braces():
    with pytest.raises(IndexError):
        main.expand_abbreviations('xx:a', {'abbreviations': {'xx': '{1}'}})
