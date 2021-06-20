"""Helper functions for working with version control systems."""
import logging
import os
from enum import Enum
import subprocess  # nosec
from shutil import which
import re
import click

from cookiecutter.exceptions import (
    RepositoryCloneFailed,
    RepositoryNotFound,
    UnknownRepoType,
    VCSNotInstalled,
)
from cookiecutter.utils import make_sure_path_exists, prompt_and_delete

logger = logging.getLogger(__name__)


class VCS:
    """Abstract base VCS class. Handles the cloning of VCS repositories."""

    cmd = 'xyz'
    """VCS command"""

    allowed_protocols = ['http', 'https', 'ssh', 'file']
    """
    List of allowed protocols
    (no match if protocol not among allowed or specific protocols)
    """

    identifiers = []
    """VCS identifiers (implicit match if present in URL)"""

    protocols = []
    """VCS-specific protocols (e.g. git://, svn://)"""

    suffixes = []
    """VCS-specifix suffixes (e.g. .git, .hg)"""

    not_found_errors = []
    """
    Error messages returned by the VCS if the repo was not found (lowercase)
    """

    branch_errors = []
    """
    Error messages returned by the VCS if the branch could not be checked out
    (lowercase)
    """

    class MatchLevel(Enum):
        """Match level returned by match_repo_url."""

        NONE = 0
        IMPLICIT = 1
        EXPLICIT = 2

    @classmethod
    def match_repo_url(cls, url):
        """
        Check if the raw URL input matches this VCS.

        Return match level:

        | **NONE:** Does not match
        | **IMPLICIT:** Contains VCS identifier
          (e.g. https://private.com/svnrepo, gitolite@server:team/repo)
        | **EXPLICIT:** Has VCS cmd prefix/protocol/suffix
          (e.g. svn://private.com/svnrepo,
          https://github.com/audreyr/cookiecutter.git,
          hg+https://bitbucket.org/foo/bar)

        :param url: Raw url parameter
        :return: VCS.VCS.MatchLevel, repo_url (or None)
        """
        match = re.match(r'''(?:([\w\d]+)\+)?((\w+)://|\w+@)(\S+)''', url)

        if not match:
            return VCS.MatchLevel.NONE, ''

        prefix, protocol_raw, protocol, repo_path = match.groups()

        # Get repo url (without prefix)
        repo_url = ('' if protocol_raw is None else protocol_raw) + repo_path

        # If a protocol is stated, it has to be among the allowed protocols
        if protocol and protocol not in cls.allowed_protocols + cls.protocols:
            return VCS.MatchLevel.NONE, ''

        # If a VCS prefix is stated, it has to equal the VCS command
        # -> explicit match
        if prefix:
            if prefix == cls.cmd:
                return VCS.MatchLevel.EXPLICIT, repo_url
            else:
                return VCS.MatchLevel.NONE, ''

        # If the protocol is among the VCS-specific protocols,
        # return explicit match
        if protocol and protocol in cls.protocols:
            return VCS.MatchLevel.EXPLICIT, repo_url

        # If the repo url suffix is among the VCS-specific suffixes,
        # return explicit match
        if any(repo_path.endswith('.' + s) for s in cls.suffixes):
            return VCS.MatchLevel.EXPLICIT, repo_url

        # If the repo url contains an identifier, return implicit match
        if any(idt in repo_url for idt in cls.identifiers):
            return VCS.MatchLevel.IMPLICIT, repo_url

        return VCS.MatchLevel.NONE, ''

    @classmethod
    def is_installed(cls):
        """
        Check if VCS is installed.

        :return: (bool) is_installed
        """
        return bool(which(cls.cmd))

    @staticmethod
    def get_repo_dir(repo_name, clone_to_dir):
        """
        Get the path of the cloned repository.

        :return: repo_dir
        """
        return os.path.normpath(os.path.join(clone_to_dir, repo_name))

    @classmethod
    def clone(cls, repo_url, checkout, clone_to_dir, repo_dir):
        """
        Clone the repository.

        :param repo_url: Repository URL
        :param checkout: Branch/Revision to check out
        :param clone_to_dir: Working directory for the VCS
        :param repo_dir: Path of the cloned repository
        :raise subprocess.CalledProcessError: if the VCS returned an error
        """
        subprocess.check_output(  # nosec
            [cls.cmd, 'clone', repo_url], cwd=clone_to_dir, stderr=subprocess.STDOUT,
        )
        if checkout is not None:
            subprocess.check_output(  # nosec
                [cls.cmd, 'checkout', checkout], cwd=repo_dir, stderr=subprocess.STDOUT,
            )


class Git(VCS):
    """Git VCS class."""

    cmd = 'git'

    identifiers = ['git']
    protocols = ['git']
    suffixes = ['git']

    not_found_errors = ['not found']
    branch_errors = ['error: pathspec']

    @staticmethod
    def get_repo_dir(repo_name, clone_to_dir):
        """
        Get the path of the cloned repository.

        :return: repo_dir
        """
        repo_name = repo_name.split(':')[-1].rsplit('.git')[0]
        return os.path.normpath(os.path.join(clone_to_dir, repo_name))


