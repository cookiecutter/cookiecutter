#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_user_config
--------------------

Tests formerly known from a unittest residing in test_config.py named
"""

import pytest


@pytest.fixture(scope='function')
def back_up_rc(request):
    """
    Back up an existing cookiecutter rc and restore it after the test.
    If ~/.cookiecutterrc is pre-existing, move it to a temp location
    """
    self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
    self.user_config_path_backup = os.path.expanduser(
        '~/.cookiecutterrc.backup'
    )

    if os.path.exists(self.user_config_path):
        shutil.copy(self.user_config_path, self.user_config_path_backup)
        os.remove(self.user_config_path)

    def restore_rc():
        """
        If it existed, restore ~/.cookiecutterrc
        """
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)
    request.addfinalizer(restore_rc)
