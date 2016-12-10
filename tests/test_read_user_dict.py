# -*- coding: utf-8 -*-

"""
test_read_user_dict
-------------------
"""

from __future__ import unicode_literals

import click
import pytest

from cookiecutter.prompt import (
    create_value_proc,
    read_user_dict,
)


@pytest.fixture
def value_proc():
    return create_value_proc(
        'default123',
        {
            'key': 1,
        },
    )


def test_value_proc_default_display(value_proc):
    assert value_proc('default123') == {'key': 1}


def test_value_proc_invalid_json(value_proc):
    with pytest.raises(click.UsageError) as exc_info:
        value_proc('nope]')

    assert str(exc_info.value) == 'Unable to decode to JSON.'


def test_value_proc_non_dict(value_proc):
    with pytest.raises(click.UsageError) as exc_info:
        value_proc('[1, 2]')

    assert str(exc_info.value) == 'Requires JSON dict.'


def test_value_proc_valid_json(value_proc):
    user_value = '{"name": "foobar", "bla": ["a", 1, "b", false]}'

    assert value_proc(user_value) == {
        'name': 'foobar',
        'bla': ['a', 1, 'b', False],
    }


def test_value_proc_deep_dict(value_proc):
    user_value = '''{
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

    assert value_proc(user_value) == {
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


def test_should_raise_type_error(mocker):
    prompt = mocker.patch('click.prompt')

    with pytest.raises(TypeError):
        read_user_dict('name', 'russell')

    assert not prompt.called


def test_should_call_prompt_with_value_proc(mocker):
    """Test to make sure that create_value_proc is actually being used
    to generate a processer for the user input."""
    prompt = mocker.patch('click.prompt')

    def process_json(user_value):
        return user_value

    create_value_proc = mocker.patch(
        'cookiecutter.prompt.create_value_proc',
        return_value=process_json,
    )

    read_user_dict('name', {'project_slug': 'pytest-plugin'})

    assert create_value_proc.call_args == mocker.call(
        'default',
        {'project_slug': 'pytest-plugin'},
    )
    assert prompt.call_args == mocker.call(
        'name',
        type=click.STRING,
        default='default',
        value_proc=process_json,
    )
