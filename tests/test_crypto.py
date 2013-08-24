#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_crypto
-----------

Tests for `cookiecutter.crypto` module.
"""

from __future__ import unicode_literals
import random
import sys

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from cookiecutter.crypto import system_random, get_secret_key


class TestSystemRandom(unittest.TestCase):

    def test_system_random(self):
        """
        test that the random.SystemRandom() class is provided in system_random.
        """
        self.assertTrue(isinstance(system_random, random.SystemRandom))

    def test_no_system_random(self):
        """
        test that the random.SystemRandom() function is not used.

            - Provides a warning to users
            - Returns "CHANGEME"
        """
        key = get_secret_key(system_random=None)
        self.assertEqual("CHANGEME!!!", key)
