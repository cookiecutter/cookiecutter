"""Verify generate context behaviour and context overwrite priorities."""

from __future__ import annotations

import os
import re
from collections import OrderedDict
from collections.abc import Iterator
from typing import Any

import pytest

from cookiecutter import generate
from cookiecutter.exceptions import ContextDecodingException
from cookiecutter.prompt import YesNoPrompt


def context_data() -> Iterator[tuple[dict[str, Any], dict[str, Any]]]:
    """Generate pytest parametrization variables for test.

    Return ('input_params, expected_context') tuples.
    """
    context = (
        {'context_file': 'tests/test-generate-context/test.json'},
        {'test': {'1': 2, 'some_key': 'some_val'}},
    )

    context_with_default = (
        {
            'context_file': 'tests/test-generate-context/test.json',
            'default_context': {'1': 3},
        },
        {'test': {'1': 3, 'some_key': 'some_val'}},
    )

    context_with_extra = (
        {
            'context_file': 'tests/test-generate-context/test.json',
            'extra_context': {'1': 4},
        },
        {'test': {'1': 4, 'some_key': 'some_val'}},
    )

    context_with_default_and_extra = (
        {
            'context_file': 'tests/test-generate-context/test.json',
            'default_context': {'1': 3},
            'extra_context': {'1': 5},
        },
        {'test': {'1': 5, 'some_key': 'some_val'}},
    )

    yield context
    yield context_with_default
    yield context_with_extra
    yield context_with_default_and_extra


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data())
def test_generate_context(input_params, expected_context) -> None:
    """Verify input contexts combinations result in expected content on output."""
    assert generate.generate_context(**input_params) == expected_context


@pytest.mark.usefixtures('clean_system')
def test_generate_context_with_json_decoding_error() -> None:
    """Verify malformed JSON file generates expected error output."""
    with pytest.raises(ContextDecodingException) as excinfo:
        generate.generate_context('tests/test-generate-context/invalid-syntax.json')
    # original message from json module should be included
    pattern = 'Expecting \'{0,1}:\'{0,1} delimiter: line 1 column (19|20) \\(char 19\\)'
    assert re.search(pattern, str(excinfo.value))
    # File name should be included too...for testing purposes, just test the
    # last part of the file. If we wanted to test the absolute path, we'd have
    # to do some additional work in the test which doesn't seem that needed at
    # this point.
    path = os.path.sep.join(['tests', 'test-generate-context', 'invalid-syntax.json'])
    assert path in str(excinfo.value)


def test_default_context_replacement_in_generate_context() -> None:
    """Verify default content settings are correctly replaced by template settings.

    Make sure that the default for list variables of `orientation` is based on
    the user config (`choices_template.json`) and not changed to a single value
    from `default_context`.
    """
    expected_context = {
        'choices_template': OrderedDict(
            [
                ('full_name', 'Raphael Pierzina'),
                ('github_username', 'hackebrot'),
                ('project_name', 'Kivy Project'),
                ('repo_name', '{{cookiecutter.project_name|lower}}'),
                ('orientation', ['landscape', 'all', 'portrait']),
            ]
        )
    }

    generated_context = generate.generate_context(
        context_file='tests/test-generate-context/choices_template.json',
        default_context={
            'not_in_template': 'foobar',
            'project_name': 'Kivy Project',
            'orientation': 'landscape',
        },
        extra_context={
            'also_not_in_template': 'foobar2',
            'github_username': 'hackebrot',
        },
    )

    assert generated_context == expected_context


def test_generate_context_decodes_non_ascii_chars() -> None:
    """Verify `generate_context` correctly decodes non-ascii chars."""
    expected_context = {
        'non_ascii': OrderedDict(
            [
                ('full_name', 'éèà'),
            ]
        )
    }

    generated_context = generate.generate_context(
        context_file='tests/test-generate-context/non_ascii.json'
    )

    assert generated_context == expected_context


