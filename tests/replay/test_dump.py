# -*- coding: utf-8 -*-

"""
test_dump
---------
"""
import functools
import json
import os
import shutil

import pytest

from cookiecutter import replay
from tests.utils import dir_tests

# replay_dir = functools.partial(dir_tests, 'test-replay')

@pytest.fixture
def temp_replay_dir(tmpdir):
    dir_replay = tmpdir.join('test-replay')
    shutil.copytree(dir_tests('test-replay'), str(dir_replay))
    return str(dir_replay)



def test_type_error_if_no_template_name(context, temp_replay_dir):
    """Test that replay.dump raises if the tempate_name is not a valid str."""
    with pytest.raises(TypeError):
        replay.dump(temp_replay_dir, None, context)


def test_type_error_if_not_dict_context(temp_replay_dir):
    """Test that replay.dump raises if the context is not of type dict."""
    with pytest.raises(TypeError):
        replay.dump(temp_replay_dir, 'cookiedozer', 'not_a_dict')


def test_value_error_if_key_missing_in_context(temp_replay_dir):
    """Test that replay.dump raises if the context does not contain a key
    named 'cookiecutter'.
    """
    with pytest.raises(ValueError):
        replay.dump(temp_replay_dir, 'cookiedozer', {'foo': 'bar'})


@pytest.fixture
def mock_ensure_failure(mocker):
    return mocker.patch(
        'cookiecutter.replay.make_sure_path_exists',
        return_value=False
    )


@pytest.fixture
def mock_ensure_success(mocker):
    return mocker.patch(
        'cookiecutter.replay.make_sure_path_exists',
        return_value=True
    )


def test_ioerror_if_replay_dir_creation_fails(mock_ensure_failure,temp_replay_dir):
    """Test that replay.dump raises when the replay_dir cannot be created."""

    with pytest.raises(IOError):
        replay.dump(temp_replay_dir,
            'foo', {'cookiecutter': {'hello': 'world'}}
        )

    mock_ensure_failure.assert_called_once_with(temp_replay_dir)


def test_run_json_dump(mocker, mock_ensure_success, mock_user_config, context,temp_replay_dir):
    """Test that replay.dump runs json.dump under the hood and that the context
    is correctly written to the expected file in the replay_dir.
    """
    spy_get_replay_file = mocker.spy(replay, 'get_file_name')

    mock_json_dump = mocker.patch('json.dump', side_effect=json.dump)

    replay.dump(temp_replay_dir, 'cookiedozer', context)

    assert not mock_user_config.called
    mock_ensure_success.assert_called_once_with(temp_replay_dir)
    spy_get_replay_file.assert_called_once_with(temp_replay_dir, 'cookiedozer')

    assert mock_json_dump.call_count == 1
    (dumped_context, outfile_handler), kwargs = mock_json_dump.call_args
    assert outfile_handler.name == os.path.join(temp_replay_dir, 'cookiedozer.json')
    assert dumped_context == context
