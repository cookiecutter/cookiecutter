#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_user_config
--------------------

Tests formerly known from a unittest residing in test_config.py named
TestGetUserConfig.test_get_user_config_valid
TestGetUserConfig.test_get_user_config_invalid
TestGetUserConfig.test_get_user_config_nonexistent
"""

import os
import shutil

import pytest

from cookiecutter import config
from cookiecutter.exceptions import InvalidConfiguration
from tests.utils import dir_tests


@pytest.fixture(scope='function')
def user_config_path():
    return os.path.expanduser('~/.cookiecutterrc')


# @pytest.mark.usefixtures('back_up_rc')
def test_get_user_config_valid(user_config_path):
    """
    Get config from a valid ~/.cookiecutterrc file
    """
    shutil.copy(dir_tests('test-config/valid-config.yaml'), user_config_path)
    conf = config.get_user_config()
    expected_conf = {
        'cookiecutters_dir': '/home/example/some-path-to-templates',
        'replay_dir': '/home/example/some-path-to-replay-files',
        'default_context': {
            'full_name': 'Firstname Lastname',
            'email': 'firstname.lastname@gmail.com',
            'github_username': 'example'
        }
    }
    assert conf == expected_conf


# @pytest.mark.usefixtures('back_up_rc')
def test_get_user_config_invalid(user_config_path):
    """
    Get config from an invalid ~/.cookiecutterrc file
    """
    shutil.copy(dir_tests('test-config/invalid-config.yaml'), user_config_path)
    with pytest.raises(InvalidConfiguration):
        config.get_user_config()


# @pytest.mark.usefixtures('back_up_rc')
def test_get_user_config_nonexistent():
    """
    Get config from a nonexistent ~/.cookiecutterrc file
    """
    assert config.get_user_config() == config.get_default_config()


@pytest.fixture
def custom_config():
    return {
        'cookiecutters_dir': '/foo/bar/some-path-to-templates',
        'replay_dir': '/foo/bar/some-path-to-replay-files',
        'default_context': {
            'full_name': 'Cookiemonster',
            'github_username': 'hackebrot'
        },
        'abbreviations': {
            'cookiedozer': 'https://github.com/hackebrot/cookiedozer.git',
        }
    }


@pytest.fixture
def custom_config_path(tmpdir, custom_config):
    user_config_file = tmpdir.join('user_config')

    user_config_file.write(config.yaml.dump(custom_config))
    return str(user_config_file)


def test_specify_config_path(mocker, custom_config_path, custom_config):
    spy_get_config = mocker.spy(config, 'get_config')

    user_config = config.get_user_config(custom_config_path)
    spy_get_config.assert_called_once_with(custom_config_path)

    assert user_config == custom_config


def test_default_config_path(user_config_path):
    assert config.get_user_config_path() == user_config_path


def test_default_config_from_env_variable(monkeypatch, custom_config_path, custom_config):
    monkeypatch.setenv('COOKIECUTTER_CONFIG', custom_config_path)

    user_config = config.get_user_config()
    assert user_config == custom_config


def test_force_default_config(mocker):
    spy_get_config = mocker.spy(config, 'get_config')

    user_config = config.get_user_config(None)

    assert user_config == config.get_default_config()
    assert not spy_get_config.called
