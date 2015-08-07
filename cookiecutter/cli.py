#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.cli
-----------------

Main `cookiecutter` CLI.
"""

from __future__ import unicode_literals

import sys
import logging

import click

from cookiecutter import __version__
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException

logger = logging.getLogger(__name__)


@click.command()
@click.version_option(__version__, '-V', '--version')
@click.argument('template')
@click.option(
    '--no-input', is_flag=True,
    help='Do not prompt for parameters and only use cookiecutter.json '
         'file content',
)
@click.option(
    '-c', '--checkout',
    help='branch, tag or commit to checkout after git clone',
)
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
def main(template, no_input, checkout, verbose):
    """Create a project from a Cookiecutter project template (TEMPLATE)."""
    if verbose:
        logging.basicConfig(
            format='%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG
        )
    else:
        # Log info and above to console
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )

    try:
        cookiecutter(template, checkout, no_input)
    except OutputDirExistsException as e:
        click.echo(e)
        sys.exit(1)

if __name__ == "__main__":  # pragma: no cover
    main()
