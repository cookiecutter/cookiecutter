# -*- coding: utf-8 -*-

"""
test_read_user_dict
-------------------
"""

from __future__ import unicode_literals

import click
import pytest

from cookiecutter.prompt import read_user_dict


def test_use_default_dict(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = 'default'

    VARIABLE = 'var'
    DEFAULT = {"key": 1}

    assert read_user_dict(VARIABLE, DEFAULT) == {'key': 1}

    click.prompt.assert_called_once_with(VARIABLE, default='default')


def test_empty_input_dict(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = '{}'

    VARIABLE = 'var'
    DEFAULT = {"key": 1}

    assert read_user_dict(VARIABLE, DEFAULT) == {}

    click.prompt.assert_called_once_with(VARIABLE, default='default')


def test_use_empty_default_dict(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = 'default'

    VARIABLE = 'var'
    DEFAULT = {}

    assert read_user_dict(VARIABLE, DEFAULT) == {}

    click.prompt.assert_called_once_with(VARIABLE, default='default')


def test_shallow_dict(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = '{"key": 2}'

    VARIABLE = 'var'
    DEFAULT = {}

    assert read_user_dict(VARIABLE, DEFAULT) == {'key': 2}

    click.prompt.assert_called_once_with(VARIABLE, default='default')


def test_deep_dict(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = '''{
        "key": "value",
        "integer_key": 37,
        "dict_key": {
            "deep_key": "deep_value",
            "deep_integer": 42,
            "deep_list": [
                "deep value 1",
                "deep value 2",
                "deep value 3"
            ]
        },
        "list_key": [
            "value 1",
            "value 2",
            "value 3"
        ]
    }'''

    VARIABLE = 'var'
    DEFAULT = {}

    assert read_user_dict(VARIABLE, DEFAULT) == {
        "key": "value",
        "integer_key": 37,
        "dict_key": {
            "deep_key": "deep_value",
            "deep_integer": 42,
            "deep_list": [
                "deep value 1",
                "deep value 2",
                "deep value 3",
            ]
        },
        "list_key": [
            "value 1",
            "value 2",
            "value 3",
        ]
    }

    click.prompt.assert_called_once_with(VARIABLE, default='default')


def test_raise_if_value_is_not_dict():
    with pytest.raises(TypeError):
        read_user_dict('foo', 'NOT A LIST')


def test_raise_if_value_not_valid_json(mocker):
    prompt = mocker.patch('click.prompt')
    prompt.return_value = '{'

    with pytest.raises(ValueError):
        read_user_dict('foo', {})
