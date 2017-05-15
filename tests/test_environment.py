# -*- coding: utf-8 -*-

import pytest

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UnknownExtension


def test_env_should_raise_for_unknown_extension():
    context = {
        'cookiecutter': {
            '_extensions': ['foobar']
        }
    }

    with pytest.raises(UnknownExtension) as err:
        StrictEnvironment(context=context, keep_trailing_newline=True)

    assert 'Unable to load extension: ' in str(err.value)


def test_env_should_come_with_jinja2_time_extension():
    env = StrictEnvironment(keep_trailing_newline=True)
    assert 'jinja2_time.jinja2_time.TimeExtension' in env.extensions


def test_env_initialization_parameters():
    context = {
        'cookiecutter': {
            '_environment': {
                'lstrip_blocks': True,
                'trim_blocks': True
            }
        }
    }

    env = StrictEnvironment(context=context)
    assert env.trim_blocks is env.lstrip_blocks is True
