#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.cleanup
--------------------

Functions for cleaning up after Cookiecutter project generation occurs.
"""

import os
import shutil


def remove_repo(repo_dir, generated_project):
    """
    Move the generated project to the same level as `repo_dir`, then delete
    `repo_dir`.
    
    Called when Cookiecutter receives a repo as an argument instead of a
    project template directory.

    :param repo_dir: Local directory of the cloned repo.
    :param generated_project: Name of project that Cookiecutter just 
        generated. All lowercase, no spaces or funny characters.
    :returns: True if successful, else False.
    """

    project_dir = os.path.join(repo_dir, generated_project)
    if os.path.exists(project_dir):
        shutil.move(project_dir, os.path.dirname(repo_dir))
        os.rmdir(repo_dir)
        return True
    return False
