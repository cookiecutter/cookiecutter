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


@pytest.fixture(autouse=True)
def test_env_should_contain_delimiter_overrides(monkeypatch):
    monkeypatch.setenv('J2_VARIABLE_START_STRING', '<<')
    monkeypatch.setenv('J2_VARIABLE_END_STRING', '>>')
    monkeypatch.setenv('J2_BLOCK_START_STRING', '<%')
    monkeypatch.setenv('J2_BLOCK_END_STRING', '%>')
    monkeypatch.setenv('J2_COMMENT_START_STRING', '<#')
    monkeypatch.setenv('J2_COMMENT_END_STRING', '#>')

    env = StrictEnvironment(keep_trailing_newline=True)
    assert '<<' == env.variable_start_string
    assert '>>' == env.variable_end_string
    assert '<%' == env.block_start_string
    assert '%>' == env.block_end_string
    assert '<#' == env.comment_start_string
    assert '#>' == env.comment_end_string
