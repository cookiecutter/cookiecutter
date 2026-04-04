"""Main `cookiecutter` CLI."""

from __future__ import annotations

import json
import os
import sys
import click
from collections import OrderedDict
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing import Literal

    from click import Context, Parameter



from cookiecutter import __version__
from cookiecutter.config import get_user_config
from cookiecutter.exceptions import (
    ContextDecodingException,
    EmptyDirNameException,
    FailedHookException,
    InvalidModeException,
    InvalidZipRepository,
    OutputDirExistsException,
    RepositoryCloneFailed,
    RepositoryNotFound,
    UndefinedVariableInTemplate,
    UnknownExtension,
)
from cookiecutter.log import configure_logger
from cookiecutter.main import cookiecutter


def version_msg() -> str:
    """Return the Cookiecutter version, location and Python powering it."""
    python_version = sys.version
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f"Cookiecutter {__version__} from {location} (Python {python_version})"


def validate_extra_context(
    _ctx: Context, _param: Parameter, value: Iterable[str]
) -> OrderedDict[str, str] | None:
    """Validate extra context."""
    for string in value:
        if '=' not in string:
            msg = (
                f"EXTRA_CONTEXT should contain items of the form key=value; "
                f"'{string}' doesn't match that form"
            )
            raise click.BadParameter(msg)

    # Convert tuple -- e.g.: ('program_name=foobar', 'startsecs=66')
    # to dict -- e.g.: {'program_name': 'foobar', 'startsecs': '66'}
    return OrderedDict(s.split('=', 1) for s in value) or None


def list_installed_templates(
    default_config: bool | dict[str, Any], passed_config_file: str | None
) -> None:
    """List installed (locally cloned) templates. Use cookiecutter --list-installed."""
    config = get_user_config(passed_config_file, default_config)
    cookiecutter_folder: str = config['cookiecutters_dir']
    if not os.path.exists(cookiecutter_folder):
        click.echo(
            f"Error: Cannot list installed templates. "
            f"Folder does not exist: {cookiecutter_folder}"
        )
        sys.exit(-1)

    template_names = [
        folder
        for folder in os.listdir(cookiecutter_folder)
        if os.path.exists(
            os.path.join(cookiecutter_folder, folder, 'cookiecutter.json')
        )
    ]
    click.echo(f'{len(template_names)} installed templates: ')
    for name in template_names:
        click.echo(f' * {name}')


@click.group(
    invoke_without_command=True,
    context_settings={
        "help_option_names": ['-h', '--help'],
        "allow_extra_args": True,
        "allow_interspersed_args": False,
    },
)
@click.pass_context
@click.version_option(__version__, '-V', '--version', message=version_msg())

