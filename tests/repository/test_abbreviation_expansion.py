# -*- coding: utf-8 -*-

"""Collection of tests around common path and url shorthands."""

from __future__ import unicode_literals
import pytest

from cookiecutter.config import BUILTIN_ABBREVIATIONS
from cookiecutter.repository import expand_abbreviations


def test_abbreviation_expansion():
    input_dir = expand_abbreviations(
        'foo', {'foo': 'bar'}
    )
    assert input_dir == 'bar'


def test_abbreviation_expansion_not_an_abbreviation():
    input_dir = expand_abbreviations(
        'baz', {'foo': 'bar'}
    )
    assert input_dir == 'baz'


def test_abbreviation_expansion_prefix():
    input_dir = expand_abbreviations(
        'xx:a', {'xx': '<{0}>'}
    )
    assert input_dir == '<a>'


def test_abbreviation_expansion_builtin():
    input_dir = expand_abbreviations(
        'gh:pydanny/cookiecutter-django', BUILTIN_ABBREVIATIONS
    )
    assert input_dir == 'https://github.com/pydanny/cookiecutter-django.git'


def test_abbreviation_expansion_override_builtin():
    input_dir = expand_abbreviations(
        'gh:a', {'gh': '<{0}>'}
    )
    assert input_dir == '<a>'


def test_abbreviation_expansion_prefix_ignores_suffix():
    input_dir = expand_abbreviations(
        'xx:a', {'xx': '<>'}
    )
    assert input_dir == '<>'


def test_abbreviation_expansion_prefix_not_0_in_braces():
    with pytest.raises(IndexError):
        expand_abbreviations('xx:a', {'xx': '{1}'})
