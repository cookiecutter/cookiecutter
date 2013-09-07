#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.vcs
----------------

Helper functions for working with version control systems.
"""

from __future__ import unicode_literals
import logging
import os
import shutil
import subprocess
import sys

from .prompt import query_yes_no
from .utils import make_sure_path_exists


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


def identify_repo(repo_url):
    """
    Determines if `repo_url` should be treated as a URL to a git or hg repo.
    :param repo_url: Repo URL of unknown type.
    :returns: "git", "hg", or None.
    """
    
    if "git" in repo_url:
        return "git"
    elif "bitbucket" in repo_url:
        return "hg"
    else:
        return None


def clone(repo_url, checkout=None, clone_to_dir="."):
    """
    Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone
    """

    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    # Return repo dir
    tail = os.path.split(repo)[1]
    repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail.rsplit('.git')[0]))
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        delete_repo(repo_dir)

    subprocess.check_call(['git', 'clone', repo], cwd=clone_to_dir)

    if checkout is not None:
        subprocess.check_call(['git', 'checkout', checkout], cwd=repo_dir)

    return repo_dir


def git_clone(repo, checkout=None, clone_to_dir="."):
    """
    Clone a git repo to the current directory.

    :param repo: Git repo URL ending with .git.
    :param checkout: The branch, tag or commit ID to checkout after clone
    """
    
    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    # Return repo dir
    tail = os.path.split(repo)[1]
    repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail.rsplit('.git')[0]))
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        delete_repo(repo_dir)

    subprocess.check_call(['git', 'clone', repo], cwd=clone_to_dir)

    if checkout is not None:
        subprocess.check_call(['git', 'checkout', checkout], cwd=repo_dir)

    return repo_dir


def hg_clone(repo, clone_to_dir="."):
    """
    Clone a mercurial repo to the current directory.

    :param repo: repo URL ending with .hg.
    """

    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    # Return repo dir
    tail = os.path.split(repo)[1]
    repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail.rsplit('.hg')[0]))
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        delete_repo(repo_dir)

    # os.system('hg clone {0}'.format(repo[0:-3]))
    subprocess.check_call(['hg', 'clone', repo[0:-3]], cwd=clone_to_dir)

    return repo_dir