@click.option(
    '--no-input',
    is_flag=True,
    help='Do not prompt for parameters and only use cookiecutter.json file content. '
    'Defaults to deleting any cached resources and redownloading them. '
    'Cannot be combined with the --replay flag.',
)
@click.option(
    '-c',
    '--checkout',
    help='branch, tag or commit to checkout after git clone',
)
@click.option(
    '--directory',
    help='Directory within repo that holds cookiecutter.json file '
    'for advanced repositories with multi templates in it',
)
@click.option(
    '-v', '--verbose', is_flag=True, help='Print debug information', default=False
)
@click.option(
    '--replay',
    is_flag=True,
    help='Do not prompt for parameters and only use information entered previously. '
    'Cannot be combined with the --no-input flag or with extra configuration passed.',
)
@click.option(
    '--replay-file',
    type=click.Path(),
    default=None,
    help='Use this file for replay instead of the default.',
)
@click.option(
    '-f',
    '--overwrite-if-exists',
    is_flag=True,
    help='Overwrite the contents of the output directory if it already exists',
)
@click.option(
    '-s',
    '--skip-if-file-exists',
    is_flag=True,
    help='Skip the files in the corresponding directories if they already exist',
    default=False,
)
@click.option(
    '-o',
    '--output-dir',
    default='.',
    type=click.Path(),
    help='Where to output the generated project dir into',
)
@click.option(
    '--config-file', type=click.Path(), default=None, help='User configuration file'
)
@click.option(
    '--default-config',
    is_flag=True,
    help='Do not load a config file. Use the defaults instead',
)
@click.option(
    '--debug-file',
    type=click.Path(),
    default=None,
    help='File to be used as a stream for DEBUG logging',
)
@click.option(
    '--accept-hooks',
    type=click.Choice(['yes', 'ask', 'no']),
    default='yes',
    help='Accept pre/post hooks',
)
@click.option(
    '-l', '--list-installed', is_flag=True, help='List currently installed templates.'
)
@click.option(
    '--keep-project-on-failure',
    is_flag=True,
    help='Do not delete project folder on failure',
)
def main(
    ctx: Context,
    no_input: bool,
    checkout: str,
    verbose: bool,
    replay: bool | str,
    overwrite_if_exists: bool,
    output_dir: str,
    config_file: str | None,
    default_config: bool,
    debug_file: str | None,
    directory: str,
    skip_if_file_exists: bool,
    accept_hooks: Literal['yes', 'ask', 'no'],
    replay_file: str | None,
    list_installed: bool,
    keep_project_on_failure: bool,
) -> None:
    """Create a project from a Cookiecutter project template (TEMPLATE).

    Cookiecutter is free and open source software, developed and managed by
    volunteers. If you would like to help out or fund the project, please get
    in touch at https://github.com/cookiecutter/cookiecutter.
    """
    # Commands that should work without arguments

    if ctx.invoked_subcommand is not None:
        return

    # Parse positional args manually from ctx.args
    args = ctx.args
    template = args[0] if args else None
    extra_context_raw = tuple(args[1:]) if len(args) > 1 else ()
    extra_context = validate_extra_context(ctx, None, extra_context_raw)
    
    if list_installed:
        list_installed_templates(default_config, config_file)
        sys.exit(0)

    # Raising usage, after all commands that should work without args.
    if not template or template.lower() == 'help':
        click.echo(click.get_current_context().get_help())
        sys.exit(0)

    configure_logger(stream_level='DEBUG' if verbose else 'INFO', debug_file=debug_file)

    # If needed, prompt the user to ask whether or not they want to execute
    # the pre/post hooks.
    if accept_hooks == "ask":
        _accept_hooks = click.confirm("Do you want to execute hooks?")
    else:
        _accept_hooks = accept_hooks == "yes"

    if replay_file:
        replay = replay_file

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
            accept_hooks=_accept_hooks,
            keep_project_on_failure=keep_project_on_failure,
        )
    except (
        ContextDecodingException,
        OutputDirExistsException,
        EmptyDirNameException,
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
        click.echo(f'{undefined_err.message}')
        click.echo(f'Error message: {undefined_err.error.message}')

        context_str = json.dumps(undefined_err.context, indent=4, sort_keys=True)
        click.echo(f'Context: {context_str}')
        sys.exit(1)

@main.command("list-prompts")
@click.argument("template")
@click.option(
    "--checkout",
    "-c",
    default=None,
    help="branch, tag or commit to checkout after git clone",
)
@click.option(
    "--directory",
    default=None,
    help="Directory within repo that holds cookiecutter.json file",
)
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["human", "json"]),
    default="human",
    help="Output format: human-readable (default) or json",
)
def list_prompts(template, checkout, directory, output_format):
    """List all variables in a Cookiecutter template without generating files.

    TEMPLATE is the path or URL to the Cookiecutter template.

    Examples:

    \b
    cookiecutter list-prompts gh:audreyfeldroy/cookiecutter-pypackage
    cookiecutter list-prompts ./my-local-template
    cookiecutter list-prompts gh:audreyfeldroy/cookiecutter-pypackage --format json
    """
    from cookiecutter.config import get_user_config
    from cookiecutter.repository import determine_repo_dir

    try:
        config_dict = get_user_config()

        repo_dir, cleanup = determine_repo_dir(
            template=template,
            abbreviations=config_dict["abbreviations"],
            clone_to_dir=config_dict["cookiecutters_dir"],
            checkout=checkout,
            no_input=True,
            directory=directory,
        )
    except Exception as e:
        click.echo(f"Error fetching template: {e}", err=True)
        sys.exit(1)

    # Find cookiecutter.json
    cookiecutter_json_path = os.path.join(repo_dir, "cookiecutter.json")
    if not os.path.exists(cookiecutter_json_path):
        click.echo(
            f"No cookiecutter.json found in {repo_dir}", err=True
        )
        sys.exit(1)

    # Load it
    with open(cookiecutter_json_path, encoding="utf-8") as f:
        cookiecutter_json = json.load(f)

    # Pull out __prompts__ if it exists
    prompts = cookiecutter_json.get("__prompts__", {})

    # Collect variables (skip private keys starting with _)
    variables = []
    for key, default in cookiecutter_json.items():
        if key.startswith("_"):
            continue
        description = prompts.get(key, None)
        variables.append(
            {
                "key": key,
                "default": default,
                "description": description,
            }
        )

    # Output
    if output_format == "json":
        click.echo(json.dumps(variables, indent=2, default=str))
    else:
        for var in variables:
            default_display = json.dumps(var["default"], default=str)
            click.echo(
                click.style(var["key"], bold=True)
                + f" (default: {default_display})"
            )
            if var["description"]:
                click.echo(f"  {var['description']}")
            click.echo()


if __name__ == "__main__":
    main()
