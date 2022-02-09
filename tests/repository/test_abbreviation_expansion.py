"""Collection of tests around common path and url shorthands."""
import pytest

from cookiecutter.config import BUILTIN_ABBREVIATIONS
from cookiecutter.repository import expand_abbreviations


@pytest.mark.parametrize(
    ('template', 'abbreviations', 'expected_result'),
    [
        ('foo', {'foo': 'bar'}, 'bar'),
        ('baz', {'foo': 'bar'}, 'baz'),
        ('xx:a', {'xx': '<{0}>'}, '<a>'),
        ('gh:a', {'gh': '<{0}>'}, '<a>'),
        ('xx:a', {'xx': '<>'}, '<>'),
        ('advanced', {'advanced': {'expansion': 'exp'}}, 'exp'),
        (
            'gh:pydanny/cookiecutter-django',
            BUILTIN_ABBREVIATIONS,
            'https://github.com/pydanny/cookiecutter-django.git',
        ),
        (
            'gl:pydanny/cookiecutter-django',
            BUILTIN_ABBREVIATIONS,
            'https://gitlab.com/pydanny/cookiecutter-django.git',
        ),
        (
            'bb:pydanny/cookiecutter-django',
            BUILTIN_ABBREVIATIONS,
            'https://bitbucket.org/pydanny/cookiecutter-django',
        ),
    ],
    ids=(
        'Simple expansion',
        'Skip expansion (expansion not an abbreviation)',
        'Expansion prefix',
        'expansion_override_builtin',
        'expansion_prefix_ignores_suffix',
        'abbreviation_with_advanced_expansion',
        'Correct expansion for builtin abbreviations (github)',
        'Correct expansion for builtin abbreviations (gitlab)',
        'Correct expansion for builtin abbreviations (bitbucket)',
    ),
)
def test_abbreviation_expansion(template, abbreviations, expected_result):
    """Verify abbreviation unpacking."""
    expanded, _ = expand_abbreviations(template, abbreviations)
    assert expanded == expected_result


def test_abbreviation_expansion_prefix_not_0_in_braces():
    """Verify abbreviation unpacking raises error on incorrect index."""
    with pytest.raises(IndexError):
        expand_abbreviations('xx:a', {'xx': '{1}'})


def test_abbreviation_with_directory():
    """Verify that we can expand advanced abbreviations with a directory"""
    template = "my-abbreviation"
    abbreviations = {
        "my-abbreviation": {
            "expansion": "the-expansion",
            "directory": "the-directory",
        }
    }
    expanded, directory = expand_abbreviations(template, abbreviations)
    assert expanded == "the-expansion"
    assert directory == "the-directory"
