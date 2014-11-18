#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_abbreviation_expansion
---------------------------

Tests formerly known from a unittest residing in test_main.py named
TestAbbreviationExpansion.test_abbreviation_expansion
"""

from __future__ import unicode_literals
import pytest

from cookiecutter import main


def expansion_data():
    """
    Fixture for test_abbreviation_expansion providing several parameters for
    main.expand_abbreviations (input_dir, config_dict) as well as a
    corresponding return value (exp_dir).
    """
    regular = (
        'foo',
        {'abbreviations': {'foo': 'bar'}},
        'bar'
    )

    yield regular


@pytest.mark.parametrize('input_dir, config_dict, exp_dir', expansion_data())
def test_abbreviation_expansion(input_dir, config_dict, exp_dir):
    expanded_input_dir = main.expand_abbreviations(input_dir, config_dict)
    assert expanded_input_dir == exp_dir
