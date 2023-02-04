# -*- coding: utf-8 -*-
# flake8: noqa
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
        {'context_file': 'tests/test-generate-context-v2/test.json'},
        {
            "test": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "J. Paul Getty"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "jpg@rich.de"),
                                    ("prompt", "What's your email?"),
                                    (
                                        "description",
                                        "Please enter an email address for the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    context_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {
                'full_name': 'James Patrick Morgan',
                'this_key_ignored': 'not_in_context',
            },
        },
        {
            "test": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "James Patrick Morgan"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "jpg@rich.de"),
                                    ("prompt", "What's your email?"),
                                    (
                                        "description",
                                        "Please enter an email address for the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    context_with_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'extra_context': {'email': 'jpm@chase.bk'},
        },
        {
            "test": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "J. Paul Getty"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "jpm@chase.bk"),
                                    ("prompt", "What's your email?"),
                                    (
                                        "description",
                                        "Please enter an email address for the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    context_with_default_and_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'full_name': 'Alpha Gamma Five'},
            'extra_context': {'email': 'agamma5@universe.open'},
        },
        {
            "test": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "Alpha Gamma Five"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "agamma5@universe.open"),
                                    ("prompt", "What's your email?"),
                                    (
                                        "description",
                                        "Please enter an email address for the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    context_choices_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
        },
        {
            "test_choices": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "license"),
                                    ("default", "Apache2"),
                                    (
                                        "choices",
                                        [
                                            "Apache2",
                                            "MIT",
                                            "BSD3",
                                            "GNU-GPL3",
                                            "Mozilla2",
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            )
        },
    )

    context_choices_with_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
            'extra_context': {'license': 'MIT'},
        },
        {
            "test_choices": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "license"),
                                    ("default", "MIT"),
                                    (
                                        "choices",
                                        [
                                            "MIT",
                                            "Apache2",
                                            "BSD3",
                                            "GNU-GPL3",
                                            "Mozilla2",
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            )
        },
    )

    context_choices_with_default_not_in_choices = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'orientation': 'landscape'},
        },
        {
            "test": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "J. Paul Getty"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "jpg@rich.de"),
                                    ("prompt", "What's your email?"),
                                    (
                                        "description",
                                        "Please enter an email address for the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    yield context
    yield context_with_default
    yield context_with_extra
    yield context_with_default_and_extra
    yield context_choices_with_default
    yield context_choices_with_extra
    yield context_choices_with_default_not_in_choices


def context_data_misses():
    context_choices_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices-miss.json',
            'default_context': {'license': 'Cherokee'},
        },
        {
            "test_choices-miss": OrderedDict(
                [
                    ("name", "test_choices-miss"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "license"),
                                    ("default", "Apache2"),
                                    (
                                        "choices",
                                        [
                                            "MIT",
                                            "BSD3",
                                            "GNU-GPL3",
                                            "Apache2",
                                            "Mozilla2",
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            )
        },
    )

    context_choices_with_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices-miss.json',
            'extra_context': {'license': 'MIT'},
        },
        {
            "test_choices-miss": OrderedDict(
                [
                    ("name", "test_choices-miss"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "license"),
                                    ("default", "MIT"),
                                    (
                                        "choices",
                                        [
                                            "MIT",
                                            "BSD3",
                                            "GNU-GPL3",
                                            "Apache2",
                                            "Mozilla2",
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            )
        },
    )

    yield context_choices_with_default
    yield context_choices_with_extra


def context_data_value_errors():
    context_choices_with_default_value_error = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': [{'license': 'MIT'}],
        },
        {
            "test_choices": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "license"),
                                    ("default", "MIT"),
                                    (
                                        "choices",
                                        [
                                            "MIT",
                                            "Apache2",
                                            "BSD3",
                                            "GNU-GPL3",
                                            "Mozilla2",
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            )
        },
        False,
    )
    context_choices_with_extra_value_error = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
            'extra_context': [{'license': 'MIT'}],
        },
        {
            "test_choices": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "license"),
                                    ("default", "MIT"),
                                    (
                                        "choices",
                                        [
                                            "MIT",
                                            "Apache2",
                                            "BSD3",
                                            "GNU-GPL3",
                                            "Mozilla2",
                                        ],
                                    ),
                                ]
                            )
                        ],
                    ),
                ]
            )
        },
        True,
    )
    yield context_choices_with_default_value_error
    yield context_choices_with_extra_value_error


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data())
def test_generate_context(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    generated_context = generate.generate_context(**input_params)
    assert generated_context == expected_context


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data_misses())
def test_generate_context_misses(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    generated_context = generate.generate_context(**input_params)
    assert generated_context == expected_context


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize(
    'input_params, expected_context, raise_exception', context_data_value_errors()
)
def test_generate_context_value_error(input_params, expected_context, raise_exception):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    if raise_exception:
        with pytest.raises(ValueError) as excinfo:
            generate.generate_context(**input_params)
    else:
        generate.generate_context(**input_params)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_invalid():
    """
    Test error condition when extra context is not a dictionary or a list
    of dictionaries.
    """

    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context='should_be_a_list_or_a_dictionary',
        )

    msg = "Extra context must be a dictionary or a list of dictionaries!"
    assert msg in str(excinfo.value)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_list_item_not_dict():
    """
    Test error condition when extra context is a list, but not a list that
    contains a dictionary.
    """
    xtra_context = ['a_string', 'here_too']
    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context=xtra_context,
        )

    msg = "Extra context list item 'a_string' is of type str, should be a dictionary."
    assert msg in str(excinfo.value)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_list_item_dict_missing_name_field():
    """
    Test error condition when extra context is a list, but not a list that
    contains a dictionary.
    """
    xtra_context = [
        {
            "shouldbename": "author_name",
            "default": "Robert Lewis",
            "prompt": "What's the author's name?",
            "description": "Please enter the author's full name.",
            "type": "string",
        }
    ]
    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context=xtra_context,
        )

    msg = "is missing a 'name' key."
    assert msg in str(excinfo.value)


