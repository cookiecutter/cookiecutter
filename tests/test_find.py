#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_find
------------

Tests for `cookiecutter.find` module.
"""

import os
import shutil
import unittest

from cookiecutter import find


class TestFind(unittest.TestCase):

    def test_find_template(self):
        os.system('git clone https://github.com/audreyr/cookiecutter-pypackage.git')
        template = find.find_template(repo_dir='cookiecutter-pypackage')
        self.assertEqual(template, '{{project.repo_name}}')
        self.assertNotEqual(template, '{{project.repo_name }}')
        self.assertNotEqual(template, '{{ project.repo_name }}')
        shutil.rmtree('cookiecutter-pypackage')

if __name__ == '__main__':
    unittest.main()
