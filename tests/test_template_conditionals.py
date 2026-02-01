"""
Test files are correctly conditionally included/excluded by path variable expansion.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from cookiecutter import main


def make_fixture(name: str):
    def fn(request: pytest.FixtureRequest) -> bool:
        return bool(request.param)

    fn.__name__ = name
    return pytest.fixture(params=[True, False], ids=[f'yes_{name}', f'no_{name}'])(fn)


include_root_file = make_fixture('include_root_file')
include_root_folder = make_fixture('include_root_folder')
include_single_nested_file = make_fixture('include_single_nested_file')
include_single_nested_folder = make_fixture('include_single_nested_folder')
include_double_nested_file = make_fixture('include_double_nested_file')
include_double_nested_folder = make_fixture('include_double_nested_folder')
include_triple_nested_file = make_fixture('include_triple_nested_file')


@pytest.fixture
def expect_root_file(include_root_file: bool) -> bool:
    return include_root_file


@pytest.fixture
def expect_root_folder(include_root_folder: bool) -> bool:
    return include_root_folder


@pytest.fixture
def expect_single_nested_file(
    expect_root_folder: bool,
    include_single_nested_file: bool,
) -> bool:
    return expect_root_folder and include_single_nested_file


@pytest.fixture
def expect_single_nested_folder(
    expect_root_folder: bool,
    include_single_nested_folder: bool,
) -> bool:
    return expect_root_folder and include_single_nested_folder


@pytest.fixture
def expect_double_nested_file(
    expect_single_nested_folder: bool,
    include_double_nested_file: bool,
) -> bool:
    return expect_single_nested_folder and include_double_nested_file


@pytest.fixture
def expect_double_nested_folder(
    expect_single_nested_folder: bool,
    include_double_nested_folder: bool,
) -> bool:
    return expect_single_nested_folder and include_double_nested_folder


@pytest.fixture
def expect_triple_nested_file(
    expect_double_nested_folder: bool,
    include_triple_nested_file: bool,
) -> bool:
    return expect_double_nested_folder and include_triple_nested_file


@pytest.fixture
def expected_tree(
    expect_root_file: bool,
    expect_root_folder: bool,
    expect_single_nested_file: bool,
    expect_single_nested_folder: bool,
    expect_double_nested_file: bool,
    expect_double_nested_folder: bool,
    expect_triple_nested_file: bool,
) -> set[str]:
    expected_files: tuple[tuple[bool, str], ...] = (
        (expect_root_file, 'project/root_file'),
        (expect_root_folder, 'project/root_folder'),
        (expect_single_nested_file, 'project/root_folder/single_nested_file'),
        (expect_single_nested_folder, 'project/root_folder/single_nested_folder'),
        (
            expect_double_nested_file,
            'project/root_folder/single_nested_folder/double_nested_file',
        ),
        (
            expect_double_nested_folder,
            'project/root_folder/single_nested_folder/double_nested_folder',
        ),
        (
            expect_triple_nested_file,
            'project/root_folder/single_nested_folder/double_nested_folder/triple_nested_file',
        ),
    )

    return {
        path.replace('/', os.sep) for is_expected, path in expected_files if is_expected
    }


@pytest.fixture
def context(
    include_root_file: bool,
    include_root_folder: bool,
    include_single_nested_file: bool,
    include_single_nested_folder: bool,
    include_double_nested_file: bool,
    include_double_nested_folder: bool,
    include_triple_nested_file: bool,
) -> dict[str, bool]:
    return {
        'include_root_file': include_root_file,
        'include_root_folder': include_root_folder,
        'include_single_nested_file': include_single_nested_file,
        'include_single_nested_folder': include_single_nested_folder,
        'include_double_nested_file': include_double_nested_file,
        'include_double_nested_folder': include_double_nested_folder,
        'include_triple_nested_file': include_triple_nested_file,
    }


def glob_tree(path: Path) -> set[str]:
    glob_tree = (path / 'project').glob('**/*')
    strip_chrs = len(str(path)) + 1

    tree = {str(sub_path)[strip_chrs:] for sub_path in glob_tree}
    tree.discard('project')

    return tree


def test_expanded_paths_with_empty_segments_should_be_skipped(
    context: dict[str, str | bool],
    tmp_path: Path,
    expected_tree: set[str],
):
    test_dir = Path(__file__).absolute().parent
    repo_dir = test_dir / 'test-templates' / 'conditionals'

    main.cookiecutter(
        str(repo_dir),
        no_input=True,
        output_dir=str(tmp_path),
        extra_context=context,
    )

    generated_paths = glob_tree(tmp_path)

    assert generated_paths == expected_tree
