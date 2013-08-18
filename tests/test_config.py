#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_config
-----------

Tests for `cookiecutter.config` module.
"""

import sys
import unittest

from cookiecutter import config

PY3 = sys.version > '3'
if PY3:
    from unittest.mock import patch
    input_str = 'builtins.input'
else:
    from mock import patch
    input_str = '__builtin__.raw_input'

if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest

class TestJsonHelpers(unittest.TestCase):

	test_file = 'tests/config/test-config.json'
	with open(test_file) as f:
		json_str = f.read()

	json_obj = {
		'foo': 'bar',
		'baz': {
			'stuff': 'thing'
		}
	}

	def test_parse_commented_json(self):
		""" Ignore comments in a json string """
		self.assertEqual(
			config._json_parse(self.json_str),
			self.json_obj
		)

	def test_open_commented_json(self):
		""" Open and parse a json file containing comments """
		self.assertEqual(
			config._json_open(self.test_file),
			self.json_obj
		)


class TestConfig(unittest.TestCase):

	def test_foo(self): self.fail('TODO')


if __name__ == '__main__':
    unittest.main()