#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_user_config
--------------------

Tests formerly known from a unittest residing in test_config.py named
"""

import os
import shutil
import pytest


@pytest.fixture(scope='function')
def back_up_rc(request):
    """
    Back up an existing cookiecutter rc and restore it after the test.
    If ~/.cookiecutterrc is pre-existing, move it to a temp location
    """
    user_config_path = os.path.expanduser('~/.cookiecutterrc')
    user_config_path_backup = os.path.expanduser(
        '~/.cookiecutterrc.backup'
    )

    if os.path.exists(user_config_path):
        shutil.copy(user_config_path, user_config_path_backup)
        os.remove(user_config_path)

    def restore_rc():
        """
        If it existed, restore ~/.cookiecutterrc
        """
        if os.path.exists(user_config_path_backup):
            shutil.copy(user_config_path_backup, user_config_path)
            os.remove(user_config_path_backup)
    request.addfinalizer(restore_rc)
