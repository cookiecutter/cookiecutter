# -*- coding: utf-8 -*-

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
    :param config_dict: The user config, which will contain abbreviation
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


def determine_repo_dir(template, abbreviations, cookiecutters_dir, checkout,
                       no_input):
    template = expand_abbreviations(template, abbreviations)

    if is_repo_url(template):
        repo_dir = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=cookiecutters_dir,
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
