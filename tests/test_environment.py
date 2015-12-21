# -*- coding: utf-8 -*-

import pytest

from cookiecutter.environment import StrictEnvironment
from cookiecutter.exceptions import UnknownExtension


def test_env_should_raise_for_unknown_extension():
    context = {
        '_extensions': ['foobar']
    }

    with pytest.raises(UnknownExtension) as err:
        StrictEnvironment(context=context, keep_trailing_newline=True)

    assert 'Unable to load extension: ' in str(err.value)
