"""Verify correct work of `_force_render` context option (issue #2205)."""

from pathlib import Path

import pytest

from cookiecutter import generate


@pytest.mark.usefixtures('clean_system')
def test_force_render_overrides_binary_false_positive(tmp_path) -> None:
    """Files starting with ``PACK`` are misclassified as binary by binaryornot.

    ``_force_render`` must force Jinja rendering for matching paths.
    """
    template = tmp_path / 'template'
    project = template / '{{cookiecutter.project_slug}}'
    project.mkdir(parents=True)
    # Content starts with PACK — binaryornot treats this as a binary signature.
    (project / 'Makefile').write_text(
        'PACKAGE_NAME := {{ cookiecutter.project_slug }}\n',
        encoding='utf-8',
    )
    (project / 'other.txt').write_text(
        'hello {{ cookiecutter.project_slug }}\n',
        encoding='utf-8',
    )

    out = tmp_path / 'out'
    out.mkdir()

    generate.generate_files(
        context={
            'cookiecutter': {
                'project_slug': 'example-package',
                '_force_render': ['Makefile', '*.mk'],
            }
        },
        repo_dir=str(template),
        output_dir=str(out),
    )

    makefile = Path(out, 'example-package', 'Makefile')
    assert makefile.is_file()
    assert makefile.read_text(encoding='utf-8') == 'PACKAGE_NAME := example-package\n'

    other = Path(out, 'example-package', 'other.txt')
    assert other.read_text(encoding='utf-8') == 'hello example-package\n'


@pytest.mark.usefixtures('clean_system')
def test_pack_prefix_without_force_render_skips_jinja(tmp_path) -> None:
    """Without ``_force_render``, PACK-prefixed text is still copied unrendered."""
    template = tmp_path / 'template'
    project = template / '{{cookiecutter.project_slug}}'
    project.mkdir(parents=True)
    (project / 'foo_file').write_text(
        'PACKAGE_NAME := {{ cookiecutter.project_slug }}\n',
        encoding='utf-8',
    )

    out = tmp_path / 'out'
    out.mkdir()

    generate.generate_files(
        context={'cookiecutter': {'project_slug': 'example-package'}},
        repo_dir=str(template),
        output_dir=str(out),
    )

    foo = Path(out, 'example-package', 'foo_file')
    assert foo.is_file()
    # binaryornot false-positive: left unrendered
    assert foo.read_text(encoding='utf-8') == (
        'PACKAGE_NAME := {{ cookiecutter.project_slug }}\n'
    )
