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

from cookiecutter import __version__, config
from cookiecutter.main import cookiecutter

logger = logging.getLogger(__name__)

# The `click` custom context settings
CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help'],
)


def print_version(context, param, value):
    if not value or context.resilient_parsing:
        return
    click.echo('Cookiecutter %s from %s (Python %s)' % (
        __version__,
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        sys.version[:3]
    ))
    context.exit()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('template')
@click.option(
    '--no-input', is_flag=True,
    help='Do not prompt for parameters and only use cookiecutter.json '
         'file content',
)
@click.option(
    '--rc-file', metavar='FILE', default=config.USER_CONFIG_PATH,
    help='Path of user configuration file (empty for none)',
)
@click.option(
    '-c', '--checkout',
    help='branch, tag or commit to checkout after git clone',
)
@click.option(
    '-V', '--version',
    is_flag=True, help='Show version information and exit.',
    callback=print_version, expose_value=False, is_eager=True,
)
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
def main(template, no_input, checkout, verbose, rc_file):
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

    cookiecutter(template, checkout, no_input, rc_file=rc_file, extra_globals=dict(
        checkout=checkout,
        verbose=verbose,
    ))
