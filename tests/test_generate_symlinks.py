"""Tests for `generate.py` that have symlinks in the templates."""

from __future__ import unicode_literals
import os
import shutil

import pytest

from cookiecutter import generate
from cookiecutter import utils


TEST_OUTPUT_DIR = 'test_symlinks'


@pytest.fixture(scope='function')
def remove_test_dir(request):
    """Remove the folder that is created by the test."""

    def fin_remove_test_dir():
        if os.path.exists(TEST_OUTPUT_DIR):
            utils.rmtree(TEST_OUTPUT_DIR)

    request.addfinalizer(fin_remove_test_dir)


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_symlinks():
    """
    Verify generating projects with symlinks.

    Includes both rendered and non-rendered symlink paths.
    """
    generate.generate_files(
        context={
            'cookiecutter': {
                'name': TEST_OUTPUT_DIR,
                "link_dir": "rendered_dir",
                "sym_to_nontemp": "rendered_sym_to_original",
                "sym_to_temp": "rendered_sym_to_rendered_dir",
                "_copy_without_render": ["copy_no_render"],
            }
        },
        repo_dir='tests/test-generate-symlinks',
    )

    dir_contents = os.listdir(TEST_OUTPUT_DIR)

    assert 'copy_no_render' in dir_contents
    assert 'original' in dir_contents
    assert 'rendered_dir' in dir_contents
    assert 'rendered_sym_to_original' in dir_contents
    assert 'rendered_sym_to_rendered_dir' in dir_contents
    assert 'symlink' in dir_contents

    # Test links that have been rendered and copied
    def _test_symlink(root, link, points_to):
        assert os.path.islink(os.path.join(root, link))

        actual_points_to = os.readlink(os.path.join(root, link))

        if actual_points_to.endswith(os.sep):
            actual_points_to = actual_points_to[:-1]

        assert actual_points_to == points_to

    # normal symlink, not rendered target
    _test_symlink(TEST_OUTPUT_DIR, 'symlink', 'original')

    # normal symlink, rendered target
    _test_symlink(TEST_OUTPUT_DIR, 'symlink_to_rendered', 'rendered_dir')

    # rendered symlink, not rendered target
    _test_symlink(TEST_OUTPUT_DIR, 'rendered_sym_to_original', 'original')

    # rendered symlink, rendered target
    _test_symlink(TEST_OUTPUT_DIR, 'rendered_sym_to_rendered_dir', 'rendered_dir')

    # Test links that have not been rendered
    non_rendered_dir = os.path.join(TEST_OUTPUT_DIR, 'copy_no_render')
    non_rendered_dir_contents = os.listdir(non_rendered_dir)

    assert 'original' in non_rendered_dir_contents
    assert 'symlink' in non_rendered_dir_contents
    assert 'symlink_to_rendered' in non_rendered_dir_contents
    assert '{{ cookiecutter.link_dir }}' in non_rendered_dir_contents
    assert '{{ cookiecutter.sym_to_nontemp }}' in non_rendered_dir_contents
    assert '{{ cookiecutter.sym_to_temp }}' in non_rendered_dir_contents

    # normal symlink, not rendered target
    _test_symlink(non_rendered_dir, 'symlink', 'original')

    # normal symlink, rendered target
    _test_symlink(
        non_rendered_dir, 'symlink_to_rendered', '{{ cookiecutter.link_dir }}'
    )

    # rendered symlink, not rendered target
    _test_symlink(non_rendered_dir, '{{ cookiecutter.sym_to_nontemp }}', 'original')

    # rendered symlink, rendered target
    _test_symlink(
        non_rendered_dir,
        '{{ cookiecutter.sym_to_temp }}',
        '{{ cookiecutter.link_dir }}',
    )

    # test overwriting + symlinks
    utils.rmtree(TEST_OUTPUT_DIR)  # remove output
    os.makedirs(os.path.join(TEST_OUTPUT_DIR, "symlink"))
    shutil.copy(
        os.path.join("tests", "test-generate-symlinks", "cookiecutter.json"),
        os.path.join(
            TEST_OUTPUT_DIR, "symlink", "afile.txt"
        ),  # copy to where output will exist
    )
    generate.generate_files(
        context={
            'cookiecutter': {
                'name': TEST_OUTPUT_DIR,
                "link_dir": "rendered_dir",
                "sym_to_nontemp": "rendered_sym_to_original",
                "sym_to_temp": "rendered_sym_to_rendered_dir",
                "_copy_without_render": ["copy_no_render"],
            }
        },
        repo_dir=os.path.join('tests', 'test-generate-symlinks'),
        overwrite_if_exists=True,  # overwrite the symlink
    )

    # normal symlink, not rendered target
    _test_symlink(non_rendered_dir, 'symlink', 'original')
