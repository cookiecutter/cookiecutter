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
import shutil

from .cleanup import remove_repo
from .find import find_template
from .prompt import prompt_for_config
from .generate import generate_context, generate_files
from .vcs import git_clone


logger = logging.getLogger(__name__)

def cookiecutter(input_dir, checkout=None, no_input=False):
    """
    API equivalent to using Cookiecutter at the command line.

    :param input_dir: A directory containing a project template dir,
        or a URL to git repo.
    :param checkout: The branch, tag or commit ID to checkout after clone
    """

    # If it's a git repo, clone and if local repo, copy
    if input_dir.endswith('.git'):
        got_repo_arg = True
        repo_dir = git_clone(input_dir, checkout)
        project_template = find_template(repo_dir)
    else:
        repo_dir = './__cookiecutter_tmpdir'
        shutil.copytree(input_dir, repo_dir)

    project_template = find_template(repo_dir)
    config_file = os.path.join(os.path.dirname(project_template),
                               'cookiecutter.json')
    logging.debug('config_file is {0}'.format(config_file))

    context = generate_context(
        config_file=config_file
    )

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set
    if not no_input:
        cookiecutter_dict = prompt_for_config(context)
        context['cookiecutter'] = cookiecutter_dict

    # Create project from local context and project template.
    generate_files(
        template_dir=project_template,
        context=context
    )

    # Remove repo if Cookiecutter cloned it in the first place.
    # Here the user just wants a project, not a project template.
    generated_project = context['cookiecutter']['repo_name']
    remove_repo(repo_dir, generated_project)



def parse_cookiecutter_args(args):
    """ Parse the command-line arguments to Cookiecutter. """

    parser = argparse.ArgumentParser(
        description='Create a project from a Cookiecutter project template.'
    )
    parser.add_argument(
        '--no-input',
        action="store_true",
        help='Do not prompt for parameters and only use cookiecutter.json '
             'file content')
    parser.add_argument(
        'input_dir',
        help='Cookiecutter project dir, e.g. cookiecutter-pypackage/'
    )
    parser.add_argument(
        '-c', '--checkout',
        help='branch, tag or commit to checkout after git clone'
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Print debug information',
        action='store_true', default=False
    )
    return parser.parse_args(args)


def main():
    """ Entry point for the package, as defined in setup.py. """

    args = parse_cookiecutter_args(sys.argv[1:])

    if args.verbose:
        logging.basicConfig(format='%(levelname)s %(filename)s: %(message)s', level=logging.DEBUG)
    else:
        # Log info and above to console
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )
    
    cookiecutter(args.input_dir, args.checkout, args.no_input)


if __name__ == '__main__':
    main()