@pytest.fixture
def template_context():
    """Fixture. Populates template content for future tests."""
    return OrderedDict(
        [
            ('full_name', 'Raphael Pierzina'),
            ('github_username', 'hackebrot'),
            ('project_name', 'Kivy Project'),
            ('repo_name', '{{cookiecutter.project_name|lower}}'),
            ('orientation', ['all', 'landscape', 'portrait']),
            ('deployment_regions', ['eu', 'us', 'ap']),
            (
                'deployments',
                {
                    'preprod': ['eu', 'us', 'ap'],
                    'prod': ['eu', 'us', 'ap'],
                },
            ),
        ]
    )


def test_apply_overwrites_does_include_unused_variables(template_context) -> None:
    """Verify `apply_overwrites_to_context` skips variables that are not in context."""
    generate.apply_overwrites_to_context(
        context=template_context, overwrite_context={'not in template': 'foobar'}
    )

    assert 'not in template' not in template_context


def test_apply_overwrites_sets_non_list_value(template_context) -> None:
    """Verify `apply_overwrites_to_context` work with string variables."""
    generate.apply_overwrites_to_context(
        context=template_context, overwrite_context={'repo_name': 'foobar'}
    )

    assert template_context['repo_name'] == 'foobar'


def test_apply_overwrites_does_not_modify_choices_for_invalid_overwrite() -> None:
    """Verify variables overwrite for list if variable not in list ignored."""
    expected_context = {
        'choices_template': OrderedDict(
            [
                ('full_name', 'Raphael Pierzina'),
                ('github_username', 'hackebrot'),
                ('project_name', 'Kivy Project'),
                ('repo_name', '{{cookiecutter.project_name|lower}}'),
                ('orientation', ['all', 'landscape', 'portrait']),
            ]
        )
    }

    with pytest.warns(UserWarning, match="Invalid default received"):
        generated_context = generate.generate_context(
            context_file='tests/test-generate-context/choices_template.json',
            default_context={
                'not_in_template': 'foobar',
                'project_name': 'Kivy Project',
                'orientation': 'foobar',
            },
            extra_context={
                'also_not_in_template': 'foobar2',
                'github_username': 'hackebrot',
            },
        )

    assert generated_context == expected_context


def test_apply_overwrites_invalid_overwrite(template_context) -> None:
    """Verify variables overwrite for list if variable not in list not ignored."""
    with pytest.raises(ValueError):
        generate.apply_overwrites_to_context(
            context=template_context, overwrite_context={'orientation': 'foobar'}
        )


def test_apply_overwrites_sets_multichoice_values(template_context) -> None:
    """Verify variable overwrite for list given multiple valid values."""
    generate.apply_overwrites_to_context(
        context=template_context,
        overwrite_context={'deployment_regions': ['eu']},
    )
    assert template_context['deployment_regions'] == ['eu']


def test_apply_overwrites_invalid_multichoice_values(template_context) -> None:
    """Verify variable overwrite for list given invalid list entries not ignored."""
    with pytest.raises(ValueError):
        generate.apply_overwrites_to_context(
            context=template_context,
            overwrite_context={'deployment_regions': ['na']},
        )


def test_apply_overwrites_error_additional_values(template_context) -> None:
    """Verify variable overwrite for list given additional entries not ignored."""
    with pytest.raises(ValueError):
        generate.apply_overwrites_to_context(
            context=template_context,
            overwrite_context={'deployment_regions': ['eu', 'na']},
        )


def test_apply_overwrites_in_dictionaries(template_context) -> None:
    """Verify variable overwrite for lists nested in dictionary variables."""
    generate.apply_overwrites_to_context(
        context=template_context,
        overwrite_context={'deployments': {'preprod': ['eu'], 'prod': ['ap']}},
    )
    assert template_context['deployments']['preprod'] == ['eu']
    assert template_context['deployments']['prod'] == ['ap']


