# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

import json
import os
import pytest


from cookiecutter import replay, utils
from cookiecutter.config import get_user_config


@pytest.fixture
def replay_dir():
    """Fixture to return the expected replay directory."""
    return os.path.expanduser('~/.cookiecutter_replay/')


def test_get_user_config(mocker, replay_dir):
    """Test that get_user_config holds the correct replay_dir."""
    mocker.patch('os.path.exists', return_value=False)
    config_dict = get_user_config()
    assert 'replay_dir' in config_dict

    assert config_dict['replay_dir'] == replay_dir


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


def test_dump_value_error_if_no_template_name(context):
    """Test that replay.dump raises if the tempate_name is not a valid str."""
    with pytest.raises(ValueError):
        replay.dump(None, context)


def test_dump_type_error_if_not_dict_context(template_name):
    """Test that replay.dump raises if the context is not of type dict."""
    with pytest.raises(TypeError):
        replay.dump(template_name, 'not_a_dict')


@pytest.fixture
def cleanup_replay_dir(request, replay_dir):
    """Fixture to remove the replay_dir that is created by replay.dump."""
    def remove_dir():
        if os.path.isdir(replay_dir):
            utils.rmtree(replay_dir)
    request.addfinalizer(remove_dir)


@pytest.mark.usefixtures('cleanup_replay_dir')
def test_raise_if_replay_dir_creation_fails(
        mocker, template_name, context, replay_dir):
    """Test that replay.dump raises when the replay_dir cannot be created."""
    mock_ensure = mocker.patch(
        'cookiecutter.replay.make_sure_path_exists',
        return_value=False
    )
    with pytest.raises(IOError):
        replay.dump(template_name, context)

    mock_ensure.assert_called_once_with(replay_dir)


@pytest.mark.usefixtures('cleanup_replay_dir')
def test_run_json_dump(
        mocker, template_name, context, replay_dir):
    """Test that replay.dump runs json.dump under the hood and that the context
    is correctly written to the expected file in the replay_dir.
    """
    spy_ensure = mocker.spy(
        'cookiecutter.replay.make_sure_path_exists',
    )
    spy_json_dump = mocker.spy('json.dump')

    mock_get_user_config = mocker.patch(
        'cookiecutter.config.get_user_config',
        return_value=replay_dir
    )

    replay.dump(template_name, context)

    spy_ensure.assert_called_once_with(replay_dir)
    assert spy_json_dump.called == 1
    assert mock_get_user_config.called == 1

    replay_dir = os.path.expanduser('~/.cookiecutter_replay/')
    replay_file = os.path.join(replay_dir, template_name)

    with open(replay_file, 'r') as f:
        dumped_context = json.load(f)
        assert dumped_context == context
