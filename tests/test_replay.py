# -*- coding: utf-8 -*-

"""
test_replay
-----------
"""

import os
import pytest


from cookiecutter import replay
from cookiecutter.config import get_user_config


def test_get_user_config():
    config_dict = get_user_config()
    assert 'replay_dir' in config_dict

    expected_dir = os.path.expanduser('~/.cookiecutter_replay/')
    assert config_dict['replay_dir'] == expected_dir


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