def test_apply_overwrites_sets_default_for_choice_variable(template_context) -> None:
    """Verify overwritten list member became a default value."""
    generate.apply_overwrites_to_context(
        context=template_context, overwrite_context={'orientation': 'landscape'}
    )

    assert template_context['orientation'] == ['landscape', 'all', 'portrait']


def test_apply_overwrites_in_nested_dict() -> None:
    """Verify nested dict in default content settings are correctly replaced."""
    expected_context = {
        'nested_dict': OrderedDict(
            [
                ('full_name', 'Raphael Pierzina'),
                ('github_username', 'hackebrot'),
                (
                    'project',
                    OrderedDict(
                        [
                            ('name', 'My Kivy Project'),
                            ('description', 'My Kivy Project'),
                            ('repo_name', '{{cookiecutter.project_name|lower}}'),
                            ('orientation', ["all", "landscape", "portrait"]),
                        ]
                    ),
                ),
            ]
        )
    }

    generated_context = generate.generate_context(
        context_file='tests/test-generate-context/nested_dict.json',
        default_context={
            'not_in_template': 'foobar',
            'project': {
                'description': 'My Kivy Project',
            },
        },
        extra_context={
            'also_not_in_template': 'foobar2',
            'github_username': 'hackebrot',
            'project': {
                'name': 'My Kivy Project',
            },
        },
    )

    assert generated_context == expected_context


def test_apply_overwrite_context_as_in_nested_dict_with_additional_values() -> None:
    """Verify nested dict in default content settings are correctly added.

    The `apply_overwrites_to_context` function should add the extra values to the dict.
    """
    expected = OrderedDict({"key1": "value1", "key2": "value2"})
    context = OrderedDict({"key1": "value1"})
    overwrite_context = OrderedDict({"key2": "value2"})
    generate.apply_overwrites_to_context(
        context,
        overwrite_context,
        in_dictionary_variable=True,
    )
    assert context == expected


def test_apply_overwrites_in_nested_dict_additional_values() -> None:
    """Verify nested dict in default content settings are correctly added."""
    expected_context = {
        'nested_dict_additional': OrderedDict(
            [
                ('mainkey1', 'mainvalue1'),
                (
                    'mainkey2',
                    OrderedDict(
                        [
                            ('subkey1', 'subvalue1'),
                            (
                                'subkey2',
                                OrderedDict(
                                    [
                                        ('subsubkey1', 'subsubvalue1'),
                                        ('subsubkey2', 'subsubvalue2_default'),
                                        ('subsubkey3', 'subsubvalue3_extra'),
                                    ]
                                ),
                            ),
                            ('subkey4', 'subvalue4_default'),
                            ('subkey5', 'subvalue5_extra'),
                        ]
                    ),
                ),
            ]
        )
    }

    generated_context = generate.generate_context(
        context_file='tests/test-generate-context/nested_dict_additional.json',
        default_context={
            'not_in_template': 'foobar',
            'mainkey2': {
                'subkey2': {
                    'subsubkey2': 'subsubvalue2_default',
                },
                'subkey4': 'subvalue4_default',
            },
        },
        extra_context={
            'also_not_in_template': 'foobar2',
            'mainkey2': {
                'subkey2': {
                    'subsubkey3': 'subsubvalue3_extra',
                },
                'subkey5': 'subvalue5_extra',
            },
        },
    )

    assert generated_context == expected_context


@pytest.mark.parametrize(
    "overwrite_value, expected",
    [(bool_string, {'key': True}) for bool_string in YesNoPrompt.yes_choices]
    + [(bool_string, {'key': False}) for bool_string in YesNoPrompt.no_choices],
)
def test_apply_overwrites_overwrite_value_as_boolean_string(overwrite_value, expected):
    """Verify boolean conversion for valid overwrite values."""
    context = {'key': not expected['key']}
    overwrite_context = {'key': overwrite_value}
    generate.apply_overwrites_to_context(context, overwrite_context)
    assert context == expected


