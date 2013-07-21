#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate
--------------

Tests for `cookiecutter.generate` module.
"""

import os
import shutil
import unittest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment

from cookiecutter import generate


class TestGenerate(unittest.TestCase):

    def test_generate_files(self):
        generate.generate_files(
            context={'food': 'pizza'},
            input_dir='tests/input',
            output_dir='tests/output'
        )
        self.assertTrue(os.path.isfile('tests/output/simple.txt'))
        simple_text = open('tests/output/simple.txt', 'rt').read()
        self.assertEqual(simple_text, 'I eat pizza')

    def test_generate_context(self):
        context = generate.generate_context(json_dir='tests/json')
        self.assertEqual(context, {"test": {"1": 2}})

    def test_output_folder(self):
        context = generate.generate_context(json_dir='tests/json2')
        generate.generate_files(
            context=context,
            input_dir='tests/input2',
            output_dir='tests/output2'
        )
        
        something = """Hi!
My name is Audrey Greenfeld.
It is 2014."""
        something2 = open('tests/output2/something.txt').read()
        self.assertEqual(something, something2)
        
        in_folder = "The color is green and the letter is D."
        in_folder2 = open('tests/output2/folder/in_folder.txt').read()
        self.assertEqual(in_folder, in_folder2)
        
        self.assertTrue(os.path.isdir('tests/output2/im_a.dir'))
        self.assertTrue(os.path.isfile('tests/output2/im_a.dir/im_a.file.py'))

    def tearDown(self):
        if os.path.exists('tests/output'):
            shutil.rmtree('tests/output')
        if os.path.exists('tests/output2'):
            shutil.rmtree('tests/output2')

if __name__ == '__main__':
    unittest.main()
