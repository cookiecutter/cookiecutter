"""
test_templates.

Tests to ensure inheritence templates are properly accessed and consumed.
"""

from pathlib import Path

import pytest

from cookiecutter import main


@pytest.fixture
def output_dir(tmpdir):
    """Fixture. Create and return custom temp directory for test."""
    return str(tmpdir.mkdir('templates'))


@pytest.mark.parametrize("template", ["include", "no-templates", "extends", "super"])
def test_build_templates(template, output_dir) -> None:
    """
    Verify Templates Design keywords.

    no-templates is a compatibility tests for repo without `templates` directory
    """
    project_dir = main.cookiecutter(
        f'tests/test-templates/{template}',
        no_input=True,
        output_dir=output_dir,
    )

    readme = Path(project_dir, 'requirements.txt').read_text()

    assert readme.split() == [
        "pip",
        "Click",
        "pytest",
    ]


def test_moved_templates(output_dir) -> None:
    """
    Verify inheritance template directory traversal via configuration
     setting in cookiecutter.json.
    """

    template = 'moved-templates/test-app'

    project_dir = main.cookiecutter(
        f'tests/test-templates/{template}',
        no_input=True,
        output_dir=output_dir,
    )

    readme = Path(project_dir, 'requirements.txt').read_text()

    assert readme.split() == [
        "pip",
        "Click",
        "pytest",
    ]
