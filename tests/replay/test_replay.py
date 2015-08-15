# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

from cookiecutter import replay


def test_get_replay_file_name():
    """Make sure that replay.get_file_name generates a valid json file path."""
    assert replay.get_file_name('foo', 'bar') == 'foo/bar.json'
