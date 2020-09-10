"""Utility functions for handling and fetching repo archives in zip format."""
import os
import tempfile
from zipfile import BadZipFile, ZipFile

import requests

from cookiecutter.exceptions import InvalidZipRepository
from cookiecutter.prompt import read_repo_password
from cookiecutter.utils import make_sure_path_exists, prompt_and_delete

try:
    import boto3
except ImportError:
    pass


def is_s3_uri(zip_uri):
    """Return True if the ZIP file's URI points to S3."""
    return zip_uri.startswith('s3://')


def s3_paths(s3_uri):
    """Split an S3 URI into a bucket name and object name."""
    return s3_uri.replace('s3://', '').split('/', 1)


def s3_identifier(s3_uri):
    """Return the basename of an S3 URL."""
    _, obj = s3_paths(s3_uri)
    return obj.rsplit('/', 1)[1]


def presign_s3_uri(s3_uri, expiration=600):
    """Return a presigned URI for an S3 object."""
    s3 = boto3.client('s3')
    bucket, obj = s3_paths(s3_uri)
    return s3.generate_presigned_url(
        'get_object', Params={'Bucket': bucket, 'Key': obj}, ExpiresIn=expiration,
    )


def unzip(zip_uri, is_url, clone_to_dir='.', no_input=False, password=None):
    """Download and unpack a zipfile at a given URI.

    This will download the zipfile to the cookiecutter repository,
    and unpack into a temporary directory.

    :param zip_uri: The URI for the zipfile.
    :param is_url: Is the zip URI a URL or a file?
    :param clone_to_dir: The cookiecutter repository directory
        to put the archive into.
    :param no_input: Suppress any prompts
    :param password: The password to use when unpacking the repository.
    """
    # Ensure that clone_to_dir exists
    clone_to_dir = os.path.expanduser(clone_to_dir)
    make_sure_path_exists(clone_to_dir)

    if is_url:
        # Build the name of the cached zipfile,
        # and prompt to delete if it already exists.
        if is_s3_uri(zip_uri):
            identifier = s3_identifier(zip_uri)
            zip_uri = presign_s3_uri(zip_uri)
        else:
            identifier = zip_uri.rsplit('/', 1)[1]
        zip_path = os.path.join(clone_to_dir, identifier)

        if os.path.exists(zip_path):
            download = prompt_and_delete(zip_path, no_input=no_input)
        else:
            download = True

        if download:
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
            raise InvalidZipRepository('Zip repository {} is empty'.format(zip_uri))

        # The first record in the zipfile should be the directory entry for
        # the archive. If it isn't a directory, there's a problem.
        first_filename = zip_file.namelist()[0]
        if not first_filename.endswith('/'):
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
            'Zip repository {} is not a valid zip archive:'.format(zip_uri)
        )

    return unzip_path
