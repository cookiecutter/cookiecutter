# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

import pytest

from cookiecutter import replay, main, exceptions


def test_get_replay_file_name():
    """Make sure that replay.get_file_name generates a valid json file path."""
    assert replay.get_file_name('foo', 'bar') == 'foo/bar.json'


@pytest.fixture(params=[
    {'no_input': True},
    {'extra_context': {}},
    {'no_input': True, 'extra_context': {}},
])
def invalid_kwargs(request):
    return request.param


def test_raise_on_invalid_mode(invalid_kwargs):
    with pytest.raises(exceptions.InvalidModeException):
        main.cookiecutter('foo', replay=True, **invalid_kwargs)
