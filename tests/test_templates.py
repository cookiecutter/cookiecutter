"""
test_custom_extension_in_hooks.

Tests to ensure custom cookiecutter extensions are properly made available to
pre- and post-gen hooks.
"""
import codecs
import os

import pytest

from cookiecutter import main


@pytest.fixture
def output_dir(tmpdir):
    """Fixture. Create and return custom temp directory for test."""
    return str(tmpdir.mkdir('templates'))


@pytest.mark.parametrize("template", ["include", "no-templates", "extends", "super"])
def test_build_templates(template, output_dir):
    """
    Verify Templates Design keywords.

    no-templates is a compatibility tests for repo without `templates` directory
    """
    project_dir = main.cookiecutter(
        f'tests/test-templates/{template}', no_input=True, output_dir=output_dir,
    )

    readme_file = os.path.join(project_dir, 'requirements.txt')

    with codecs.open(readme_file, encoding='utf8') as f:
        readme = f.read().splitlines()

    assert readme == [
        "pip==19.2.3",
        "Click==7.0",
        "pytest==4.6.5",
    ]
