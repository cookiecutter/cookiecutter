#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.main
-----------------

Main entry point for the `cookiecutter` command.

The code in this module is also a good example of how to use Cookiecutter as a
library rather than a script.
"""

import argparse
import logging
import os

from .cleanup import remove_repo
from .find import find_template
from .generate import generate_context, generate_files
from .vcs import git_clone


logger = logging.getLogger(__name__)

def cookiecutter(input_dir):
    """
    API equivalent to using Cookiecutter at the command line.
    
    :param input_dir: A project template directory or URL to git repo.
    """

    # If it's a git repo, clone and prompt
    if input_dir.endswith('.git'):
        got_repo_arg = True
        repo_dir = git_clone(input_dir)
        project_template = find_template(repo_dir)
        os.chdir(repo_dir)
    else:
        got_repo_arg = False
        project_template = input_dir

    # Create project from local context and project template.


    json_dir = os.path.join(os.path.dirname(project_template), 'json/')
    logging.info('json_dir is {0}'.format(json_dir))
    context = generate_context(
        json_dir=json_dir
    )
    generate_files(
        input_dir=project_template,
        context=context
    )

    # Remove repo if Cookiecutter cloned it in the first place.
    # Here the user just wants a project, not a project template.
    if got_repo_arg:
        generated_project = context['project']['repo_name']
        remove_repo(repo_dir, generated_project)
    

def main():
    """ Entry point for the package, as defined in setup.py. """

    # Log info and above to console
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    # Get command line input/output arguments
    parser = argparse.ArgumentParser(
        description='Create a project from a Cookiecutter project template.'
    )
    parser.add_argument(
        'input_dir',
        help='Cookiecutter project template dir, e.g. {{project.repo_name}}/'
    )
    args = parser.parse_args()
    
    cookiecutter(args.input_dir)

if __name__ == '__main__':
    main()
