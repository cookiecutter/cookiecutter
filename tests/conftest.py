#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
conftest
--------

Contains pytest fixtures which are globally available throughout the suite.
"""

import pytest
import os
import shutil
from cookiecutter import utils


@pytest.fixture(scope='function')
def clean_system(request):
    """
    Fixture that simulates a clean system with no config/cloned cookiecutters.

    It runs code which can be regarded as setup code as known from a unittest
    TestCase. Additionally it defines a local function referring to values
    which have been stored to local variables in the setup such as the location
    of the cookiecutters on disk. This function is registered as a teardown
    hook with `request.addfinalizer` at the very end of the fixture. Pytest
    runs the named hook as soon as the fixture is out of scope, when the test
    finished to put it another way.

    During setup:

    * Back up the `~/.cookiecutterrc` config file to `~/.cookiecutterrc.backup`
    * Back up the `~/.cookiecutters/` dir to `~/.cookiecutters.backup/`
    * Starts off a test case with no pre-existing `~/.cookiecutterrc` or
      `~/.cookiecutters/`

    During teardown:

    * Delete `~/.cookiecutters/` only if a backup is present at
      `~/.cookiecutters.backup/`
    * Restore the `~/.cookiecutterrc` config file from
      `~/.cookiecutterrc.backup`
    * Restore the `~/.cookiecutters/` dir from `~/.cookiecutters.backup/`

    """

    # If ~/.cookiecutterrc is pre-existing, move it to a temp location
    user_config_path = os.path.expanduser('~/.cookiecutterrc')
    user_config_path_backup = os.path.expanduser(
        '~/.cookiecutterrc.backup'
    )
    if os.path.exists(user_config_path):
        user_config_found = True
        shutil.copy(user_config_path, user_config_path_backup)
        os.remove(user_config_path)
    else:
        user_config_found = False

    # If the default cookiecutters_dir is pre-existing, move it to a
    # temp location
    cookiecutters_dir = os.path.expanduser('~/.cookiecutters')
    cookiecutters_dir_backup = os.path.expanduser('~/.cookiecutters.backup')
    if os.path.isdir(cookiecutters_dir):
        cookiecutters_dir_found = True

        # Remove existing backups before backing up. If they exist, they're
        # stale.
        if os.path.isdir(cookiecutters_dir_backup):
            utils.rmtree(cookiecutters_dir_backup)

        shutil.copytree(cookiecutters_dir, cookiecutters_dir_backup)
    else:
        cookiecutters_dir_found = False

    def restore_backup():
        # If it existed, restore ~/.cookiecutterrc
        # We never write to ~/.cookiecutterrc, so this logic is simpler.
        if user_config_found and os.path.exists(user_config_path_backup):
            shutil.copy(user_config_path_backup, user_config_path)
            os.remove(user_config_path_backup)

        # Carefully delete the created ~/.cookiecutters dir only in certain
        # conditions.
        cookie_dir_is_dir = os.path.isdir(cookiecutters_dir)
        if cookiecutters_dir_found:
            # Delete the created ~/.cookiecutters dir as long as a backup
            # exists
            if cookie_dir_is_dir and os.path.isdir(cookiecutters_dir_backup):
                utils.rmtree(cookiecutters_dir)
        else:
            # Delete the created ~/.cookiecutters dir.
            # There's no backup because it never existed
            if cookie_dir_is_dir:
                utils.rmtree(cookiecutters_dir)

        # Restore the user's default cookiecutters_dir contents
        if os.path.isdir(cookiecutters_dir_backup):
            shutil.copytree(cookiecutters_dir_backup, cookiecutters_dir)
        if os.path.isdir(cookiecutters_dir):
            utils.rmtree(cookiecutters_dir_backup)

    request.addfinalizer(restore_backup)