class Hg(VCS):
    """Mercury VCS class."""

    cmd = 'hg'

    identifiers = ['hg', 'bitbucket']
    protocols = ['hg']
    suffixes = ['hg']

    not_found_errors = ['not found']
    branch_errors = ['unknown revision']


class SVN(VCS):
    """Subversion VCS class."""

    cmd = 'svn'

    identifiers = ['svn']
    protocols = ['svn']
    suffixes = []

    not_found_errors = ['unable to connect', 'doesn\'t exist']
    branch_errors = ['no such revision', 'syntax error in revision']

    @classmethod
    def match_repo_url(cls, url):
        """
        Check if the raw URL input matches SVN.

        :param url: Raw url parameter
        :return: VCS.VCS.MatchLevel, repo_url (or None)
        """
        level, repo_url = super().match_repo_url(url)

        # SVN-specific ssh prefix
        repo_url = re.sub(r'''^ssh://''', 'svn+ssh://', repo_url)

        return level, repo_url

    @classmethod
    def clone(cls, repo_url, checkout, clone_to_dir, repo_dir):
        """
        Clone the repository.

        :param repo_url: Repository URL
        :param checkout: Branch/Revision to check out
        :param clone_to_dir: Working directory for the VCS
        :param repo_dir: Path of the cloned repository
        :raise subprocess.CalledProcessError: if the VCS returned an error
        """
        # SVN SSH syntax: svn+ssh://private.com/myrepo
        command = [cls.cmd, 'export', repo_url]

        if checkout:
            command += ['-r', checkout]

        subprocess.check_output(  # nosec
            command, cwd=clone_to_dir, stderr=subprocess.STDOUT
        )


REPO_TYPES = [
    Git,
    Hg,
    SVN,
]


def is_repo_url(repo_url):
    """Return True if value is a repository URL."""
    return any(
        vcs.match_repo_url(repo_url)[0] != VCS.MatchLevel.NONE for vcs in REPO_TYPES
    )


def identify_repo(repo_url):
    """
    Determine if `repo_url` should be treated as a URL to a VCS repository.

    Repos can be identified by prepending "hg+", "git+" or "svn+"
    to the repo URL.

    :param repo_url: Repo URL of unknown type.
    :returns: (VCS, repo_url)
    :raise: UnknownRepoType if repo type could not be identified
    """
    implicit_choice = None

    for vcs in REPO_TYPES:
        level, url = vcs.match_repo_url(repo_url)

        if level == VCS.MatchLevel.EXPLICIT:
            return vcs, url
        elif level == VCS.MatchLevel.IMPLICIT and implicit_choice is None:
            implicit_choice = vcs, url

    if implicit_choice is not None:
        return implicit_choice

    raise UnknownRepoType


def is_vcs_installed(repo_type):
    """
    Check if the version control system for a repo type is installed.

    :param repo_type:
    """
    return bool(which(repo_type))


def clone(repo_url, checkout=None, clone_to_dir='.', no_input=False):
    """
    Clone a repo to the current directory.

    :param repo_url: Repo URL of unknown type.
    :param checkout: The branch, tag or commit ID to checkout after clone.
    :param clone_to_dir: The directory to clone to.
                         Defaults to the current directory.
    :param no_input: Suppress all user prompts when calling via API.
    :returns: str with path to the new directory of the repository.
    """
    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    # identify the repo_type
    vcs, repo_url = identify_repo(repo_url)

    # check that the appropriate VCS for the repo_type is installed
    if not vcs.is_installed():
        msg = "'{0}' is not installed.".format(vcs.cmd)
        raise VCSNotInstalled(msg)

    repo_url = repo_url.rstrip('/')
    repo_name = os.path.split(repo_url)[1]
    repo_dir = vcs.get_repo_dir(repo_name, clone_to_dir)
    logger.debug('repo_dir is {0}'.format(repo_dir))

    if os.path.isdir(repo_dir):
        clone = prompt_and_delete(repo_dir, no_input=no_input)
    else:
        clone = True

    if clone:
        try:
            vcs.clone(repo_url, checkout, clone_to_dir, repo_dir)
        except subprocess.CalledProcessError as clone_error:
            output = clone_error.output.decode('utf-8')

            # In case of error, print VCS output
            click.echo(
                'Cloning of {} repository {} returned an error:\n{}'.format(
                    vcs.cmd, repo_url, output
                )
            )

            if any(error in output.lower() for error in vcs.not_found_errors):
                raise RepositoryNotFound(
                    'The repository {} could not be found, '
                    'have you made a typo?'.format(repo_url)
                )
            if any(error in output.lower() for error in vcs.branch_errors):
                raise RepositoryCloneFailed(
                    'The {} branch of repository {} could not found, '
                    'have you made a typo?'.format(checkout, repo_url)
                )
            # Raise base subprocess error if SVN error can't be identified
            raise

    return repo_dir
