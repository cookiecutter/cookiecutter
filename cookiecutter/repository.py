# -*- coding: utf-8 -*-

"""Cookiecutter repository functions."""
from __future__ import unicode_literals
import os
import re

from .exceptions import RepositoryNotFound
from .vcs import clone

BUILTIN_ABBREVIATIONS = {
    'gh': 'https://github.com/{0}.git',
    'bb': 'https://bitbucket.org/{0}',
}

REPO_REGEX = re.compile(r"""
(?x)
((((git|hg)\+)?(git|ssh|https?):(//)?)  # something like git:// ssh:// etc.
 |                                      # or
 (\w+@[\w\.]+)                          # something like user@...
)
""")


def is_repo_url(value):
    """Return True if value is a repository URL."""
    return bool(REPO_REGEX.match(value))


def expand_abbreviations(template, user_abbreviations):
    """
    Expand abbreviations in a template name.

    :param template: The project template name.
    :param user_abbreviations: The user config, which will contain abbreviation
        definitions.
    """
    abbreviations = BUILTIN_ABBREVIATIONS.copy()
    abbreviations.update(user_abbreviations)

    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(':')
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template


def determine_repo_dir(template, abbreviations, clone_to_dir, checkout,
                       no_input):
    """
    Locate the repository directory from a template reference.

    Applies repository abbreviations to the template reference.
    If the template refers to a repository URL, clone it.
    If the template is a path to a local repository, use it.

    :param template: A directory containing a project template directory,
        or a URL to a git repository.
    :param abbreviations: A dictionary of repository abbreviation
        definitions.
    :param clone_to_dir: The directory to clone the repository into.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param no_input: Prompt the user at command line for manual configuration?
    :return:
    """
    template = expand_abbreviations(template, abbreviations)

    if is_repo_url(template):
        repo_dir = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=clone_to_dir,
            no_input=no_input,
        )
    else:
        # If it's a local repo, no need to clone or copy to your
        # cookiecutters_dir
        repo_dir = template

    if not os.path.isdir(repo_dir):
        raise RepositoryNotFound(
            'The repository {0} could not be located.'.format(template)
        )
    return repo_dir
