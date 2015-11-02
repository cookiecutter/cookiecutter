# -*- coding: utf-8 -*-

import pytest

from cookiecutter import config_parser


@pytest.fixture
def user_config():
    return """default_context:
    full_name: "Audrey Roy"
    email: "audreyr@gmail.com"
    github_username: "audreyr"
cookiecutters_dir: "/home/audreyr/my-custom-cookiecutters-dir/"
replay_dir: "/home/audreyr/my-custom-replay-dir/"
abbreviations:
    pp: https://github.com/audreyr/cookiecutter-pypackage.git
    gh: https://github.com/{0}.git
    bb: https://bitbucket.org/{0}
"""


@pytest.fixture
def expected_config():
    return {
        'default_context': {
            'full_name': 'Audrey Roy',
            'email': 'audreyr@gmail.com',
            'github_username': 'audreyr',
        },
        'cookiecutters_dir': "/home/audreyr/my-custom-cookiecutters-dir/",
        'replay_dir': "/home/audreyr/my-custom-replay-dir/",
        'abbreviations': {
            'pp': "https://github.com/audreyr/cookiecutter-pypackage.git",
            'gh': "https://github.com/{0}.git",
            'bb': "https://bitbucket.org/{0}"
        }
    }


def test_parse_config(user_config, expected_config):
    assert config_parser.loads(user_config) == expected_config


def test_find_simple(user_config):
    result = config_parser.find_simple(user_config)
    expected = {
        'cookiecutters_dir': "/home/audreyr/my-custom-cookiecutters-dir/",
        'replay_dir': "/home/audreyr/my-custom-replay-dir/",
    }
    assert result == expected


def test_find_nested(user_config):
    result = config_parser.find_nested(user_config)
    expected = {
        'default_context': {
            'full_name': 'Audrey Roy',
            'email': 'audreyr@gmail.com',
            'github_username': 'audreyr',
        },
        'abbreviations': {
            'pp': "https://github.com/audreyr/cookiecutter-pypackage.git",
            'gh': "https://github.com/{0}.git",
            'bb': "https://bitbucket.org/{0}"
        }
    }
    assert result == expected
