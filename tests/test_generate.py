#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_generate
--------------

Tests for `cookiecutter.generate` module.
"""
from __future__ import unicode_literals
import logging
import os
import io
import sys
import stat
import unittest

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from jinja2.exceptions import TemplateSyntaxError

from cookiecutter import generate
from cookiecutter import exceptions
from cookiecutter import utils
from tests import CookiecutterCleanSystemTestCase


PY3 = sys.version > '3'

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class TestGenerateFile(unittest.TestCase):

    def test_generate_file(self):
        env = Environment()
        env.loader = FileSystemLoader('.')
        infile = 'tests/files/{{generate_file}}.txt'
        generate.generate_file(
            project_dir=".",
            infile=infile,
            context={'generate_file': 'cheese'},
            env=env
        )
        self.assertTrue(os.path.isfile('tests/files/cheese.txt'))
        with open('tests/files/cheese.txt', 'rt') as f:
            generated_text = f.read()
            self.assertEqual(generated_text, 'Testing cheese')

    def test_generate_file_verbose_template_syntax_error(self):
        env = Environment()
        env.loader = FileSystemLoader('.')
        try:
            generate.generate_file(
                project_dir=".",
                infile='tests/files/syntax_error.txt',
                context={'syntax_error': 'syntax_error'},
                env=env
            )
        except TemplateSyntaxError as exception:
            expected = (
                'Missing end of comment tag\n'
                '  File "./tests/files/syntax_error.txt", line 1\n'
                '    I eat {{ syntax_error }} {# this comment is not closed}'
            )
            expected = expected.replace("/", os.sep)
            self.assertEquals(str(exception), expected)
        except exception:
            self.fail('Unexpected exception thrown:', exception)
        else:
            self.fail('TemplateSyntaxError not thrown')

    def tearDown(self):
        if os.path.exists('tests/files/cheese.txt'):
            os.remove('tests/files/cheese.txt')


class TestGenerateFiles(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        if os.path.exists('inputpizzä'):
            utils.rmtree('inputpizzä')
        if os.path.exists('inputgreen'):
            utils.rmtree('inputgreen')
        if os.path.exists('inputbinary_files'):
            utils.rmtree('inputbinary_files')
        if os.path.exists('tests/custom_output_dir'):
            utils.rmtree('tests/custom_output_dir')
        if os.path.exists('inputpermissions'):
            utils.rmtree('inputpermissions')
        super(TestGenerateFiles, self).tearDown()

    def test_generate_files_nontemplated_exception(self):
        self.assertRaises(
            exceptions.NonTemplatedInputDirException,
            generate.generate_files,
            context={
                'cookiecutter': {'food': 'pizza'}
            },
            repo_dir='tests/test-generate-files-nontemplated'
        )

    def test_generate_files(self):
        generate.generate_files(
            context={
                'cookiecutter': {'food': 'pizzä'}
            },
            repo_dir='tests/test-generate-files'
        )
        self.assertTrue(os.path.isfile('inputpizzä/simple.txt'))
        simple_text = io.open('inputpizzä/simple.txt', 'rt', encoding='utf-8').read()
        self.assertEqual(simple_text, u'I eat pizzä')

    def test_generate_files_binaries(self):
        generate.generate_files(
            context={
                'cookiecutter': {'binary_test': 'binary_files'}
            },
            repo_dir='tests/test-generate-binaries'
        )
        self.assertTrue(os.path.isfile('inputbinary_files/logo.png'))
        self.assertTrue(os.path.isfile('inputbinary_files/.DS_Store'))
        self.assertTrue(os.path.isfile('inputbinary_files/readme.txt'))
        self.assertTrue(
            os.path.isfile('inputbinary_files/some_font.otf')
        )
        self.assertTrue(
            os.path.isfile('inputbinary_files/binary_files/logo.png')
        )
        self.assertTrue(
            os.path.isfile('inputbinary_files/binary_files/.DS_Store')
        )
        self.assertTrue(
            os.path.isfile('inputbinary_files/binary_files/readme.txt')
        )
        self.assertTrue(
            os.path.isfile('inputbinary_files/binary_files/some_font.otf')
        )
        self.assertTrue(
            os.path.isfile('inputbinary_files/binary_files/binary_files/logo.png')
        )

    def test_generate_files_absolute_path(self):
        generate.generate_files(
            context={
                'cookiecutter': {'food': 'pizzä'}
            },
            repo_dir=os.path.abspath('tests/test-generate-files')
        )
        self.assertTrue(os.path.isfile('inputpizzä/simple.txt'))

    def test_generate_files_output_dir(self):
        os.mkdir('tests/custom_output_dir')
        generate.generate_files(
            context={
                'cookiecutter': {'food': 'pizzä'}
            },
            repo_dir=os.path.abspath('tests/test-generate-files'),
            output_dir='tests/custom_output_dir'
        )
        self.assertTrue(os.path.isfile('tests/custom_output_dir/inputpizzä/simple.txt'))

    def test_generate_files_permissions(self):
        """
        simple.txt and script.sh should retain their respective 0o644 and
        0o755 permissions
        """
        generate.generate_files(
            context={
                'cookiecutter': {'permissions': 'permissions'}
            },
            repo_dir='tests/test-generate-files-permissions'
        )

        self.assertTrue(os.path.isfile('inputpermissions/simple.txt'))

        # simple.txt should still be 0o644
        self.assertEquals(
            os.stat('tests/test-generate-files-permissions/input{{cookiecutter.permissions}}/simple.txt').st_mode & 0o777,
            os.stat('inputpermissions/simple.txt').st_mode & 0o777
        )

        self.assertTrue(os.path.isfile('inputpermissions/script.sh'))

        # script.sh should still be 0o755
        self.assertEquals(
            os.stat('tests/test-generate-files-permissions/input{{cookiecutter.permissions}}/script.sh').st_mode & 0o777,
            os.stat('inputpermissions/script.sh').st_mode & 0o777
        )


class TestGenerateContext(CookiecutterCleanSystemTestCase):

    def test_generate_context(self):
        context = generate.generate_context(
            context_file='tests/test-generate-context/test.json'
        )
        self.assertEqual(context, {"test": {"1": 2, "some_key": "some_val"}})

    def test_generate_context_with_default(self):
        context = generate.generate_context(
            context_file='tests/test-generate-context/test.json',
            default_context={"1": 3}
        )
        self.assertEqual(context, {"test": {"1": 3, "some_key": "some_val"}})


class TestOutputFolder(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        if os.path.exists('output_folder'):
            utils.rmtree('output_folder')
        super(TestOutputFolder, self).tearDown()

    def test_output_folder(self):
        context = generate.generate_context(
            context_file='tests/test-output-folder/cookiecutter.json'
        )
        logging.debug('Context is {0}'.format(context))
        generate.generate_files(
            context=context,
            repo_dir='tests/test-output-folder'
        )

        something = """Hi!
