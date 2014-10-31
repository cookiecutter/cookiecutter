#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import locale
import logging
import os
import subprocess

from cookiecutter.compat import patch, unittest
from cookiecutter import exceptions, utils, vcs

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False


# Log debug and above to console
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
encoding = locale.getdefaultlocale()[1]


class TestIdentifyRepo(unittest.TestCase):

    def test_identify_git_github(self):
        repo_url = "https://github.com/audreyr/cookiecutter-pypackage.git"
        self.assertEqual(vcs.identify_repo(repo_url), "git")

    def test_identify_git_github_no_extension(self):
        repo_url = "https://github.com/audreyr/cookiecutter-pypackage"
        self.assertEqual(vcs.identify_repo(repo_url), "git")

    def test_identify_git_gitorious(self):
        repo_url = "git@gitorious.org:cookiecutter-gitorious/cookiecutter-gitorious.git"
        self.assertEqual(vcs.identify_repo(repo_url), "git")

    def test_identify_hg_mercurial(self):
        repo_url = "https://audreyr@bitbucket.org/audreyr/cookiecutter-bitbucket"
        self.assertEqual(vcs.identify_repo(repo_url), "hg")

    def test_unknown_repo_type(self):
        repo_url = "http://norepotypespecified.com"
        self.assertRaises(
            exceptions.UnknownRepoType,
            vcs.identify_repo,
            repo_url
        )


@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub/Bitbucket.')
class TestVCS(unittest.TestCase):

    def test_git_clone(self):
        repo_dir = vcs.clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')

    def test_git_clone_checkout(self):
        repo_dir = vcs.clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git',
            'console-script'
        )
        git_dir = 'cookiecutter-pypackage'
        self.assertEqual(repo_dir, git_dir)
        self.assertTrue(os.path.isfile(os.path.join('cookiecutter-pypackage', 'README.rst')))

        proc = subprocess.Popen(
            ['git', 'symbolic-ref', 'HEAD'],
            cwd=git_dir,
            stdout=subprocess.PIPE
        )
        symbolic_ref = proc.communicate()[0]
        branch = symbolic_ref.decode(encoding).strip().split('/')[-1]
        self.assertEqual('console-script', branch)

        if os.path.isdir(git_dir):
            utils.rmtree(git_dir)

    def test_git_clone_custom_dir(self):
        os.makedirs("tests/custom_dir1/custom_dir2/")
        repo_dir = vcs.clone(
            repo_url='https://github.com/audreyr/cookiecutter-pypackage.git',
            checkout=None,
            clone_to_dir="tests/custom_dir1/custom_dir2/"
        )
        with utils.work_in("tests/custom_dir1/custom_dir2/"):
            test_dir = 'tests/custom_dir1/custom_dir2/cookiecutter-pypackage'.replace("/", os.sep)
            self.assertEqual(repo_dir, test_dir)
            self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))
            if os.path.isdir('cookiecutter-pypackage'):
                utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('tests/custom_dir1'):
            utils.rmtree('tests/custom_dir1')

    def test_hg_clone(self):
        repo_dir = vcs.clone(
            'https://bitbucket.org/pokoli/cookiecutter-trytonmodule'
        )
        self.assertEqual(repo_dir, 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.isfile('cookiecutter-trytonmodule/README.rst'))
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')

    @patch('cookiecutter.vcs.identify_repo', lambda x: u'stringthatisntashellcommand')
    def test_vcs_not_installed(self):
        self.assertRaises(
            exceptions.VCSNotInstalled,
            vcs.clone,
            "http://norepotypespecified.com"
        )


@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub/Bitbucket.')
class TestVCSPrompt(unittest.TestCase):

    def setUp(self):
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        os.mkdir('cookiecutter-pypackage/')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')
        os.mkdir('cookiecutter-trytonmodule/')

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'y')
    def test_git_clone_overwrite(self):
        repo_dir = vcs.clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))

    def test_git_clone_overwrite_with_no_prompt(self):
        repo_dir = vcs.clone(
            'https://github.com/audreyr/cookiecutter-pypackage.git',
            no_input=True
        )
        self.assertEqual(repo_dir, 'cookiecutter-pypackage')
        self.assertTrue(os.path.isfile('cookiecutter-pypackage/README.rst'))

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'n')
    def test_git_clone_cancel(self):
        self.assertRaises(
            SystemExit,
            vcs.clone,
            'https://github.com/audreyr/cookiecutter-pypackage.git'
        )

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'y')
    def test_hg_clone_overwrite(self):
        repo_dir = vcs.clone(
            'https://bitbucket.org/pokoli/cookiecutter-trytonmodule'
        )
        self.assertEqual(repo_dir, 'cookiecutter-trytonmodule')
        self.assertTrue(os.path.isfile('cookiecutter-trytonmodule/README.rst'))

    @patch('cookiecutter.prompt.read_response', lambda x=u'': u'n')
    def test_hg_clone_cancel(self):
        self.assertRaises(
            SystemExit,
            vcs.clone,
            'https://bitbucket.org/pokoli/cookiecutter-trytonmodule'
        )

    def tearDown(self):
        if os.path.isdir('cookiecutter-pypackage'):
            utils.rmtree('cookiecutter-pypackage')
        if os.path.isdir('cookiecutter-trytonmodule'):
            utils.rmtree('cookiecutter-trytonmodule')


class TestIsVCSInstalled(unittest.TestCase):

    def test_existing_repo_type(self):
        self.assertTrue(
            vcs.is_vcs_installed("git"),
        )

    def test_non_existing_repo_type(self):
        self.assertFalse(
            vcs.is_vcs_installed("stringthatisntashellcommand")
        )


if __name__ == '__main__':
    unittest.main()
