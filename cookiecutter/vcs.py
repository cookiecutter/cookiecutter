"""Helper functions for working with version control systems."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from shutil import which
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Literal

from cookiecutter.exceptions import (
    RepositoryCloneFailed,
    RepositoryNotFound,
    UnknownRepoType,
    VCSNotInstalled,
)
from cookiecutter.prompt import prompt_and_delete
from cookiecutter.utils import make_sure_path_exists

logger = logging.getLogger(__name__)


BRANCH_ERRORS = [
    'error: pathspec',
    'unknown revision',
]


def identify_repo(repo_url: str) -> tuple[Literal["git", "hg"], str]:
    """Determine if `repo_url` should be treated as a URL to a git or hg repo.

    Repos can be identified by prepending "hg+" or "git+" to the repo URL.

    :param repo_url: Repo URL of unknown type.
    :returns: ('git', repo_url), ('hg', repo_url), or None.
    """
    repo_url_values = repo_url.split('+')
    if len(repo_url_values) == 2:
        repo_type = repo_url_values[0]
        if repo_type in ["git", "hg"]:
            return repo_type, repo_url_values[1]  # type: ignore[return-value]
        raise UnknownRepoType
    if 'git' in repo_url:
        return 'git', repo_url
    if 'bitbucket' in repo_url:
        return 'hg', repo_url
    raise UnknownRepoType


def is_vcs_installed(repo_type: str) -> bool:
    """
    Check if the version control system for a repo type is installed.

    :param repo_type:
    """
    return bool(which(repo_type))


def clone(
    repo_url: str,
    checkout: str | None = None,
    clone_to_dir: Path | str = ".",
    no_input: bool = False,
) -> str:
    """Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param clone_to_dir: The directory to clone to.
                         Defaults to the current directory.
    :param no_input: Do not prompt for user input and eventually force a refresh of
        cached resources.
    :returns: str with path to the new directory of the repository.
    """
    # Ensure that clone_to_dir exists
    clone_to_dir = Path(clone_to_dir).expanduser()
    make_sure_path_exists(clone_to_dir)

    # identify the repo_type
    repo_type, repo_url = identify_repo(repo_url)

    # check that the appropriate VCS for the repo_type is installed
    if not is_vcs_installed(repo_type):
        msg = f"'{repo_type}' is not installed."
        raise VCSNotInstalled(msg)

    repo_url = repo_url.rstrip('/')
    repo_name = os.path.split(repo_url)[1]
    if repo_type == 'git':
        repo_name = repo_name.split(':')[-1].rsplit('.git')[0]
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, repo_name))
    if repo_type == 'hg':
        repo_dir = os.path.normpath(os.path.join(clone_to_dir, repo_name))
    logger.debug(f'repo_dir is {repo_dir}')

    # Clone to a temporary directory first to avoid data loss
    # if the operation fails mid-way.
    temp_dir = tempfile.mkdtemp(dir=clone_to_dir)
    try:
        subprocess.check_output(
            [repo_type, 'clone', repo_url, temp_dir],
            stderr=subprocess.STDOUT,
        )
        if checkout is not None:
            checkout_params = [checkout]
            # Avoid Mercurial "--config" and "--debugger" injection vulnerability
            if repo_type == "hg":
                checkout_params.insert(0, "--")
            subprocess.check_output(
                [repo_type, 'checkout', *checkout_params],
                cwd=temp_dir,
                stderr=subprocess.STDOUT,
            )
    except subprocess.CalledProcessError as clone_error:
        shutil.rmtree(temp_dir, ignore_errors=True)
        output = clone_error.output.decode('utf-8')
        if 'not found' in output.lower():
            msg = f'The repository {repo_url} could not be found, have you made a typo?'
            raise RepositoryNotFound(msg) from clone_error
        if any(error in output for error in BRANCH_ERRORS):
            msg = (
                f'The {checkout} branch of repository '
                f'{repo_url} could not found, have you made a typo?'
            )
            raise RepositoryCloneFailed(msg) from clone_error
        logger.exception('git clone failed with error: %s', output)
        raise

    # Clone and checkout succeeded — now safely replace the cached repo
    try:
        if os.path.isdir(repo_dir):
            should_proceed = prompt_and_delete(repo_dir, no_input=no_input)
            if not should_proceed:
                # User wants to reuse the existing version
                shutil.rmtree(temp_dir, ignore_errors=True)
                return repo_dir
            # prompt_and_delete already removed the directory at this point

        shutil.move(temp_dir, repo_dir)
        return repo_dir
    finally:
        # Safety net: ensure temp_dir is cleaned up even if
        # prompt_and_delete raises SystemExit / KeyboardInterrupt
        if os.path.isdir(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