My name is Audrey Greenfeld.
It is 2014."""
        something2 = open('output_folder/something.txt').read()
        self.assertEqual(something, something2)

        in_folder = "The color is green and the letter is D."
        in_folder2 = open('output_folder/folder/in_folder.txt').read()
        self.assertEqual(in_folder, in_folder2)

        self.assertTrue(os.path.isdir('output_folder/im_a.dir'))
        self.assertTrue(os.path.isfile('output_folder/im_a.dir/im_a.file.py'))


def make_test_repo(name):
    hooks = os.path.join(name, 'hooks')
    template = os.path.join(name, 'input{{cookiecutter.shellhooks}}')
    os.mkdir(name)
    os.mkdir(hooks)
    os.mkdir(template)

    with open(os.path.join(template, 'README.rst'), 'w') as f:
        f.write("foo\n===\n\nbar\n")

    if sys.platform.startswith('win'):
        filename = os.path.join(hooks, 'pre_gen_project.bat')
        with open(filename, 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo pre generation hook\n")
            f.write("echo. >shell_pre.txt\n")

        filename = os.path.join(hooks, 'post_gen_project.bat')
        with open(filename, 'w') as f:
            f.write("@echo off\n")
            f.write("\n")
            f.write("echo post generation hook\n")
            f.write("echo. >shell_post.txt\n")
    else:
        filename = os.path.join(hooks, 'pre_gen_project.sh')
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'pre generation hook';\n")
            f.write("touch 'shell_pre.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)

        filename = os.path.join(hooks, 'post_gen_project.sh')
        with open(filename, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("\n")
            f.write("echo 'post generation hook';\n")
            f.write("touch 'shell_post.txt'\n")
        # Set the execute bit
        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR)


class TestHooks(CookiecutterCleanSystemTestCase):

    def tearDown(self):
        if os.path.exists('tests/test-pyhooks/inputpyhooks'):
            utils.rmtree('tests/test-pyhooks/inputpyhooks')
        if os.path.exists('inputpyhooks'):
            utils.rmtree('inputpyhooks')
        if os.path.exists('tests/test-shellhooks'):
            utils.rmtree('tests/test-shellhooks')
        super(TestHooks, self).tearDown()

    def test_ignore_hooks_dirs(self):
        generate.generate_files(
            context={
                'cookiecutter' : {'pyhooks': 'pyhooks'}
            },
            repo_dir='tests/test-pyhooks/',
            output_dir='tests/test-pyhooks/'
        )
        self.assertFalse(os.path.exists('tests/test-pyhooks/inputpyhooks/hooks'))

    def test_run_python_hooks(self):
        generate.generate_files(
            context={
                'cookiecutter' : {'pyhooks': 'pyhooks'}
            },
            repo_dir='tests/test-pyhooks/'.replace("/", os.sep),
            output_dir='tests/test-pyhooks/'.replace("/", os.sep)
        )
        self.assertTrue(os.path.exists('tests/test-pyhooks/inputpyhooks/python_pre.txt'))
        self.assertTrue(os.path.exists('tests/test-pyhooks/inputpyhooks/python_post.txt'))

    def test_run_python_hooks_cwd(self):
        generate.generate_files(
            context={
                'cookiecutter' : {'pyhooks': 'pyhooks'}
            },
            repo_dir='tests/test-pyhooks/'
        )
        self.assertTrue(os.path.exists('inputpyhooks/python_pre.txt'))
        self.assertTrue(os.path.exists('inputpyhooks/python_post.txt'))

    def test_run_shell_hooks(self):
        make_test_repo('tests/test-shellhooks')
        generate.generate_files(
            context={
                'cookiecutter' : {'shellhooks': 'shellhooks'}
            },
            repo_dir='tests/test-shellhooks/',
            output_dir='tests/test-shellhooks/'
        )
        self.assertTrue(os.path.exists('tests/test-shellhooks/inputshellhooks/shell_pre.txt'))
        self.assertTrue(os.path.exists('tests/test-shellhooks/inputshellhooks/shell_post.txt'))


if __name__ == '__main__':
    unittest.main()