@pytest.mark.usefixtures('clean_system')
def test_generate_context_extra_ctx_list_item_dict_no_name_field_match():
    """
    Test error condition when extra context is a list, but not a list that
    contains a dictionary.
    """
    xtra_context = [
        {
            "name": "author_name",
            "default": "Robert Lewis",
            "prompt": "What's the author's name?",
            "description": "Please enter the author's full name.",
            "type": "string",
        }
    ]
    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/test.json',
            default_context=None,
            extra_context=xtra_context,
        )

    msg = "No variable found in context whose name matches extra context name 'author_name'"
    assert msg in str(excinfo.value)


def gen_context_data_inputs_expected():
    # Extra field ignored
    context_with_valid_extra_0 = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'extra_context': [
                {
                    'name': 'email',
                    'default': 'miles.davis@jazz.gone',
                    'description': 'Enter jazzy email...',
                    'extra_field': 'extra_field_value',
                }
            ],
        },
        {
            "test": OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "full_name"),
                                    ("default", "J. Paul Getty"),
                                    ("prompt", "What's your full name?"),
                                    (
                                        "description",
                                        "Please enter your full name. It will be displayed on the README file and used for the PyPI package definition.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "email"),
                                    ("default", "miles.davis@jazz.gone"),
                                    ("prompt", "What's your email?"),
                                    ("description", "Enter jazzy email..."),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Empty extra context precipitates no ill effect
    context_with_valid_extra_1 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': []
            # 'extra_context': [
            #     {
            #         'name': 'email',
            #         'default': 'miles.davis@jazz.gone',
            #         'description': 'Enter jazzy email...',
            #         'extra_field': 'extra_field_value',
            #     }
            # ]
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    # Test the ability to change the variable's name field (since it is used
    # to identify the variable to be modifed) with extra context and to remove
    # a key from the context via the removal token: '<<REMOVE::FIELD>>'
    context_with_valid_extra_2 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative-director.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credit',
                    'prompt': 'Is there a producer credit on this film?',
                    'description': 'There are usually a lot of producers...',
                },
                {
                    'name': 'director_name',
                    'skip_if': '<<REMOVE::FIELD>>',
                },
            ],
        },
        {
            "representative-director": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "producer_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a producer credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "There are usually a lot of producers...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_exists"),
                                    ("default", False),
                                    ("prompt", "Is there a Director?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The director exists.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            True,
                                            False,
                                        ],
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test the ability to change the variable's name field (since it is used
    # to identify the variable to be modifed) with extra context and to also
    # test that any other references in other variables that might use the
    # original variable name get updated as well.
    context_with_valid_extra_2_B = (
        {
            'context_file': 'tests/test-generate-context-v2/representative_2B.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credit',
                    'prompt': 'Is there a producer credit on this film?',
                    'description': 'There are usually a lot of producers...',
                },
            ],
        },
        {
            "representative_2B": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "producer_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a producer credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "There are usually a lot of producers...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                            "{{cookiecutter.producer_credit}}",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.producer_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    # Test changing variable's name field value, default field, prompt field,
    # and changing the type
    context_with_valid_extra_3 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credits',
                    'default': 2,
                    'prompt': 'How many producers does this film have?',
                    'description': 'There are usually a lot of producers...',
                    'type': "int",
                }
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "producer_credits"),
                                    ("default", 2),
                                    (
                                        "prompt",
                                        "How many producers does this film have?",
                                    ),
                                    (
                                        "description",
                                        "There are usually a lot of producers...",
                                    ),
                                    ("type", "int"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.producer_credits == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test changing choices field without changing the default, but default
    # does not change because the first position in choices matches default
    context_with_valid_extra_4 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'choices': [
                        'Allan Smithe',
                        'Ridley Scott',
                        'Victor Fleming',
                        'John Houston',
                        'John Ford',
                        'Billy Wilder',
                    ],
                }
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            'Allan Smithe',
                                            'Ridley Scott',
                                            'Victor Fleming',
                                            'John Houston',
                                            'John Ford',
                                            'Billy Wilder',
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test changing choices field and changing the default
    context_with_valid_extra_5 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'default': 'John Ford',
                    'choices': [
                        'Allan Smithe',
                        'Ridley Scott',
                        'Victor Fleming',
                        'John Houston',
                        'John Ford',
                        'Billy Wilder',
                    ],
                }
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "John Ford"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            'John Ford',
                                            'Allan Smithe',
                                            'Ridley Scott',
                                            'Victor Fleming',
                                            'John Houston',
                                            'Billy Wilder',
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test changing the default, but not the choices field, yet seeing choices field re-ordered
    # to put default value in first location
    context_with_valid_extra_6 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'default': 'John Ford',
                }
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "John Ford"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            'John Ford',
                                            'Allan Smithe',
                                            'Ridley Scott',
                                            'Victor Fleming',
                                            'John Houston',
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test changing choices field without changing the default, but default
    # does get changee because the first position in choices field chagned
    context_with_valid_extra_7 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'choices': [
                        'Billy Wilder',
                        'Allan Smithe',
                        'Ridley Scott',
                        'Victor Fleming',
                        'John Houston',
                        'John Ford',
                    ],
                }
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Billy Wilder"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            'Billy Wilder',
                                            'Allan Smithe',
                                            'Ridley Scott',
                                            'Victor Fleming',
                                            'John Houston',
                                            'John Ford',
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test changing the default value with a value that is not in choices,
    # we should see the choice first position get updated.
    context_with_valid_extra_8 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_name',
                    'default': 'Peter Sellers',
                }
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Peter Sellers"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Peter Sellers",
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.director_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    yield context_with_valid_extra_0
    yield context_with_valid_extra_1
    yield context_with_valid_extra_2
    yield context_with_valid_extra_2_B
    yield context_with_valid_extra_3
    yield context_with_valid_extra_4
    yield context_with_valid_extra_5
    yield context_with_valid_extra_6
    yield context_with_valid_extra_7
    yield context_with_valid_extra_8


