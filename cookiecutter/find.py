#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.find
-----------------

Functions for finding Cookiecutter templates and other components.
"""

import logging
import os


def find_template(repo_dir):
    """
    Determines which child directory of `repo_dir` is the project template.
    
    :param repo_dir: Local directory of newly cloned repo.
    :returns project_template: Relative path to project template.
    """

    logging.info('Searching {0} for the project template.'.format(repo_dir))
    contents_set = set(os.listdir(repo_dir))
    exclude_set = set(['.DS_Store', '.git', '.gitignore', 'README.rst', 'cookiecutter.json'])
    
    # Subtract set of excludes from contents.
    contents_set -= exclude_set

    if len(contents_set) == 1:
        project_template = contents_set.pop()
        project_template = os.path.join(repo_dir, project_template)
        logging.info('The project template appears to be {0}'.format(project_template))
        return project_template
    return False
