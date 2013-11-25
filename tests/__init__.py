#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__init__
---------

Contains testing helpers.
"""

import os
import shutil
import stat
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


def force_delete(func, path, exc_info):
    """
    Error handler for `shutil.rmtree()` equivalent to `rm -rf`
    Usage: `shutil.rmtree(path, onerror=force_delete)`
    From stackoverflow.com/questions/2656322
    """

    if not os.access(path, os.W_OK):
        # Is the error an access error?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise


class CookiecutterCleanSystemTestCase(unittest.TestCase):
    """
    Test case that simulates a clean system with no config/cloned cookiecutters.
    
    During setUp:

    * Back up the `~/.cookiecutterrc` config file to `~/.cookiecutterrc.backup`
    * Back up the `~/.cookiecutters/` dir to `~/.cookiecutters.backup/`
    * Starts off a test case with no pre-existing `~/.cookiecutterrc` or 
      `~/.cookiecutters/`

    During tearDown:

    * Delete `~/.cookiecutters/` only if a backup is present at
      `~/.cookiecutters.backup/`
    * Restore the `~/.cookiecutterrc` config file from `~/.cookiecutterrc.backup`
    * Restore the `~/.cookiecutters/` dir from `~/.cookiecutters.backup/`

    """

    def setUp(self):
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        if os.path.exists(self.user_config_path):
            self.user_config_found = True
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)
        else:
            self.user_config_found = False

        # If the default cookiecutters_dir is pre-existing, move it to a
        # temp location
        self.cookiecutters_dir = os.path.expanduser('~/.cookiecutters')
        self.cookiecutters_dir_backup = os.path.expanduser('~/.cookiecutters.backup')
        if os.path.isdir(self.cookiecutters_dir):
            self.cookiecutters_dir_found = True

            # Remove existing backups before backing up. If they exist, they're stale.
            if os.path.isdir(self.cookiecutters_dir_backup):
                shutil.rmtree(self.cookiecutters_dir_backup)

            shutil.copytree(self.cookiecutters_dir, self.cookiecutters_dir_backup)
        else:
            self.cookiecutters_dir_found = False

    def tearDown(self):
        # If it existed, restore ~/.cookiecutterrc
        # We never write to ~/.cookiecutterrc, so this logic is simpler.
        if self.user_config_found and os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)

        # Carefully delete the created ~/.cookiecutters dir only in certain
        # conditions. 
        if self.cookiecutters_dir_found:        
            # Delete the created ~/.cookiecutters dir as long as a backup exists
            if os.path.isdir(self.cookiecutters_dir) and os.path.isdir(self.cookiecutters_dir_backup):
                shutil.rmtree(self.cookiecutters_dir)
        else:
            # Delete the created ~/.cookiecutters dir.
            # There's no backup because it never existed
            if os.path.isdir(self.cookiecutters_dir):
                shutil.rmtree(self.cookiecutters_dir)
        
        # Restore the user's default cookiecutters_dir contents
        if os.path.isdir(self.cookiecutters_dir_backup):
            shutil.copytree(self.cookiecutters_dir_backup, self.cookiecutters_dir)
        if os.path.isdir(self.cookiecutters_dir):
            shutil.rmtree(self.cookiecutters_dir_backup)
