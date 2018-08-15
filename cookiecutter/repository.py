# -*- coding: utf-8 -*-

"""Cookiecutter repository functions."""

from __future__ import unicode_literals
import os
import re

from .exceptions import RepositoryNotFound
from .vcs import clone
from .zipfile import unzip

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


def is_zip_file(value):
    """Return True if value is a zip file."""
    return value.lower().endswith('.zip')


def expand_abbreviations(template, abbreviations):
    """Expand abbreviations in a template name.

    :param template: The project template name.
    :param abbreviations: Abbreviation definitions.
    """
    if template in abbreviations:
        return abbreviations[template]

    # Split on colon. If there is no colon, rest will be empty
    # and prefix will be the whole template
    prefix, sep, rest = template.partition(':')
    if prefix in abbreviations:
        return abbreviations[prefix].format(rest)

    return template


def repository_has_cookiecutter_json(repo_directory):
    """Determine if `repo_directory` contains a `cookiecutter.json` file.

    :param repo_directory: The candidate repository directory.
    :return: True if the `repo_directory` is valid, else False.
    """
    repo_directory_exists = os.path.isdir(repo_directory)

    repo_config_exists = os.path.isfile(
        os.path.join(repo_directory, 'cookiecutter.json')
    )
    return repo_directory_exists and repo_config_exists


def determine_repo_dir(template, abbreviations, clone_to_dir, checkout,
                       no_input, password=None):
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
    :param password: The password to use when extracting the repository.
    :return: A tuple containing the cookiecutter template directory, and
        a boolean descriving whether that directory should be cleaned up
        after the template has been instantiated.
    :raises: `RepositoryNotFound` if a repository directory could not be found.
    """
    template = expand_abbreviations(template, abbreviations)

    if is_zip_file(template):
        unzipped_dir = unzip(
            zip_uri=template,
            is_url=is_repo_url(template),
            clone_to_dir=clone_to_dir,
            no_input=no_input,
            password=password
        )
        repository_candidates = [unzipped_dir]
        cleanup = True
    elif is_repo_url(template):
        cloned_repo = clone(
            repo_url=template,
            checkout=checkout,
            clone_to_dir=clone_to_dir,
            no_input=no_input,
        )
        repository_candidates = [cloned_repo]
        cleanup = False
    else:
        repository_candidates = [
            template,
            os.path.join(clone_to_dir, template)
        ]
        cleanup = False

    for repo_candidate in repository_candidates:
        if repository_has_cookiecutter_json(repo_candidate):
            return repo_candidate, cleanup

    raise RepositoryNotFound(
        'A valid repository for "{}" could not be found in the following '
        'locations:\n{}'.format(
            template,
            '\n'.join(repository_candidates)
        )
    )
