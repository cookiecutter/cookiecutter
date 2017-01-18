# -*- coding: utf-8 -*-

"""
test_read_user_dict
-------------------
"""

from __future__ import unicode_literals

import click
import pytest

from cookiecutter.prompt import (
    process_json,
    read_user_dict,
)


def test_process_json_invalid_json():
    with pytest.raises(click.UsageError) as exc_info:
        process_json('nope]')

    assert str(exc_info.value) == 'Unable to decode to JSON.'


def test_process_json_non_dict():
    with pytest.raises(click.UsageError) as exc_info:
        process_json('[1, 2]')

    assert str(exc_info.value) == 'Requires JSON dict.'


def test_process_json_valid_json():
    user_value = '{"name": "foobar", "bla": ["a", 1, "b", false]}'

    assert process_json(user_value) == {
        'name': 'foobar',
        'bla': ['a', 1, 'b', False],
    }


def test_process_json_deep_dict():
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

    assert process_json(user_value) == {
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


def test_should_call_prompt_with_process_json(mocker):
    """Test to make sure that process_jon is actually being used
    to generate a processer for the user input."""

    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
    )

    read_user_dict('name', {'project_slug': 'pytest-plugin'})

    assert mock_prompt.call_args == mocker.call(
        'name',
        type=click.STRING,
        default='default',
        value_proc=process_json,
    )


def test_read_user_dict_default_value(mocker):
    """Test to make sure that read_user_dict returns the default value for a
    dict variable rather than the display value.
    """
    mock_prompt = mocker.patch(
        'cookiecutter.prompt.click.prompt',
        autospec=True,
        return_value='default',
    )

    val = read_user_dict('name', {'project_slug': 'pytest-plugin'})

    assert mock_prompt.call_args == mocker.call(
        'name',
        type=click.STRING,
        default='default',
        value_proc=process_json,
    )

    assert val == {'project_slug': 'pytest-plugin'}
