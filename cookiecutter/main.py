#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.main
-----------------

Main entry point for the `cookiecutter` command.

The code in this module is also a good example of how to use Cookiecutter as a
library rather than a script.
"""

from __future__ import unicode_literals
import argparse
import logging
import os
import sys

from . import __version__
from .config import get_user_config
from .generate import generate_context, generate_files
from .prompt import prompt_for_config
from .utils import read_json_file
from .vcs import clone

logger = logging.getLogger(__name__)


def cookiecutter(input_dir, checkout=None, no_input=False, parameters=None):
    """
    API equivalent to using Cookiecutter at the command line.

    :param input_dir: A directory containing a project template dir,
        or a URL to git repo.
    :param checkout: The branch, tag or commit ID to checkout after clone
    :param parameters: dictionary containing parameters to be passed to
        cookiecutter overriding values in cookiecutter.json and default_context.
    """

    # Get user config from ~/.cookiecutterrc or equivalent
    # If no config file, sensible defaults from config.DEFAULT_CONFIG are used
    config_dict = get_user_config()

    # TODO: find a better way to tell if it's a repo URL
    if "git@" in input_dir or "https://" in input_dir:
        repo_dir = clone(
            repo_url=input_dir,
            checkout=checkout,
            clone_to_dir=config_dict['cookiecutters_dir']
        )
    else:
        # If it's a local repo, no need to clone or copy to your cookiecutters_dir
        repo_dir = input_dir

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    logging.debug('context_file is {0}'.format(context_file))

    context = generate_context(
        context_file=context_file,
        default_context=config_dict['default_context'],
        user_parameters=parameters
    )

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set
    if not no_input:
        cookiecutter_dict = prompt_for_config(context)
        context['cookiecutter'] = cookiecutter_dict

    # Create project from local context and project template.
    generate_files(
        repo_dir=repo_dir,
        context=context
    )


def _get_parser():
    parser = argparse.ArgumentParser(
        description='Create a project from a Cookiecutter project template.'
    )
    parser.add_argument(
        '--no-input',
        action="store_true",
        help='Do not prompt for parameters and only use cookiecutter.json '
             'file content')
    parser.add_argument(
        '--parameters',
        metavar='parameters.json',
        help="file containings parameters to be passed to cookiecutter"
    )
    parser.add_argument(
        'input_dir',
        help='Cookiecutter project dir, e.g. cookiecutter-pypackage/'
    )
    parser.add_argument(
        '-c', '--checkout',
        help='branch, tag or commit to checkout after git clone'
    )
    cookiecutter_pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parser.add_argument(
        '-V', '--version',
        help="Show version information and exit.",
        action='version',
        version='Cookiecutter %s from %s (Python %s)' % (
            __version__,
            cookiecutter_pkg_dir,
            sys.version[:3]
        )
    )
    parser.add_argument(
        '-v', '--verbose',
        help='Print debug information',
        action='store_true', default=False
    )

    return parser


def parse_cookiecutter_args(args):
    """ Parse the command-line arguments to Cookiecutter. """
    parser = _get_parser()
    return parser.parse_args(args)


def main():
    """ Entry point for the package, as defined in setup.py. """

    args = parse_cookiecutter_args(sys.argv[1:])

    if args.verbose:
        logging.basicConfig(format='%(levelname)s %(filename)s: %(message)s',
                            level=logging.DEBUG)
    else:
        # Log info and above to console
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )

    # load parameters from the passed in --parameters JSON file
    parameters = read_json_file(args.parameters) if args.parameters else None

    cookiecutter(args.input_dir, args.checkout, args.no_input, parameters)


if __name__ == '__main__':
    main()
