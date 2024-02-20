"""
Main entry point for the `cookiecutter` command.

The code in this module is also a good example of how to use Cookiecutter as a
library rather than a script.
"""

import logging
import os
import sys
from copy import copy
from pathlib import Path

from cookiecutter.config import get_user_config
from cookiecutter.exceptions import InvalidModeException
from cookiecutter.generate import generate_context, generate_files
from cookiecutter.hooks import run_pre_prompt_hook
from cookiecutter.prompt import choose_nested_template, prompt_for_config
from cookiecutter.replay import dump, load
from cookiecutter.repository import determine_repo_dir
from cookiecutter.utils import rmtree

logger = logging.getLogger(__name__)


def cookiecutter(
    template,
    checkout=None,
    no_input=False,
    extra_context=None,
    replay=None,
    overwrite_if_exists=False,
    output_dir='.',
    config_file=None,
    default_config=False,
    password=None,
    directory=None,
    skip_if_file_exists=False,
    accept_hooks=True,
    keep_project_on_failure=False,
):
    """
    Run Cookiecutter just as if using it from the command line.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Do not prompt for user input.
        Use default values for template parameters taken from `cookiecutter.json`, user
        config and `extra_dict`. Force a refresh of cached resources.
    :param extra_context: A dictionary of context that overrides default
        and user configuration.
    :param replay: Do not prompt for input, instead read from saved json. If
        ``True`` read from the ``replay_dir``.
        if it exists
    :param overwrite_if_exists: Overwrite the contents of the output directory
        if it exists.
    :param output_dir: Where to output the generated project dir into.
    :param config_file: User configuration file path.
    :param default_config: Use default values rather than a config file.
    :param password: The password to use when extracting the repository.
    :param directory: Relative path to a cookiecutter template in a repository.
    :param skip_if_file_exists: Skip the files in the corresponding directories
        if they already exist.
    :param accept_hooks: Accept pre and post hooks if set to `True`.
    :param keep_project_on_failure: If `True` keep generated project directory even when
        generation fails
    """
    if replay and ((no_input is not False) or (extra_context is not None)):
        err_msg = (
            "You can not use both replay and no_input or extra_context "
            "at the same time."
        )
        raise InvalidModeException(err_msg)

    config_dict = get_user_config(
        config_file=config_file,
        default_config=default_config,
    )
    base_repo_dir, cleanup_base_repo_dir = determine_repo_dir(
        template=template,
        abbreviations=config_dict['abbreviations'],
        clone_to_dir=config_dict['cookiecutters_dir'],
        checkout=checkout,
        no_input=no_input,
        password=password,
        directory=directory,
    )
    repo_dir, cleanup = base_repo_dir, cleanup_base_repo_dir
    # Run pre_prompt hook
    repo_dir = run_pre_prompt_hook(base_repo_dir) if accept_hooks else repo_dir
    # Always remove temporary dir if it was created
    cleanup = True if repo_dir != base_repo_dir else False

    import_patch = _patch_import_path_for_repo(repo_dir)
    template_name = os.path.basename(os.path.abspath(repo_dir))
    if replay:
        with import_patch:
            if isinstance(replay, bool):
                context_from_replayfile = load(config_dict['replay_dir'], template_name)
            else:
                path, template_name = os.path.split(os.path.splitext(replay)[0])
                context_from_replayfile = load(path, template_name)

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    logger.debug('context_file is %s', context_file)

    if replay:
        context = generate_context(
            context_file=context_file,
            default_context=config_dict['default_context'],
            extra_context=None,
        )
        logger.debug('replayfile context: %s', context_from_replayfile)
        items_for_prompting = {
            k: v
            for k, v in context['cookiecutter'].items()
            if k not in context_from_replayfile['cookiecutter'].keys()
        }
        context_for_prompting = {}
        context_for_prompting['cookiecutter'] = items_for_prompting
        context = context_from_replayfile
        logger.debug('prompting context: %s', context_for_prompting)
    else:
        context = generate_context(
            context_file=context_file,
            default_context=config_dict['default_context'],
            extra_context=extra_context,
        )
        context_for_prompting = context
    # preserve the original cookiecutter options
    # print(context['cookiecutter'])
    context['_cookiecutter'] = {
        k: v for k, v in context['cookiecutter'].items() if not k.startswith("_")
    }

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set

    with import_patch:
        if {"template", "templates"} & set(context["cookiecutter"].keys()):
            nested_template = choose_nested_template(context, repo_dir, no_input)
            return cookiecutter(
                template=nested_template,
                checkout=checkout,
                no_input=no_input,
                extra_context=extra_context,
                replay=replay,
                overwrite_if_exists=overwrite_if_exists,
                output_dir=output_dir,
                config_file=config_file,
                default_config=default_config,
                password=password,
                directory=directory,
                skip_if_file_exists=skip_if_file_exists,
                accept_hooks=accept_hooks,
                keep_project_on_failure=keep_project_on_failure,
            )
        if context_for_prompting['cookiecutter']:
            context['cookiecutter'].update(
                prompt_for_config(context_for_prompting, no_input)
            )

    logger.debug('context is %s', context)

    # include template dir or url in the context dict
    context['cookiecutter']['_template'] = template

    # include output+dir in the context dict
    context['cookiecutter']['_output_dir'] = os.path.abspath(output_dir)

    # include repo dir or url in the context dict
    context['cookiecutter']['_repo_dir'] = f"{repo_dir}"

    # include checkout details in the context dict
    context['cookiecutter']['_checkout'] = checkout

    dump(config_dict['replay_dir'], template_name, context)

    # Create project from local context and project template.
    with import_patch:
        result = generate_files(
            repo_dir=repo_dir,
            context=context,
            overwrite_if_exists=overwrite_if_exists,
            skip_if_file_exists=skip_if_file_exists,
            output_dir=output_dir,
            accept_hooks=accept_hooks,
            keep_project_on_failure=keep_project_on_failure,
        )

    # Cleanup (if required)
    if cleanup:
        rmtree(repo_dir)
    if cleanup_base_repo_dir:
        rmtree(base_repo_dir)
    return result


class _patch_import_path_for_repo:
    def __init__(self, repo_dir: "os.PathLike[str]"):
        self._repo_dir = f"{repo_dir}" if isinstance(repo_dir, Path) else repo_dir
        self._path = None

    def __enter__(self):
        self._path = copy(sys.path)
        sys.path.append(self._repo_dir)

    def __exit__(self, type, value, traceback):
        sys.path = self._path
