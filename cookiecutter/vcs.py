#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.vcs
----------------

Helper functions for working with version control systems.
"""

import logging
import os
import shutil
import subprocess
import sys

from .prompt import query_yes_no


def delete_repo(repo_dir):
    """
    Asks the user whether it's okay to delete the previously-cloned repo.
    If yes, deletes it. Otherwise, Cookiecutter exits.
    :param repo_dir: Directory of previously-cloned repo.
    """

    ok_to_delete = query_yes_no("You've cloned {0} before. "
        "Is it okay to delete and re-clone it?".format(repo_dir),
        default="yes"
    )
    if ok_to_delete:
        shutil.rmtree(repo_dir)
    else:
        sys.exit()


def git_clone(repo, checkout=None):
    """
    Clone a git repo to the current directory.

    :param repo: Git repo URL ending with .git.
    :param checkout: The branch, tag or commit ID to checkout after clone
    """

    # Return repo dir
    tail = os.path.split(repo)[1]
    repo_dir = tail.rsplit('.git')[0]
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        delete_repo(repo_dir)

    os.system('git clone {0}'.format(repo))

    if checkout is not None:
        subprocess.check_call(['git', 'checkout', checkout], cwd=repo_dir)

    return repo_dir


def hg_clone(repo):
    """
    Clone a mercurial repo to the current directory.

    :param repo: repo URL ending with .hg.
    """

    # Return repo dir
    tail = os.path.split(repo)[1]
    repo_dir = tail.rsplit('.hg')[0]
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        delete_repo(repo_dir)

    os.system('hg clone {0}'.format(repo[0:-3]))

    return repo_dir
