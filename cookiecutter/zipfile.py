from __future__ import absolute_import

import os
import requests
import sys
from zipfile import ZipFile

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

    return ok_to_delete


def unzip(zip_url, is_url, clone_to_dir='.', no_input=False):
    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    if is_url:
        # Build the name of the cached zipfile,
        # and prompt to delete if it already exists.
        identifier = zip_url.rsplit('/', 1)[1]
        zip_path = os.path.join(clone_to_dir, identifier)

        if os.path.exists(zip_path):
            ok_to_delete = prompt_and_delete(zip_path, no_input=no_input)
        else:
            ok_to_delete = None

        # (Re) download the zipfile
        r = requests.get(zip_url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    else:
        # Just use the local zipfile as-is.
        zip_path = os.path.abspath(zip_url)
        ok_to_delete = None

    # Now unpack the repository. The zipfile will include
    # the name of the template as the top level directory;
    # Check if that directory already exists, and if so,
    # prompt for deletion. If we've previously OK'd deletion,
    # don't ask again.
    zip_file = ZipFile(zip_path)
    unzip_name = zip_file.namelist()[0][:-1]

    unzip_path = os.path.join(clone_to_dir, unzip_name)
    if os.path.exists(unzip_path):
        if ok_to_delete is None:
            ok_to_delete = prompt_and_delete(unzip_path, no_input=no_input)
        else:
            rmtree(unzip_path)

    # Extract the zip file
    zip_file.extractall(path=clone_to_dir)

    return unzip_path
