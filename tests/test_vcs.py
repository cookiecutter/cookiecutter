#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import logging
import os
import shutil
import unittest

from cookiecutter import vcs


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class TestVCS(unittest.TestCase):

    def test_git_clone(self):
        repo_dir = vcs.git_clone('https://github.com/audreyr/cookiecutter-pypackage.git')
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))
        if os.path.isdir('cookiecutter-pypackage'):
            shutil.rmtree('cookiecutter-pypackage')

if __name__ == '__main__':
    unittest.main()
