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
import logging
import os

from .config import get_user_config
from .prompt import prompt_for_config
from .generate import generate_context, generate_files
from .vcs import clone

logger = logging.getLogger(__name__)

builtin_abbreviations = {
    'gh': 'https://github.com/{0}.git',
    'bb': 'https://bitbucket.org/{0}',
}


def expand_abbreviations(template, config_dict):
    """
    Expand abbreviations in a template name.

    :param template: The project template name.
    :param config_dict: The user config, which will contain abbreviation
        definitions.
    """

    abbreviations = builtin_abbreviations.copy()
    abbreviations.update(config_dict.get('abbreviations', {}))

    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(':')
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template


def cookiecutter(template, checkout=None, no_input=False, extra_context=None):
    """
    API equivalent to using Cookiecutter at the command line.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :param extra_context: A dictionary of context that overrides default
        and user configuration.
    """

    # Get user config from ~/.cookiecutterrc or equivalent
    # If no config file, sensible defaults from config.DEFAULT_CONFIG are used
    config_dict = get_user_config()

    template = expand_abbreviations(template, config_dict)

    # TODO: find a better way to tell if it's a repo URL
    if 'git@' in template or 'https://' in template:
        repo_dir = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=config_dict['cookiecutters_dir'],
            no_input=no_input
        )
    else:
        # If it's a local repo, no need to clone or copy to your
        # cookiecutters_dir
        repo_dir = template

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    logging.debug('context_file is {0}'.format(context_file))

    context = generate_context(
        context_file=context_file,
        default_context=config_dict['default_context'],
        extra_context=extra_context,
    )

    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set
    context['cookiecutter'] = prompt_for_config(context, no_input)

    # Create project from local context and project template.
    generate_files(
        repo_dir=repo_dir,
        context=context
    )
