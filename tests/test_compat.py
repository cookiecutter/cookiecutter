#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_compat
------------

Tests for `cookiecutter.compat` module.
"""

import unittest
from cookiecutter.compat import which


class TestWhich(unittest.TestCase):

    def test_existing_command(self):
        self.assertTrue(
            which('cookiecutter')
        )

    def test_non_existing_command(self):
        self.assertFalse(
            which('stringthatisntashellcommand')
        )

if __name__ == '__main__':
    unittest.main()
