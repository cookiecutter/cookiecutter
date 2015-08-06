# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

import json
import os
import pytest


from cookiecutter import replay
from cookiecutter.config import get_user_config


@pytest.fixture
def replay_dir():
    return os.path.expanduser('~/.cookiecutter_replay/')


def test_get_user_config(mocker, replay_dir):
    mocker.patch('os.path.exists', return_value=False)
    config_dict = get_user_config()
    assert 'replay_dir' in config_dict

    assert config_dict['replay_dir'] == replay_dir


@pytest.fixture
def template_name():
    return 'cookiedozer'


@pytest.fixture
def context():
    return {
        u'email': u'raphael@hackebrot.de',
        u'full_name': u'Raphael Pierzina',
        u'github_username': u'hackebrot',
        u'version': u'0.1.0',
    }


def test_dump_value_error_if_no_template_name(context):
    with pytest.raises(ValueError):
        replay.dump(None, context)


def test_dump_type_error_if_not_dict_context(template_name):
    with pytest.raises(TypeError):
        replay.dump(template_name, 'not_a_dict')


def test_raise_if_replay_dir_creation_fails(
        mocker, template_name, context, replay_dir):
    mock_ensure = mocker.patch(
        'cookiecutter.replay.make_sure_path_exists',
        return_value=False
    )
    with pytest.raises(IOError):
        replay.dump(template_name, context)

    mock_ensure.assert_called_once_with(replay_dir)


def test_run_json_dump(
        mocker, template_name, context, replay_dir):
    spy_ensure = mocker.spy(
        'cookiecutter.replay.make_sure_path_exists',
    )

    replay.dump(template_name, context)

    spy_ensure.assert_called_once_with(replay_dir)

    replay_dir = os.path.expanduser('~/.cookiecutter_replay/')
    replay_file = os.path.join(replay_dir, template_name)

    with open(replay_file, 'r') as f:
        dumped_context = json.load(f)
        assert dumped_context == context
