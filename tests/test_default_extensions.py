# -*- coding: utf-8 -*-

"""
test_default_extensions.

Tests to ensure Jinja2 filters/extensions are available from within pre- and
post-gen hooks.
"""

import io
import os

import freezegun
import pytest

from cookiecutter.main import cookiecutter


@pytest.yield_fixture(autouse=True)
def freeze():
    freezer = freezegun.freeze_time("2015-12-09 23:33:01")
    freezer.start()
    yield
    freezer.stop()


def test_jinja2_time_extension(tmpdir):
    project_dir = cookiecutter(
        'tests/test-extensions/default/',
        no_input=True,
        output_dir=str(tmpdir)
    )
    changelog_file = os.path.join(project_dir, 'HISTORY.rst')
    assert os.path.isfile(changelog_file)

    with io.open(changelog_file, 'r', encoding='utf-8') as f:
        changelog_lines = f.readlines()

    expected_lines = [
        'History\n',
        '-------\n',
        '\n',
        '0.1.0 (2015-12-09)\n',
        '---------------------\n',
        '\n',
        'First release on PyPI.\n'
    ]
    assert expected_lines == changelog_lines
