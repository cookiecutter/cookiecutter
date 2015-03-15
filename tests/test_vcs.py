#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vcs
------------

Tests for `cookiecutter.vcs` module.
"""

import locale
import os
import subprocess
import unittest

from cookiecutter.compat import patch
from cookiecutter import exceptions, utils, vcs
from tests.skipif_markers import skipif_no_network

try:
    no_network = os.environ[u'DISABLE_NETWORK_TESTS']
except KeyError:
    no_network = False


encoding = locale.getdefaultlocale()[1]

@skipif_no_network
def test_git_clone():
    repo_dir = vcs.clone(
        'https://github.com/audreyr/cookiecutter-pypackage.git'
    )

    assert repo_dir == 'cookiecutter-pypackage'
    assert os.path.isfile('cookiecutter-pypackage/README.rst')

    if os.path.isdir('cookiecutter-pypackage'):
        utils.rmtree('cookiecutter-pypackage')


@unittest.skipIf(condition=no_network, reason='Needs a network connection to GitHub/Bitbucket.')
class TestVCS(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
