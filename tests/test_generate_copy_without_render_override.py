"""Verify correct work of `_copy_without_render` context option."""

import os
from pathlib import Path

import pytest

from cookiecutter import generate, utils


@pytest.mark.parametrize('skip_existing', [True, False])
@pytest.mark.parametrize('copy_path', ['raw.txt', 'assets'])
def test_skip_existing_copy_without_render(tmp_path, skip_existing, copy_path):
    """Preserve existing copied files only when skipping was requested."""
    repo = tmp_path / 'template'
    template = repo / '{{cookiecutter.project}}'
    template.mkdir(parents=True)
    output = tmp_path / 'output'
    project = output / 'example'
    project.mkdir(parents=True)
    relative_file = 'raw.txt' if copy_path == 'raw.txt' else 'assets/keep.txt'
    source = template / relative_file
    destination = project / relative_file
    source.parent.mkdir(parents=True, exist_ok=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('template content')
    destination.write_text('local changes')
    (template / 'new-raw.txt').write_text('{{ leave this raw }}')
    if copy_path == 'assets':
        (source.parent / 'nested').mkdir()
        (source.parent / 'nested' / 'new.txt').write_text('{{ leave this raw }}')
        (destination.parent / 'local-only.txt').write_text('local file')

    generate.generate_files(
        repo_dir=repo,
        output_dir=output,
        context={
            'cookiecutter': {
                'project': 'example',
                '_copy_without_render': [copy_path, 'new-raw.txt'],
            }
        },
        overwrite_if_exists=True,
        skip_if_file_exists=skip_existing,
        accept_hooks=False,
    )

    expected = 'local changes' if skip_existing else 'template content'
    assert destination.read_text() == expected
    assert (project / 'new-raw.txt').read_text() == '{{ leave this raw }}'
    if copy_path == 'assets':
        assert (
            destination.parent / 'nested' / 'new.txt'
        ).read_text() == '{{ leave this raw }}'
        assert (destination.parent / 'local-only.txt').exists() == skip_existing


@pytest.fixture
def remove_test_dir():
    """Fixture. Remove the folder that is created by the test."""
    yield
    if os.path.exists('test_copy_without_render'):
        utils.rmtree('test_copy_without_render')


@pytest.mark.usefixtures('clean_system', 'remove_test_dir')
def test_generate_copy_without_render_extensions() -> None:
    """Verify correct work of `_copy_without_render` context option.

    Some files/directories should be rendered during invocation,
    some just copied, without any modification.
    """
    # first run
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_copy_without_render',
                'render_test': 'I have been rendered!',
                '_copy_without_render': [
                    '*not-rendered',
                    'rendered/not_rendered.yml',
                    '*.txt',
                    '{{cookiecutter.repo_name}}-rendered/README.md',
                ],
            }
        },
        repo_dir='tests/test-generate-copy-without-render-override',
    )

    # second run with override flag to True
    generate.generate_files(
        context={
            'cookiecutter': {
                'repo_name': 'test_copy_without_render',
                'render_test': 'I have been rendered!',
                '_copy_without_render': [
                    '*not-rendered',
                    'rendered/not_rendered.yml',
                    '*.txt',
                    '{{cookiecutter.repo_name}}-rendered/README.md',
                ],
            }
        },
        overwrite_if_exists=True,
        repo_dir='tests/test-generate-copy-without-render',
    )

    dir_contents = os.listdir('test_copy_without_render')

    assert 'test_copy_without_render-not-rendered' in dir_contents
    assert 'test_copy_without_render-rendered' in dir_contents

    file_1 = Path('test_copy_without_render/README.txt').read_text()
    assert '{{cookiecutter.render_test}}' in file_1

    file_2 = Path('test_copy_without_render/README.rst').read_text()
    assert 'I have been rendered!' in file_2

    file_3 = Path(
        'test_copy_without_render/test_copy_without_render-rendered/README.txt'
    ).read_text()
    assert '{{cookiecutter.render_test}}' in file_3

    file_4 = Path(
        'test_copy_without_render/test_copy_without_render-rendered/README.rst'
    ).read_text()
    assert 'I have been rendered' in file_4

    file_5 = Path(
        'test_copy_without_render/'
        'test_copy_without_render-not-rendered/'
        'README.rst'
    ).read_text()
    assert '{{cookiecutter.render_test}}' in file_5

    file_6 = Path('test_copy_without_render/rendered/not_rendered.yml').read_text()
    assert '{{cookiecutter.render_test}}' in file_6

    file_7 = Path(
        'test_copy_without_render/' 'test_copy_without_render-rendered/' 'README.md'
    ).read_text()
    assert '{{cookiecutter.render_test}}' in file_7
