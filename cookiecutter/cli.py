#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.cli
-----------------

Main `cookiecutter` CLI.
"""

from __future__ import unicode_literals

import os
import sys
import logging

import click

from cookiecutter import __version__
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import (
    OutputDirExistsException, InvalidModeException
)

logger = logging.getLogger(__name__)


def version_msg():
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = 'Cookiecutter %(version)s from {} (Python {})'
    return message.format(location, python_version)


@click.command()
@click.version_option(__version__, '-V', '--version', message=version_msg())
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
@click.option(
    '--replay', is_flag=True,
    help='Do not prompt for parameters and only use information entered '
         'previously',
)
def main(template, no_input, checkout, verbose, replay):
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
        cookiecutter(template, checkout, no_input, replay=replay)
    except (OutputDirExistsException, InvalidModeException) as e:
        click.echo(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
