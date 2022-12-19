"""Collection of tests around loading extensions."""
import pytest

from cookieninja.environment import StrictEnvironment
from cookieninja.exceptions import UnknownExtension


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
    assert 'cookieninja.extensions.JsonifyExtension' in env.extensions
    assert 'cookieninja.extensions.RandomStringExtension' in env.extensions
    assert 'cookieninja.extensions.SlugifyExtension' in env.extensions
    assert 'cookieninja.extensions.UUIDExtension' in env.extensions
