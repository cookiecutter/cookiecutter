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
import sys

from .cleanup import remove_repo
from .find import find_template
from .prompt import prompt_for_config
from .generate import generate_context, generate_files
from .vcs import git_clone


logger = logging.getLogger(__name__)

def cookiecutter(input_dir):
    """
    API equivalent to using Cookiecutter at the command line.
    
    :param input_dir: A directory containing a project template dir, 
        or a URL to git repo.
    """

    # If it's a git repo, clone and prompt
    if input_dir.endswith('.git'):
        got_repo_arg = True
        repo_dir = git_clone(input_dir)
        project_template = find_template(repo_dir)
    else:
        got_repo_arg = False
        project_template = find_template(input_dir)

    config_file = os.path.join(os.path.dirname(project_template), 'cookiecutter.json')
    logging.debug('config_file is {0}'.format(config_file))

    context = generate_context(
        config_file=config_file
    )

    # If the context came from a repo, prompt the user to manually configure
    # at the command line.
    if got_repo_arg:
        cookiecutter_dict = prompt_for_config(context)
        context['cookiecutter'] = cookiecutter_dict

    # Create project from local context and project template.
    generate_files(
        template_dir=project_template,
        context=context
    )

    # Remove repo if Cookiecutter cloned it in the first place.
    # Here the user just wants a project, not a project template.
    if got_repo_arg:
        generated_project = context['cookiecutter']['repo_name']
        remove_repo(repo_dir, generated_project)

def parse_cookiecutter_args(args):
    """ Parse the command-line arguments to Cookiecutter. """

    parser = argparse.ArgumentParser(
        description='Create a project from a Cookiecutter project template.'
    )
    parser.add_argument(
        'input_dir',
        help='Cookiecutter project dir, e.g. cookiecutter-pypackage/'
    )
    return parser.parse_args(args)
    
def main():
    """ Entry point for the package, as defined in setup.py. """

    # Log info and above to console
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

    args = parse_cookiecutter_args(sys.argv[1:])
    
    cookiecutter(args.input_dir)

if __name__ == '__main__':
    main()
