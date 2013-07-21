#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

from .generate import generate_context, generate_files


def main():
    """ Entry point for the package, as defined in setup.py. """

    # Get command line input/output arguments
    parser = argparse.ArgumentParser(
        description='Create a project from a Cookiecutter project template.'
    )
    parser.add_argument(
        'input_dir',
        help='Cookiecutter project template dir, e.g. {{project.repo_name}}/'
    )
    parser.add_argument(
        'output_dir',
        help='Name of desired output dir, e.g. alotofeffort/ or'
            '{{project.repo_name}}/. (This can be templated.)'
    )
    args = parser.parse_args()

    context = generate_context()
    generate_files(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        context=context
    )


if __name__ == '__main__':
    main()
