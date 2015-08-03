# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""


def test_get_user_config():
    config_dict = get_user_config()
    assert 'replay_dir' in config_dict

    expected_dir = os.path.expanduser('~/.cookiecutter_replay/')
    assert config_dict['replay_dir'] == expected_dir
