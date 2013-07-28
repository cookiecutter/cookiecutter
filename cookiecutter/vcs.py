#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.vcs
----------------

Helper functions for working with version control systems.
"""

import logging
import os


def git_clone(repo):
    """
    Clone a git repo to the current directory.
    
    :param repo: Git repo URL ending with .git.
    """

    os.system('git clone {0}'.format(repo))
    
    # Return repo dir
    tail = os.path.split(repo)[1]
    repo_dir = tail.rsplit('.git')[0]
    logging.info('repo_dir is {0}'.format(repo_dir))
    return repo_dir
