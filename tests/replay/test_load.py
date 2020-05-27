"""test_load."""
import json
import os

import pytest

from cookiecutter import replay


@pytest.fixture
def template_name():
    """Fixture to return a valid template_name."""
    return 'cookiedozer_load'


@pytest.fixture
def replay_file(replay_test_dir, template_name):
    """Fixture to return a actual file name of the dump."""
    file_name = '{}.json'.format(template_name)
    return os.path.join(replay_test_dir, file_name)


def test_type_error_if_no_template_name(replay_test_dir):
    """Test that replay.load raises if the template_name is not a valid str."""
    with pytest.raises(TypeError):
        replay.load(replay_test_dir, None)


def test_value_error_if_key_missing_in_context(mocker, replay_test_dir):
    """Test that replay.load raises if the loaded context does not contain \
    'cookiecutter'."""
    with pytest.raises(ValueError):
        replay.load(replay_test_dir, 'invalid_replay')


def test_io_error_if_no_replay_file(mocker, replay_test_dir):
    """Test that replay.load raises if it cannot find a replay file."""
    with pytest.raises(IOError):
        replay.load(replay_test_dir, 'no_replay')


def test_run_json_load(
    mocker, mock_user_config, template_name, context, replay_test_dir, replay_file
):
    """Test that replay.load runs json.load under the hood and that the context \
    is correctly loaded from the file in replay_dir."""
    spy_get_replay_file = mocker.spy(replay, 'get_file_name')

    mock_json_load = mocker.patch('json.load', side_effect=json.load)

    loaded_context = replay.load(replay_test_dir, template_name)

    assert not mock_user_config.called
    spy_get_replay_file.assert_called_once_with(replay_test_dir, template_name)

    assert mock_json_load.call_count == 1
    (infile_handler,), kwargs = mock_json_load.call_args
    assert infile_handler.name == replay_file
    assert loaded_context == context
