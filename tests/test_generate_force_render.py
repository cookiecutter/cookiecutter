"""Verify correct work of `_force_render` context option.

The Makefile fixture ends with a NUL byte so `binaryornot` classifies it as
binary on every supported platform.
"""

from pathlib import Path

from binaryornot.check import is_binary

from cookiecutter import generate

PACKAGE_NAME_FILE = (
    'tests/test-generate-force-render/input{{cookiecutter.package_name}}/Makefile'
)


def test_force_render_overrides_binary_detection(tmp_path) -> None:
    """Files matching `_force_render` are rendered even if detected as binary."""
    assert is_binary(PACKAGE_NAME_FILE)

    generate.generate_files(
        context={
            'cookiecutter': {
                'package_name': 'my_package',
                '_force_render': ['Make*'],
            }
        },
        repo_dir='tests/test-generate-force-render',
        output_dir=tmp_path,
    )

    rendered_file = Path(tmp_path, 'inputmy_package/Makefile')
    assert rendered_file.read_text(encoding='utf-8') == (
        'PACKAGE_NAME := my_package\n\x00'
    )


def test_force_render_does_not_change_default_behavior(tmp_path) -> None:
    """Binary-like files are still copied without rendering by default."""
    generate.generate_files(
        context={'cookiecutter': {'package_name': 'my_package'}},
        repo_dir='tests/test-generate-force-render',
        output_dir=tmp_path,
    )

    copied_file = Path(tmp_path, 'inputmy_package/Makefile')
    assert copied_file.read_text(encoding='utf-8') == (
        'PACKAGE_NAME := {{ cookiecutter.package_name }}\n\x00'
    )


def test_copy_without_render_takes_precedence_over_force_render(tmp_path) -> None:
    """`_copy_without_render` wins when a file matches both settings."""
    generate.generate_files(
        context={
            'cookiecutter': {
                'package_name': 'my_package',
                '_copy_without_render': ['Makefile'],
                '_force_render': ['Make*'],
            }
        },
        repo_dir='tests/test-generate-force-render',
        output_dir=tmp_path,
    )

    copied_file = Path(tmp_path, 'inputmy_package/Makefile')
    assert copied_file.read_text(encoding='utf-8') == (
        'PACKAGE_NAME := {{ cookiecutter.package_name }}\n\x00'
    )
