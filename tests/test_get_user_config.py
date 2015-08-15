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


@pytest.fixture(scope='module')
def user_config_path():
    return os.path.expanduser('~/.cookiecutterrc')


@pytest.fixture(scope='function')
def back_up_rc(request, user_config_path):
    """
    Back up an existing cookiecutter rc and restore it after the test.
    If ~/.cookiecutterrc is pre-existing, move it to a temp location
    """
    user_config_path_backup = os.path.expanduser('~/.cookiecutterrc.backup')

    if os.path.exists(user_config_path):
        shutil.copy(user_config_path, user_config_path_backup)
        os.remove(user_config_path)

    def remove_test_rc():
        """
        Remove the ~/.cookiecutterrc that has been created in the test.
        """
        if os.path.exists(user_config_path):
            os.remove(user_config_path)

    def restore_original_rc():
        """
        If it existed, restore the original ~/.cookiecutterrc
        """
        if os.path.exists(user_config_path_backup):
            shutil.copy(user_config_path_backup, user_config_path)
            os.remove(user_config_path_backup)

    # According to the py.test source code finalizers are popped from an
    # internal list that we populated via 'addfinalizer'. As a result the
    # last-added finalizer function is executed first.
    request.addfinalizer(restore_original_rc)
    request.addfinalizer(remove_test_rc)


@pytest.mark.usefixtures('back_up_rc')
def test_get_user_config_valid(user_config_path):
    """
    Get config from a valid ~/.cookiecutterrc file
    """
    shutil.copy('tests/test-config/valid-config.yaml', user_config_path)
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


@pytest.mark.usefixtures('back_up_rc')
def test_get_user_config_invalid(user_config_path):
    """
    Get config from an invalid ~/.cookiecutterrc file
    """
    shutil.copy('tests/test-config/invalid-config.yaml', user_config_path)
    with pytest.raises(InvalidConfiguration):
        config.get_user_config()


@pytest.mark.usefixtures('back_up_rc')
def test_get_user_config_nonexistent():
    """
    Get config from a nonexistent ~/.cookiecutterrc file
    """
    assert config.get_user_config() == config.DEFAULT_CONFIG
