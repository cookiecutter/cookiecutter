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
        'Correct expansion for builtin abbreviations (github)',
        'Correct expansion for builtin abbreviations (gitlab)',
        'Correct expansion for builtin abbreviations (bitbucket)',
    ),
)
def test_abbreviation_expansion(template, abbreviations, expected_result) -> None:
    """Verify abbreviation unpacking."""
    expanded = expand_abbreviations(template, abbreviations)
    assert expanded == expected_result


def test_abbreviation_expansion_prefix_not_0_in_braces() -> None:
    """Verify abbreviation unpacking raises error on incorrect index."""
    with pytest.raises(IndexError):
        expand_abbreviations('xx:a', {'xx': '{1}'})
