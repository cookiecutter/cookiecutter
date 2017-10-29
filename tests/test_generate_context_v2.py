# -*- coding: utf-8 -*-

"""
test_generate_convext_v2
------------------------

Tests associated with processing v2 context syntax in the
`cookiecutter.generate` module.
"""

from __future__ import unicode_literals
import pytest

from collections import OrderedDict

from cookiecutter import generate


def context_data():
    context = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json'
        },
        {
            "test": OrderedDict([
                ("name", "cookiecutter-pytest-plugin"),
                ("cookiecutter_version", "2.0.0"),
                ("variables", [
                    OrderedDict([
                        ("name", "full_name"),
                        ("default", "J. Paul Getty"),
                        ("prompt", "What's your full name?"),
                        ("description", "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition."),
                        ("type", "string")]),
                    OrderedDict([
                        ("name", "email"),
                        ("default", "jpg@rich.de"),
                        ("prompt", "What's your email?"),
                        ("description", "Please enter an email address for the meta information in setup.py."),
                        ("type", "string")]),
                ])
            ])
        }
    )

    context_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'full_name': 'James Patrick Morgan'}
        },
        {
            "test": OrderedDict([
                ("name", "cookiecutter-pytest-plugin"),
                ("cookiecutter_version", "2.0.0"),
                ("variables", [
                    OrderedDict([
                        ("name", "full_name"),
                        ("default", "James Patrick Morgan"),
                        ("prompt", "What's your full name?"),
                        ("description", "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition."),
                        ("type", "string")]),
                    OrderedDict([
                        ("name", "email"),
                        ("default", "jpg@rich.de"),
                        ("prompt", "What's your email?"),
                        ("description", "Please enter an email address for the meta information in setup.py."),
                        ("type", "string")]),
                ])
            ])
        }
    )

    context_with_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'extra_context': {'email': 'jpm@chase.bk'}
        },
        {
            "test": OrderedDict([
                ("name", "cookiecutter-pytest-plugin"),
                ("cookiecutter_version", "2.0.0"),
                ("variables", [
                    OrderedDict([
                        ("name", "full_name"),
                        ("default", "J. Paul Getty"),
                        ("prompt", "What's your full name?"),
                        ("description", "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition."),
                        ("type", "string")]),
                    OrderedDict([
                        ("name", "email"),
                        ("default", "jpm@chase.bk"),
                        ("prompt", "What's your email?"),
                        ("description", "Please enter an email address for the meta information in setup.py."),
                        ("type", "string")]),
                ])
            ])
        }
    )

    context_with_default_and_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'full_name': 'Alpha Gamma Five'},
            'extra_context': {'email': 'agamma5@universe.open'}
        },
        {
            "test": OrderedDict([
                ("name", "cookiecutter-pytest-plugin"),
                ("cookiecutter_version", "2.0.0"),
                ("variables", [
                    OrderedDict([
                        ("name", "full_name"),
                        ("default", "Alpha Gamma Five"),
                        ("prompt", "What's your full name?"),
                        ("description", "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition."),
                        ("type", "string")]),
                    OrderedDict([
                        ("name", "email"),
                        ("default", "agamma5@universe.open"),
                        ("prompt", "What's your email?"),
                        ("description", "Please enter an email address for the meta information in setup.py."),
                        ("type", "string")]),
                ])
            ])
        }
    )

    context_choices_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
        },
        {
            "test_choices": OrderedDict([
                ("name", "cookiecutter-pytest-plugin"),
                ("cookiecutter_version", "2.0.0"),
                ("variables", [
                    OrderedDict([
                        ("name", "license"),
                        ("default", "Apache2"),
                        ("choices", ["Apache2", "MIT", "BSD3", "GNU-GPL3", "Mozilla2"]),
                    ])]
                 )
            ])
        }
    )

    context_choices_with_default_not_in_choices = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'orientation': 'landscape'},
        },
        {
            "test": OrderedDict([
                ("name", "cookiecutter-pytest-plugin"),
                ("cookiecutter_version", "2.0.0"),
                ("variables", [
                    OrderedDict([
                        ("name", "full_name"),
                        ("default", "J. Paul Getty"),
                        ("prompt", "What's your full name?"),
                        ("description", "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition."),
                        ("type", "string")]),
                    OrderedDict([
                        ("name", "email"),
                        ("default", "jpg@rich.de"),
                        ("prompt", "What's your email?"),
                        ("description", "Please enter an email address for the meta information in setup.py."),
                        ("type", "string")]),
                ])
            ])
        }
    )
    yield context
    yield context_with_default
    yield context_with_extra
    yield context_with_default_and_extra
    yield context_choices_with_default
    yield context_choices_with_default_not_in_choices


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data())
def test_generate_context(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    assert generate.generate_context(**input_params) == expected_context
