"""Verify Jinja2 filters/extensions are available from pre-gen/post-gen hooks."""

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


def test_jinja2_time_extension(tmp_path) -> None:
    """Verify Jinja2 time extension work correctly."""
    project_dir = Path(
        cookiecutter(
            'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
        )
    )
    changelog_file = project_dir / 'HISTORY.rst'
    assert changelog_file.exists()

    with changelog_file.open(encoding='utf-8') as f:
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


def test_jinja2_slugify_extension(tmp_path) -> None:
    """Verify Jinja2 slugify extension work correctly."""
    project_dir = Path(
        cookiecutter(
            'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
        )
    )

    assert project_dir.name == "it-s-slugified-foobar"


def test_jinja2_uuid_extension(tmp_path) -> None:
    """Verify Jinja2 uuid extension work correctly."""
    project_dir = Path(
        cookiecutter(
            'tests/test-extensions/default/', no_input=True, output_dir=str(tmp_path)
        )
    )
    changelog_file = project_dir / 'id'
    assert changelog_file.is_file()

    changelog_lines = changelog_file.read_text(encoding='utf-8').strip()

    uuid.UUID(changelog_lines, version=4)
