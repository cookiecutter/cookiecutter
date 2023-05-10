"""Verify Jinja2 filters/extensions are available from pre-gen/post-gen hooks."""
import os
import uuid
from pathlib import Path

import freezegun
import pytest

from cookiecutter.main import cookiecutter


@pytest.fixture(autouse=True)
def freeze():
    """Fixture. Make time stating during all tests in this file."""
    freezer = freezegun.freeze_time("2015-12-09 23:33:01")
    freezer.start()
    yield
    freezer.stop()


def test_jinja2_time_extension(tmp_path):
    """Verify Jinja2 time extension work correctly."""
    project_dir = cookiecutter(
        'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
    )
    changelog_file = os.path.join(project_dir, 'HISTORY.rst')
    assert os.path.isfile(changelog_file)

    with Path(changelog_file).open(encoding='utf-8') as f:
        changelog_lines = f.readlines()

    expected_lines = [
        'History\n',
        '-------\n',
        '\n',
        '0.1.0 (2015-12-09)\n',
        '------------------\n',
        '\n',
        'First release on PyPI.\n',
    ]
    assert expected_lines == changelog_lines


def test_jinja2_slugify_extension(tmp_path):
    """Verify Jinja2 slugify extension work correctly."""
    project_dir = cookiecutter(
        'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
    )

    assert os.path.basename(project_dir) == "it-s-slugified-foobar"


def test_jinja2_uuid_extension(tmp_path):
    """Verify Jinja2 uuid extension work correctly."""
    project_dir = cookiecutter(
        'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
    )
    changelog_file = os.path.join(project_dir, 'id')
    assert os.path.isfile(changelog_file)

    with Path(changelog_file).open(encoding='utf-8') as f:
        changelog_lines = f.readlines()

    uuid.UUID(changelog_lines[0], version=4)


def test_jinja2_secret_key_extension(tmp_path):
    """Verify Jinja2 secret key extension work correctly."""
    project_dir = cookiecutter(
        'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
    )
    secret_file = os.path.join(project_dir, 'secret')
    assert os.path.isfile(secret_file)

    with Path(secret_file).open(encoding='utf-8') as f:
        secret_key1, secret_key2 = f.read().split("\n")

    assert len(secret_key1) == 50
    assert len(secret_key2) == 50
    assert secret_key1 != secret_key2
