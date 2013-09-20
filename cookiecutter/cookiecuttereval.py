#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.evaluate
-----------------

Main entry point for the `cookiecuttereval` command.
"""

import sys
import argparse

from cookiecutter.generate import resolve_context

def parse_cookiecuttereval_args(args):
    """ Parse the command-line arguments to Cookiecutter. """

    parser = argparse.ArgumentParser(
        description='Querry the context of cookiecutter.'
    )
    parser.add_argument(
        '-e', '--expression', required=True,
        help='The expression to be evaluated based on the context.',
    )
    return parser.parse_args(args)



def main():
    """ Entry point for the package, as defined in setup.py. """
    args = parse_cookiecuttereval_args(sys.argv[1:])

    sys.stdout.write(resolve_context(args.expression))

if __name__ == '__main__':
    main()
