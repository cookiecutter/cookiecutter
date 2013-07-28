#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import os
import shutil
import unittest

from cookiecutter import vcs


class TestVCS(unittest.TestCase):

    def test_git_clone(self):
        vcs.git_clone('https://github.com/audreyr/cookiecutter-pypackage.git')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))
        shutil.rmtree('cookiecutter-pypackage')

if __name__ == '__main__':
    unittest.main()
