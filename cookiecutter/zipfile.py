"""Utility functions for handling and fetching repo archives in zip format."""
import os
import tempfile
from pathlib import Path
from typing import Optional
from zipfile import BadZipFile, ZipFile

import requests

from cookiecutter.exceptions import InvalidZipRepository
from cookiecutter.prompt import read_repo_password
from cookiecutter.utils import make_sure_path_exists, prompt_and_delete


def unzip(
    zip_uri: str,
    is_url: bool,
    clone_to_dir: "os.PathLike[str]" = ".",
    no_input: bool = False,
    password: Optional[str] = None,
):
    """Download and unpack a zipfile at a given URI.

    This will download the zipfile to the cookiecutter repository,
    and unpack into a temporary directory.

    :param zip_uri: The URI for the zipfile.
    :param is_url: Is the zip URI a URL or a file?
    :param clone_to_dir: The cookiecutter repository directory
        to put the archive into.
    :param no_input: Do not prompt for user input and eventually force a refresh of
        cached resources.
    :param password: The password to use when unpacking the repository.
    """
    # Ensure that clone_to_dir exists
    clone_to_dir = Path(clone_to_dir).expanduser()
    make_sure_path_exists(clone_to_dir)

    if is_url:
        # Build the name of the cached zipfile,
        # and prompt to delete if it already exists.
        identifier = zip_uri.rsplit('/', 1)[1]
        zip_path = os.path.join(clone_to_dir, identifier)

        if os.path.exists(zip_path):
            download = prompt_and_delete(zip_path, no_input=no_input)
        else:
            download = True

        if download:
            # (Re) download the zipfile
            r = requests.get(zip_uri, stream=True, timeout=100)
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
            raise InvalidZipRepository(f'Zip repository {zip_uri} is empty')

        # The first record in the zipfile should be the directory entry for
        # the archive. If it isn't a directory, there's a problem.
        first_filename = zip_file.namelist()[0]
        if not first_filename.endswith('/'):
            raise InvalidZipRepository(
                f"Zip repository {zip_uri} does not include a top-level directory"
            )

        # Construct the final target directory
        project_name = first_filename[:-1]
        unzip_base = tempfile.mkdtemp()
        unzip_path = os.path.join(unzip_base, project_name)

        # Extract the zip file into the temporary directory
        try:
            zip_file.extractall(path=unzip_base)
        except RuntimeError:
            # File is password protected; try to get a password from the
            # environment; if that doesn't work, ask the user.
            if password is not None:
                try:
                    zip_file.extractall(path=unzip_base, pwd=password.encode('utf-8'))
                except RuntimeError:
                    raise InvalidZipRepository(
                        'Invalid password provided for protected repository'
                    )
            elif no_input:
                raise InvalidZipRepository(
                    'Unable to unlock password protected repository'
                )
            else:
                retry = 0
                while retry is not None:
                    try:
                        password = read_repo_password('Repo password')
                        zip_file.extractall(
                            path=unzip_base, pwd=password.encode('utf-8')
                        )
                        retry = None
                    except RuntimeError:
                        retry += 1
                        if retry == 3:
                            raise InvalidZipRepository(
                                'Invalid password provided for protected repository'
                            )

    except BadZipFile:
        raise InvalidZipRepository(
            f'Zip repository {zip_uri} is not a valid zip archive:'
        )

    return unzip_path
