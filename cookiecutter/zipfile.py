from __future__ import absolute_import

import os
import requests
import sys
import tempfile
from zipfile import ZipFile
try:
    from zipfile import BadZipFile
except ImportError:
    from zipfile import BadZipfile as BadZipFile

from .exceptions import InvalidZipRepository
from .prompt import read_user_yes_no
from .utils import make_sure_path_exists, rmtree


def prompt_and_delete(path, no_input=False):
    """Ask the user whether it's okay to delete the previously-downloaded
    file/directory.

    If yes, deletes it. Otherwise, Cookiecutter exits.

    :param path: Previously downloaded zipfile.
    :param no_input: Suppress prompt to delete repo and just delete it.
    """
    # Suppress prompt if called via API
    if no_input:
        ok_to_delete = True
    else:
        question = (
            "You've downloaded {} before. "
            "Is it okay to delete and re-download it?"
        ).format(path)

        ok_to_delete = read_user_yes_no(question, 'yes')

    if ok_to_delete:
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)
    else:
        sys.exit()


def unzip(zip_uri, is_url, clone_to_dir='.', no_input=False):
    """Download and unpack a zipfile at a given URI.

    This will download the zipfile to the cookiecutter repository,
    and unpack into a temporary directory.

    :param zip_uri: The URI for the zipfile.
    :param is_url: Is the zip URI a URL or a file?
    :param clone_to_dir: The cookiecutter repository directory
        to put the archive into.
    :param no_input: Supress any prompts
    """
    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    if is_url:
        # Build the name of the cached zipfile,
        # and prompt to delete if it already exists.
        identifier = zip_uri.rsplit(os.path.sep, 1)[1]
        zip_path = os.path.join(clone_to_dir, identifier)

        if os.path.exists(zip_path):
            prompt_and_delete(zip_path, no_input=no_input)

        # (Re) download the zipfile
        r = requests.get(zip_uri, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        # Just use the local zipfile as-is.
        zip_path = os.path.abspath(zip_uri)

    # Now unpack the repository. The zipfile will be unpacked
    # into a temporary directory
    try:
        zip_file = ZipFile(zip_path)

        if len(zip_file.namelist()) == 0:
            raise InvalidZipRepository(
                'Zip repository {} is empty'.format(zip_uri)
            )

        # The first record in the zipfile should be the directory entry for
        # the archive. If it isn't a directory, there's a problem.
        first_filename = zip_file.namelist()[0]
        if not first_filename.endswith(os.path.sep):
            raise InvalidZipRepository(
                'Zip repository {} does not include '
                'a top-level directory'.format(zip_uri)
            )

        # Construct the final target directory
        project_name = first_filename[:-1]
        unzip_base = tempfile.mkdtemp()
        unzip_path = os.path.join(unzip_base, project_name)

        # Extract the zip file into the temporary directory
        try:
            zip_file.extractall(path=unzip_base)
        except RuntimeError:
            # File is encrypted; in the future, we can get a password
            # and retry here.
            raise InvalidZipRepository(
                'Zip repository {} is password protected'.format(zip_uri)
            )

    except BadZipFile:
        raise InvalidZipRepository(
            'Zip repository {} is not a valid zip archive:'.format(zip_uri)
        )

    return unzip_path
