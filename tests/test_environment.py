# -*- coding: utf-8 -*-

"""Collection of tests around loading extensions."""

import pytest

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UnknownExtension


def test_env_should_raise_for_unknown_extension():
    """Test should raise if extension not installed in system."""
    context = {'cookiecutter': {'_extensions': ['foobar']}}

    with pytest.raises(UnknownExtension) as err:
        StrictEnvironment(context=context, keep_trailing_newline=True)

    assert 'Unable to load extension: ' in str(err.value)


def test_env_should_come_with_default_extensions():
    """Verify default extensions loaded with StrictEnvironment."""
    env = StrictEnvironment(keep_trailing_newline=True)
    assert 'jinja2_time.jinja2_time.TimeExtension' in env.extensions
    assert 'cookiecutter.extensions.JsonifyExtension' in env.extensions
    assert 'cookiecutter.extensions.RandomStringExtension' in env.extensions
    assert 'cookiecutter.extensions.SlugifyExtension' in env.extensions
