# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

import pytest


from cookiecutter import replay, config


@pytest.fixture
def replay_test_dir():
    return 'tests/test-replay/'


@pytest.fixture
def mock_user_config(mocker, replay_test_dir):
    user_config = config.DEFAULT_CONFIG
    user_config.update({'replay_dir': replay_test_dir})

    return mocker.patch(
        'cookiecutter.replay.get_user_config', return_value=user_config
    )


def test_get_replay_file_name():
    """Make sure that replay.get_file_name generates a valid json file path."""
    assert replay.get_file_name('foo', 'bar') == 'foo/bar.json'


@pytest.fixture
def template_name():
    """Fixture to return a valid template_name."""
    return 'cookiedozer'


@pytest.fixture
def context():
    """Fixture to return a valid context as known from a cookiecutter.json."""
    return {
        u'email': u'raphael@hackebrot.de',
        u'full_name': u'Raphael Pierzina',
        u'github_username': u'hackebrot',
        u'version': u'0.1.0',
    }


def test_dump_type_error_if_no_template_name(context):
    """Test that replay.dump raises if the tempate_name is not a valid str."""
    with pytest.raises(TypeError):
        replay.dump(None, context)


def test_dump_type_error_if_not_dict_context(template_name):
    """Test that replay.dump raises if the context is not of type dict."""
    with pytest.raises(TypeError):
        replay.dump(template_name, 'not_a_dict')


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


def test_dump_ioerror_if_replay_dir_creation_fails(
        mock_ensure_failure, mock_user_config, replay_test_dir):
    """Test that replay.dump raises when the replay_dir cannot be created."""

    with pytest.raises(IOError):
        replay.dump('foo', {'hello': 'world'})

    mock_ensure_failure.assert_called_once_with(replay_test_dir)


def test_dump_run_json_dump(mocker, mock_ensure_success, mock_user_config,
                            template_name, context, replay_test_dir):
    """Test that replay.dump runs json.dump under the hood and that the context
    is correctly written to the expected file in the replay_dir.
    """
    spy_get_replay_file = mocker.spy(replay, 'get_file_name')

    mock_json_dump = mocker.patch('json.dump')

    replay.dump(template_name, context)

    assert mock_user_config.call_count == 1
    mock_ensure_success.assert_called_once_with(replay_test_dir)
    spy_get_replay_file.assert_called_once_with(replay_test_dir, template_name)

    replay_file = replay.get_file_name(replay_test_dir, template_name)

    assert mock_json_dump.call_count == 1
    (dumped_context, outfile_handler), kwargs = mock_json_dump.call_args
    assert outfile_handler.name == replay_file
    assert dumped_context == context


def test_load_type_error_if_no_template_name():
    """Test that replay.load raises if the tempate_name is not a valid str."""
    with pytest.raises(TypeError):
        replay.load(None)


def test_load_run_json_load(mocker, mock_user_config, template_name,
                            context, replay_test_dir):
    """Test that replay.load runs json.load under the hood and that the context
    is correctly loaded from the file in replay_dir.
    """
    spy_get_replay_file = mocker.spy(replay, 'get_file_name')

    mock_json_load = mocker.patch('json.load', return_value=context)

    loaded_context = replay.load(template_name)

    assert mock_user_config.call_count == 1
    spy_get_replay_file.assert_called_once_with(replay_test_dir, template_name)

    replay_file = replay.get_file_name(replay_test_dir, template_name)

    assert mock_json_load.call_count == 1
    (infile_handler,), kwargs = mock_json_load.call_args
    assert infile_handler.name == replay_file
    assert loaded_context == context
