#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.find
-----------------

Functions for finding Cookiecutter templates and other components.
"""

import os


def find_template(repo_dir):
    """
    Determines which child directory of `repo_dir` is the project template.
    
    :param repo_dir: Local directory of newly cloned repo.
    """

    contents_set = set(os.listdir(repo_dir))
    exclude_set = set(['.DS_Store', '.git', '.gitignore', 'README.rst', 'json'])
    
    # Subtract set of excludes from contents.
    contents_set -= exclude_set

    if len(contents_set) == 1:
        return contents_set.pop()
    return False
