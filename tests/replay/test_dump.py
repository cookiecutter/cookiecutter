# -*- coding: utf-8 -*-

"""
test_dump
---------
"""

import json
import os
import pytest

from cookiecutter import replay


@pytest.fixture
def template_name():
    """Fixture to return a valid template_name."""
    return 'cookiedozer'


@pytest.fixture
def replay_file(replay_test_dir, template_name):
    """Fixture to return a actual file name of the dump."""
    file_name = '{}.json'.format(template_name)
    return os.path.join(replay_test_dir, file_name)


@pytest.fixture(autouse=True)
def remove_replay_dump(request, replay_file):
    """Remove the replay file created by tests."""
    def fin_remove_replay_file():
        if os.path.exists(replay_file):
            os.remove(replay_file)
    request.addfinalizer(fin_remove_replay_file)


def test_type_error_if_no_template_name(replay_test_dir, context):
    """Test that replay.dump raises if the tempate_name is not a valid str."""
    with pytest.raises(TypeError):
        replay.dump(replay_test_dir, None, context)


def test_type_error_if_not_dict_context(replay_test_dir, template_name):
    """Test that replay.dump raises if the context is not of type dict."""
    with pytest.raises(TypeError):
        replay.dump(replay_test_dir, template_name, 'not_a_dict')


def test_value_error_if_key_missing_in_context(replay_test_dir, template_name):
    """Test that replay.dump raises if the context does not contain a key
    named 'cookiecutter'.
    """
    with pytest.raises(ValueError):
        replay.dump(replay_test_dir, template_name, {'foo': 'bar'})


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


def test_ioerror_if_replay_dir_creation_fails(
        mock_ensure_failure, replay_test_dir):
    """Test that replay.dump raises when the replay_dir cannot be created."""

    with pytest.raises(IOError):
        replay.dump(
            replay_test_dir,
            'foo', {'cookiecutter': {'hello': 'world'}}
        )

    mock_ensure_failure.assert_called_once_with(replay_test_dir)


def test_run_json_dump(mocker, mock_ensure_success, mock_user_config,
                       template_name, context, replay_test_dir, replay_file):
    """Test that replay.dump runs json.dump under the hood and that the context
    is correctly written to the expected file in the replay_dir.
    """
    spy_get_replay_file = mocker.spy(replay, 'get_file_name')

    mock_json_dump = mocker.patch('json.dump', side_effect=json.dump)

    replay.dump(replay_test_dir, template_name, context)

    assert not mock_user_config.called
    mock_ensure_success.assert_called_once_with(replay_test_dir)
    spy_get_replay_file.assert_called_once_with(replay_test_dir, template_name)

    assert mock_json_dump.call_count == 1
    (dumped_context, outfile_handler), kwargs = mock_json_dump.call_args
    assert outfile_handler.name == replay_file
    assert dumped_context == context