def test_apply_overwrites_error_overwrite_value_as_boolean_string():
    """Verify boolean conversion for invalid overwrite values."""
    context = {'key': True}
    overwrite_context = {'key': 'invalid'}
    with pytest.raises(ValueError):
        generate.apply_overwrites_to_context(context, overwrite_context)


def test_apply_overwrites_continues_after_invalid_entry(template_context) -> None:
    """Valid entries after an invalid one are still applied.

    Regression test for gh-2219: the first invalid entry used to raise
    ValueError immediately, causing every subsequent (potentially valid)
    entry in the overwrite dict to be silently dropped.
    """
    with pytest.raises(ValueError) as excinfo:
        generate.apply_overwrites_to_context(
            context=template_context,
            overwrite_context={
                # Invalid choice — should be collected, not raised immediately
                'orientation': 'foobar',
                # Valid overwrite — MUST still be applied
                'repo_name': 'should-be-applied',
            },
        )
    # The valid entry should have been applied before the error is raised
    assert template_context['repo_name'] == 'should-be-applied'
    # The error message should mention the offending variable
    assert 'orientation' in str(excinfo.value)


def test_apply_overwrites_collects_all_errors() -> None:
    """All invalid entries are reported, not just the first one."""
    context = OrderedDict(
        [
            ('choice_var', ['a', 'b', 'c']),
            ('multi_var', ['x', 'y', 'z']),
            ('bool_var', False),
        ]
    )
    with pytest.raises(ValueError) as excinfo:
        generate.apply_overwrites_to_context(
            context=context,
            overwrite_context={
                'choice_var': 'invalid',
                'multi_var': ['w'],
                'bool_var': 'not-a-bool',
            },
        )
    msg = str(excinfo.value)
    assert 'choice_var' in msg
    assert 'multi_var' in msg
    assert 'bool_var' in msg


def test_apply_overwrites_nested_error_collection() -> None:
    """Errors from nested dict entries are collected with parent prefix."""
    context = OrderedDict(
        [
            ('key1', 'value1'),
            (
                'nested',
                OrderedDict(
                    [
                        ('bool_a', True),
                        ('bool_b', False),
                    ]
                ),
            ),
        ]
    )
    with pytest.raises(ValueError) as excinfo:
        generate.apply_overwrites_to_context(
            context=context,
            overwrite_context={
                'nested': {
                    'bool_a': 'invalid-a',
                    'bool_b': 'invalid-b',
                },
            },
        )
    msg = str(excinfo.value)
    # Both nested errors should be reported with the parent prefix
    assert 'nested:' in msg
    assert 'bool_a' in msg
    assert 'bool_b' in msg


def test_apply_overwrites_no_error_when_all_valid(template_context) -> None:
    """No exception is raised when all overwrites are valid."""
    generate.apply_overwrites_to_context(
        context=template_context,
        overwrite_context={
            'repo_name': 'new-repo',
            'orientation': 'landscape',
        },
    )
    assert template_context['repo_name'] == 'new-repo'
    # orientation should be moved to front (choice variable default)
    assert template_context['orientation'][0] == 'landscape'


def test_generate_context_reports_all_invalid_defaults() -> None:
    """generate_context warns about all invalid default_context entries,
    not just the first one, and still applies valid entries that follow."""
    with pytest.warns(UserWarning, match="Invalid default received") as record:
        generated = generate.generate_context(
            context_file='tests/test-generate-context/choices_template.json',
            default_context={
                # Valid — should be applied
                'project_name': 'Kivy Project',
                # Invalid choice — should warn but not block later entries
                'orientation': 'foobar',
                # Valid — should still be applied since the loop no longer
                # exits early on the previous invalid entry
                'github_username': 'rayman',
            },
        )
    # Only one warning (combined message) should be emitted
    assert len(record) == 1
    warning_msg = str(record[0].message)
    assert 'orientation' in warning_msg
    # Valid entries before AND after the invalid one should be applied
    assert generated['choices_template']['project_name'] == 'Kivy Project'
    assert generated['choices_template']['github_username'] == 'rayman'
