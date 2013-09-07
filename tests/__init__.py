#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
__init__
---------

Contains testing helpers.
"""

import os
import shutil
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

class CookiecutterTestCase(unittest.TestCase):
    def setUp(self):
        # If ~/.cookiecutterrc is pre-existing, move it to a temp location
        self.user_config_path = os.path.expanduser('~/.cookiecutterrc')
        self.user_config_path_backup = os.path.expanduser(
            '~/.cookiecutterrc.backup'
        )
        if os.path.exists(self.user_config_path):
            shutil.copy(self.user_config_path, self.user_config_path_backup)
            os.remove(self.user_config_path)

        # If the default cookiecutters_dir is pre-existing, move it to a
        # temp location
        self.cookiecutters_dir = os.path.expanduser('~/.cookiecutters')
        self.cookiecutters_dir_backup = os.path.expanduser('~/.cookiecutters.backup')
        if os.path.isdir(self.cookiecutters_dir):
            shutil.copytree(self.cookiecutters_dir, self.cookiecutters_dir_backup)
        if os.path.isdir(self.cookiecutters_dir_backup):
            shutil.rmtree(self.cookiecutters_dir)

    def tearDown(self):
        # Delete the created ~/.cookiecutters dir as long as a backup exists
        if os.path.isdir(self.cookiecutters_dir) and os.path.isdir(self.cookiecutters_dir_backup):
            shutil.rmtree(self.cookiecutters_dir)
    
        # If it existed, restore ~/.cookiecutterrc
        if os.path.exists(self.user_config_path_backup):
            shutil.copy(self.user_config_path_backup, self.user_config_path)
            os.remove(self.user_config_path_backup)
        
        # Restore the user's default cookiecutters_dir contents
        if os.path.isdir(self.cookiecutters_dir_backup):
            shutil.copytree(self.cookiecutters_dir_backup, self.cookiecutters_dir)
        if os.path.isdir(self.cookiecutters_dir):
            shutil.rmtree(self.cookiecutters_dir_backup)