def gen_context_data_inputs_expected_var():
    # Test the ability to change the variable's name field (since it is used
    # to identify the variable to be modifed) with extra context and to remove
    # a key from the context via the removal token: '<<REMOVE::FIELD>>'
    context_with_valid_extra_2 = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credit',
                    'prompt': 'Is there a producer credit on this film?',
                    'description': 'There are usually a lot of producers...',
                },
                {
                    'name': 'director_name',
                    'skip_if': '<<REMOVE::FIELD>>',
                },
            ],
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "producer_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a producer credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "There are usually a lot of producers...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )
    # Test the ability to change the variable's name field (since it is used
    # to identify the variable to be modifed) with extra context and to also
    # test that any other references in other variables that might use the
    # original variable name get updated as well.
    context_with_valid_extra_2_B = (
        {
            'context_file': 'tests/test-generate-context-v2/representative_2B.json',
            'extra_context': [
                {
                    'name': 'director_credit::producer_credit',
                    'prompt': 'Is there a producer credit on this film?',
                    'description': 'There are usually a lot of producers...',
                },
            ],
        },
        {
            "representative_2B": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "producer_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a producer credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "There are usually a lot of producers...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                            "{{cookiecutter.producer_credit}}",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    (
                                        "skip_if",
                                        "{{cookiecutter.producer_credit == False}}",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )

    yield context_with_valid_extra_2
    yield context_with_valid_extra_2_B


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize(
    'input_params, expected_context', gen_context_data_inputs_expected()
)
def test_generate_context_with_extra_context_dictionary(
    input_params, expected_context, monkeypatch
):
    """
    Test the generated context with extra content overwrite to multiple fields,
    with creation of new fields NOT allowed.
    """
    assert generate.generate_context(**input_params) == expected_context


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize(
    'input_params, expected_context', gen_context_data_inputs_expected_var()
)
def test_generate_context_with_extra_context_dictionary_var(
    input_params, expected_context, monkeypatch
):
    """
    Test the generated context with extra content overwrite to multiple fields,
    with creation of new fields NOT allowed.
    """
    assert generate.generate_context(**input_params) == expected_context


def context_data_2():
    context_with_valid_extra_2_A = (
        {
            'context_file': 'tests/test-generate-context-v2/representative.json',
        },
        {
            "representative": OrderedDict(
                [
                    ("name", "cc-representative"),
                    ("cookiecutter_version", "2.0.0"),
                    (
                        "variables",
                        [
                            OrderedDict(
                                [
                                    ("name", "director_credit"),
                                    ("default", True),
                                    (
                                        "prompt",
                                        "Is there a director credit on this film?",
                                    ),
                                    (
                                        "description",
                                        "Directors take credit for most of their films, usually...",
                                    ),
                                    ("type", "boolean"),
                                ]
                            ),
                            OrderedDict(
                                [
                                    ("name", "director_name"),
                                    ("default", "Allan Smithe"),
                                    ("prompt", "What's the Director's full name?"),
                                    ("prompt_user", True),
                                    (
                                        "description",
                                        "The default director is not proud of their work, we hope you are.",
                                    ),
                                    ("hide_input", False),
                                    (
                                        "choices",
                                        [
                                            "Allan Smithe",
                                            "Ridley Scott",
                                            "Victor Fleming",
                                            "John Houston",
                                        ],
                                    ),
                                    ("validation", "^[a-z][A-Z]+$"),
                                    ("validation_flags", ["verbose", "ascii"]),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            )
        },
    )


@pytest.mark.usefixtures('clean_system')
def test_raise_exception_when_attempting_to_remove_mandatory_field():
    """
    Test that ValueError is raised if attempt is made to remove a mandatory
    field -- the default field.
    The other mandatory field, name, cannot be removed because it has to be
    used to specify which variable to remove.
    """
    xtra_context = [
        {
            'name': 'director_name',
            'default': '<<REMOVE::FIELD>>',
        },
    ]

    with pytest.raises(ValueError) as excinfo:
        generate.generate_context(
            context_file='tests/test-generate-context-v2/representative.json',
            default_context=None,
            extra_context=xtra_context,
        )

    assert "Cannot remove mandatory 'default' field" in str(excinfo.value)
