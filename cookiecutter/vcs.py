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
import subprocess
import sys

from .exceptions import UnknownRepoType
from .prompt import query_yes_no
from .utils import make_sure_path_exists, rmtree


def prompt_and_delete_repo(repo_dir):
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
        rmtree(repo_dir)
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
        raise UnknownRepoType


def clone(repo_url, checkout=None, clone_to_dir="."):
    """
    Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone
    """

    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    repo_type = identify_repo(repo_url)

    tail = os.path.split(repo_url)[1]
    if repo_type == "git":
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail.rsplit('.git')[0]))
    elif repo_type == "hg":
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, tail))
    logging.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        prompt_and_delete_repo(repo_dir)

    if repo_type in ["git", "hg"]:
        subprocess.check_call([repo_type, 'clone', repo_url], cwd=clone_to_dir)
        if checkout is not None:
            subprocess.check_call([repo_type, 'checkout', checkout], cwd=repo_dir)

    return repo_dir
