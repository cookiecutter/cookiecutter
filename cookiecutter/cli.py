# -*- coding: utf-8 -*-

"""Main `cookiecutter` CLI."""

import os
import sys
import json
import collections

import click

from cookiecutter import __version__
from cookiecutter.log import configure_logger
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import (
    OutputDirExistsException,
    InvalidModeException,
    FailedHookException,
    UndefinedVariableInTemplate,
    UnknownExtension,
    InvalidZipRepository,
    RepositoryNotFound,
    RepositoryCloneFailed,
)


def version_msg():
    """Return the Cookiecutter version, location and Python powering it."""
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = u'Cookiecutter %(version)s from {} (Python {})'
    return message.format(location, python_version)


def validate_extra_context(ctx, param, value):
    """Validate extra context."""
    for s in value:
        if '=' not in s:
            raise click.BadParameter(
                'EXTRA_CONTEXT should contain items of the form key=value; '
                "'{}' doesn't match that form".format(s)
            )

    # Convert tuple -- e.g.: (u'program_name=foobar', u'startsecs=66')
    # to dict -- e.g.: {'program_name': 'foobar', 'startsecs': '66'}
    return collections.OrderedDict(s.split('=', 1) for s in value) or None


@click.command(context_settings=dict(help_option_names=[u'-h', u'--help']))
@click.version_option(__version__, u'-V', u'--version', message=version_msg())
@click.argument(u'template')
@click.argument(u'extra_context', nargs=-1, callback=validate_extra_context)
@click.option(
    u'--no-input',
    is_flag=True,
    help=u'Do not prompt for parameters and only use cookiecutter.json '
    u'file content',
)
@click.option(
    u'-c', u'--checkout', help=u'branch, tag or commit to checkout after git clone',
)
@click.option(
    u'--directory',
    help=u'Directory within repo that holds cookiecutter.json file '
    u'for advanced repositories with multi templates in it',
)
@click.option(
    '-v', '--verbose', is_flag=True, help='Print debug information', default=False
)
@click.option(
    u'--replay',
    is_flag=True,
    help=u'Do not prompt for parameters and only use information entered '
    u'previously',
)
@click.option(
    u'-f',
    u'--overwrite-if-exists',
    is_flag=True,
    help=u'Overwrite the contents of the output directory if it already exists',
)
@click.option(
    u'-s',
    u'--skip-if-file-exists',
    is_flag=True,
    help=u'Skip the files in the corresponding directories if they already ' u'exist',
    default=False,
)
@click.option(
    u'-o',
    u'--output-dir',
    default='.',
    type=click.Path(),
    help=u'Where to output the generated project dir into',
)
@click.option(
    u'--config-file', type=click.Path(), default=None, help=u'User configuration file'
)
@click.option(
    u'--default-config',
    is_flag=True,
    help=u'Do not load a config file. Use the defaults instead',
)
@click.option(
    u'--debug-file',
    type=click.Path(),
    default=None,
    help=u'File to be used as a stream for DEBUG logging',
)
def main(
    template,
    extra_context,
    no_input,
    checkout,
    verbose,
    replay,
    overwrite_if_exists,
    output_dir,
    config_file,
    default_config,
    debug_file,
    directory,
    skip_if_file_exists,
):
    """Create a project from a Cookiecutter project template (TEMPLATE).

    Cookiecutter is free and open source software, developed and managed by
    volunteers. If you would like to help out or fund the project, please get
    in touch at https://github.com/audreyr/cookiecutter.
    """
    # If you _need_ to support a local template in a directory
    # called 'help', use a qualified path to the directory.
    if template == u'help':
        click.echo(click.get_current_context().get_help())
        sys.exit(0)

    configure_logger(stream_level='DEBUG' if verbose else 'INFO', debug_file=debug_file)

    try:
        cookiecutter(
            template,
            checkout,
            no_input,
            extra_context=extra_context,
            replay=replay,
            overwrite_if_exists=overwrite_if_exists,
            output_dir=output_dir,
            config_file=config_file,
            default_config=default_config,
            password=os.environ.get('COOKIECUTTER_REPO_PASSWORD'),
            directory=directory,
            skip_if_file_exists=skip_if_file_exists,
        )
    except (
        OutputDirExistsException,
        InvalidModeException,
        FailedHookException,
        UnknownExtension,
        InvalidZipRepository,
        RepositoryNotFound,
        RepositoryCloneFailed,
    ) as e:
        click.echo(e)
        sys.exit(1)
    except UndefinedVariableInTemplate as undefined_err:
        click.echo('{}'.format(undefined_err.message))
        click.echo('Error message: {}'.format(undefined_err.error.message))

        context_str = json.dumps(undefined_err.context, indent=4, sort_keys=True)
        click.echo('Context: {}'.format(context_str))
        sys.exit(1)


if __name__ == "__main__":
    main()
