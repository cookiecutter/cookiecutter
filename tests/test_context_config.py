#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
test_context_config
---------------

Tests for context related config functions
'''

import pytest

from cookiecutter.config import get_from_context


@pytest.fixture
def get_context():
    """
    helper method to get a context object
    """
    basic = {
        'string': 'value1',
        'list': ['value1', 'value2'],
        'dict': {
            'string': 'value1',
            'deep': {
                'path': {
                    'list': ['value1', 'value2'],
                }
            }
        }
    }

    nested_list = [[1, 2], [3, 4]]

    return {
        'basic': basic,
        'nested_list': nested_list
    }


def test_get_config():
    """
    get the config value of a first level key
    """
    context = get_context()['basic']

    assert context['string'] == get_from_context(context, 'string')
    assert context['list'] == get_from_context(context, 'list')
    assert context['dict'] == get_from_context(context, 'dict')


def test_get_config_dot_notation():
    """
    get a value using dot notation
    """
    context = get_context()['basic']

    assert context['dict']['string'] == get_from_context(
        context, 'dict.string')
    assert context['dict']['deep']['path']['list'] == get_from_context(
        context, 'dict.deep.path.list')
    assert context['list'][0] == get_from_context(context, 'list.0')


def test_get_config_dot_notation_for_nested_lists():
    """
    get a value using dot notation in nested lists
    """
    context = get_context()['nested_list']

    assert context[1][0] == get_from_context(context, '1.0')


def test_get_config_with_non_existing_key():
    """
    returns None if the given key does not exist
    """
    context = get_context()['basic']

    assert get_from_context(context, 'not_existing') is None
    assert get_from_context(context, 'dict.not_existing') is None


def test_get_config_with_default_value():
    """
    a default value can be specified to be returned in case the key does not
    exist
    """
    context = get_context()['basic']
    expected = 'otherstring'
    key = 'not_existing'

    assert expected == get_from_context(context, key, expected)
    assert [] == get_from_context(context, key, [])
    assert {} == get_from_context(context, key, {})
    assert get_from_context(context, key, True)
    assert not get_from_context(context, key, False)
    assert key not in context


def test_get_config_create_missing_key():
    """
    a missing key can be initialized
    """
    context = get_context()['basic']
    value = 'value2'
    key = 'string2'

    assert get_from_context(context, 'dict.missing', update=True) is None
    assert 'missing' in context['dict']
    assert value == get_from_context(context, key, value, True)
    assert key in context
