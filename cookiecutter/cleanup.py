#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.cleanup
--------------------

Functions for cleaning up after Cookiecutter project generation occurs.
"""

from __future__ import unicode_literals
import logging
import os
import shutil

from .exceptions import MissingProjectDir


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

    logging.debug('Moving {0} out of {1} and removing {1}'.format(generated_project, repo_dir))
    
    parent_dir = os.path.dirname(os.path.abspath(repo_dir))
    logging.debug('parent_dir is {0}'.format(parent_dir))

    project_dir = os.path.join(repo_dir, generated_project)
    logging.debug('project_dir is {0}'.format(project_dir))
    
    if os.path.exists(project_dir):
        shutil.move(project_dir, parent_dir)
        shutil.rmtree(repo_dir)
        return True
    else:
        raise MissingProjectDir(
            'The project did not get generated. Please file an issue in '
            'Cookiecutter with as much detail as possible about what happened.'
        )
