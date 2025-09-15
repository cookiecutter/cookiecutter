"""Main `cookiecutter` CLI."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Annotated, Any, Optional, Literal

if TYPE_CHECKING:
    from collections.abc import Iterable
    from typing_extensions import Literal


from mininterface import Validation, run, Tag
from mininterface.tag.flag import Dir, File
from tyro.conf import DisallowNone, arg, Positional, FlagCreatePairsOff

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


def validate_extra_context(value: Tag[Iterable[str]]):
    """Validate extra context."""
    for string in value.val:
        if '=' not in string:
            msg = (
                f"EXTRA_CONTEXT should contain items of the form key=value; "
                f"'{string}' doesn't match that form"
            )
            return msg
    return True


def list_installed_templates(
    default_config: bool | dict[str, Any], passed_config_file: str | None
) -> None:
    """List installed (locally cloned) templates. Use cookiecutter --list-installed."""
    config = get_user_config(passed_config_file, default_config)
    cookiecutter_folder: str = config['cookiecutters_dir']
    if not os.path.exists(cookiecutter_folder):
        print(
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
    print(f'{len(template_names)} installed templates: ')
    for name in template_names:
        print(f' * {name}')

@dataclass
class Env:
    template: Positional[Optional[File]] = None
    """Template to use"""

    extra_context: Annotated[Positional[list], Validation(validate_extra_context)]  = field(default_factory=list)
    """Extra context parameters as KEY=VALUE pairs"""

    no_input: bool = False
    """Do not prompt for parameters and only use cookiecutter.json file content.
    Defaults to deleting any cached resources and redownloading them.
    Cannot be combined with the --replay flag.
    """

    checkout: Annotated[Optional[str], arg(aliases=["-c"])] = None
    """Branch, tag or commit to checkout after git clone"""

    directory: Optional[Dir] = None
    """Directory within repo that holds cookiecutter.json file for advanced repositories"""

    verbose: Annotated[bool, arg(aliases=["-v"])] = False
    """Print debug information"""

    replay: bool = False
    """Do not prompt for parameters and only use information entered previously.
    Cannot be combined with the --no-input flag or with extra configuration passed.
    """

    replay_file: Optional[File] = None
    """Use this file for replay instead of the default"""

    overwrite_if_exists: Annotated[bool, arg(aliases=["-f"])] = False
    """Overwrite the contents of the output directory if it already exists"""

    skip_if_file_exists: Annotated[bool, arg(aliases=["-s"])] = False
    """Skip the files in the corresponding directories if they already exist"""

    output_dir: Annotated[Dir, arg(aliases=["-o"])] = Path(".")
    """Where to output the generated project dir into"""

    config_file: Optional[File] = None
    """User configuration file"""

    default_config: bool = False
    """Do not load a config file. Use the defaults instead"""

    debug_file: Optional[File] = None
    """File to be used as a stream for DEBUG logging"""

    accept_hooks: Literal["yes", "ask", "no"] = "yes"
    """Accept pre/post hooks"""

    list_installed: Annotated[bool, arg(aliases=["-l"])] = False
    """List currently installed templates"""

    keep_project_on_failure: bool = False
    """Do not delete project folder on failure"""


def main(
) -> None:
    """Create a project from a Cookiecutter project template (TEMPLATE).

    Cookiecutter is free and open source software, developed and managed by
    volunteers. If you would like to help out or fund the project, please get
    in touch at https://github.com/cookiecutter/cookiecutter.
    """
    m = run(FlagCreatePairsOff[DisallowNone[Env]], ask_on_empty_cli=True, add_version=version_msg())
    # m: Mininterface[Env]
    e = m.env
    # Commands that should work without arguments
    if e.list_installed:
        list_installed_templates(e.default_config, str(e.config_file))
        sys.exit(0)

    # Amendments
    configure_logger(stream_level='DEBUG' if e.verbose else 'INFO', debug_file=str(e.debug_file))

    # Convert tuple -- e.g.: ('program_name=foobar', 'startsecs=66')
    # to dict -- e.g.: {'program_name': 'foobar', 'startsecs': '66'}
    extra_context = dict(s.split('=', 1) for s in e.extra_context) or None

    # If needed, prompt the user to ask whether or not they want to execute
    # the pre/post hooks.
    if e.accept_hooks == "ask":
        _accept_hooks = m.confirm("Do you want to execute hooks?")
    else:
        _accept_hooks = e.accept_hooks == "yes"

    # NOTE we may refactor cookiecutter to accept pathlib.Path instead of str and remove the str(Path) casting
    # NOTE we may refactor cookiecutter to accept Env instead of parameters to save code
    try:
        cookiecutter(
            str(e.template),
            e.checkout,
            e.no_input,
            extra_context=extra_context,
            replay=str(e.replay_file) or e.replay,
            overwrite_if_exists=e.overwrite_if_exists,
            output_dir=str(e.output_dir),
            config_file=str(e.config_file),
            default_config=e.default_config,
            password=os.environ.get('COOKIECUTTER_REPO_PASSWORD'),
            directory=str(e.directory),
            skip_if_file_exists=e.skip_if_file_exists,
            accept_hooks=_accept_hooks,
            keep_project_on_failure=e.keep_project_on_failure,
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
        print(e)
        sys.exit(1)
    except UndefinedVariableInTemplate as undefined_err:
        print(f'{undefined_err.message}')
        print(f'Error message: {undefined_err.error.message}')

        context_str = json.dumps(undefined_err.context, indent=4, sort_keys=True)
        print(f'Context: {context_str}')
        sys.exit(1)


if __name__ == "__main__":
    main()
