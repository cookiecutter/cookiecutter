# -*- coding: utf-8 -*-

"""
test_load
-----------
"""
import functools
import json
import pytest

from cookiecutter import replay
from tests.utils import dir_tests

test_replay_dir = functools.partial(dir_tests, 'test-replay')


def test_type_error_if_no_template_name():
    """Test that replay.load raises if the tempate_name is not a valid str."""
    with pytest.raises(TypeError):
        replay.load(test_replay_dir(), None)


def test_value_error_if_key_missing_in_context(mocker):
    """Test that replay.load raises if the loaded context does not contain
    'cookiecutter'.
    """
    with pytest.raises(ValueError):
        replay.load(test_replay_dir(), 'invalid_replay')


def test_io_error_if_no_replay_file(mocker):
    """Test that replay.load raises if it cannot find a replay file."""
    with pytest.raises(IOError):
        replay.load(test_replay_dir(), 'no_replay')


def test_run_json_load(mocker, mock_user_config, context):
    """Test that replay.load runs json.load under the hood and that the context
    is correctly loaded from the file in replay_dir.
    """
    spy_get_replay_file = mocker.spy(replay, 'get_file_name')

    mock_json_load = mocker.patch('json.load', side_effect=json.load)

    loaded_context = replay.load(test_replay_dir(), 'cookiedozer_load')

    assert not mock_user_config.called
    spy_get_replay_file.assert_called_once_with(test_replay_dir(), 'cookiedozer_load')

    assert mock_json_load.call_count == 1
    (infile_handler,), kwargs = mock_json_load.call_args
    assert infile_handler.name == test_replay_dir('cookiedozer_load.json')
    assert loaded_context == context
