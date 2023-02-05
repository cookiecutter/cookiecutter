# -*- coding: utf-8 -*-
# flake8: noqa
"""
test_generate_convext_v2
------------------------

Tests associated with processing v2 context syntax in the
`cookiecutter.generate` module.
"""

from __future__ import unicode_literals

from collections import OrderedDict
from copy import deepcopy

import pytest

from cookiecutter import generate

# writing explicitely the expected outcomes of different tests
expected_file1_v0 = OrderedDict(
    [
        ("version", "2.0"),
        ("requires", OrderedDict([("cookiecutter", ">1")])),
        (
            "template",
            OrderedDict(
                [
                    ("name", "cookiecutter-pytest-plugin"),
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
                                        "Please enter your full name. It will be displayed on "
                                        "the README file and used for the PyPI package definition.",
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
                                        "Please enter an email address for "
                                        "the meta information in setup.py.",
                                    ),
                                    ("type", "string"),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
        ),
    ]
)

expected_file1_v1 = deepcopy(expected_file1_v0)
expected_file1_v1['template']['variables'][0]['default'] = 'James Patrick Morgan'

expected_file1_v2 = deepcopy(expected_file1_v0)
expected_file1_v2['template']['variables'][1]['default'] = 'jpm@chase.bk'

expected_file1_v3 = deepcopy(expected_file1_v0)
expected_file1_v3['template']['variables'][0]['default'] = 'Alpha Gamma Five'
expected_file1_v3['template']['variables'][1]['default'] = 'agamma5@universe.open'

expected_file1_v4 = deepcopy(expected_file1_v0)
expected_file1_v4['template']['variables'][1]['name'] = 'email'
expected_file1_v4['template']['variables'][1]['default'] = 'miles.davis@jazz.gone'
expected_file1_v4['template']['variables'][1]['description'] = 'Enter jazzy email...'

expected_file2_v0 = OrderedDict(
    [
        ("version", "2.0"),
        (
            "template",
            OrderedDict(
                [
                    ("name", "cc-representative"),
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
                                        "The default director is not proud of their work, "
                                        "we hope you are.",
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
            ),
        ),
    ]
)

expected_file2_v1 = deepcopy(expected_file2_v0)
expected_file2_v1['template']['variables'][0]['name'] = 'producer_credit'
expected_file2_v1['template']['variables'][0][
    'prompt'
] = 'Is there a producer credit on this film?'
expected_file2_v1['template']['variables'][0][
    'description'
] = 'There are usually a lot of producers...'
del expected_file2_v1['template']['variables'][1]['skip_if']

expected_file2_v2 = deepcopy(expected_file2_v0)
expected_file2_v2['template']['variables'][0]['name'] = 'producer_credits'
expected_file2_v2['template']['variables'][0]['default'] = 2
expected_file2_v2['template']['variables'][0][
    'prompt'
] = 'How many producers does this film have?'
expected_file2_v2['template']['variables'][0][
    'description'
] = 'There are usually a lot of producers...'
expected_file2_v2['template']['variables'][0]['type'] = 'int'
expected_file2_v2['template']['variables'][1][
    'skip_if'
] = '{{cookiecutter.producer_credits == False}}'

expected_file2_v3 = deepcopy(expected_file2_v0)
expected_file2_v3['template']['variables'][1]['default'] = "Allan Smithe"
expected_file2_v3['template']['variables'][1]['choices'] = [
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
    'John Ford',
    'Billy Wilder',
]

expected_file2_v4 = deepcopy(expected_file2_v0)
expected_file2_v4['template']['variables'][1]['default'] = "John Ford"
expected_file2_v4['template']['variables'][1]['choices'] = [
    'John Ford',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
    'Billy Wilder',
]

expected_file2_v5 = deepcopy(expected_file2_v0)
expected_file2_v5['template']['variables'][1]['default'] = 'John Ford'
expected_file2_v5['template']['variables'][1]['choices'] = [
    'John Ford',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
]

expected_file2_v6 = deepcopy(expected_file2_v0)
expected_file2_v6['template']['variables'][1]['default'] = "Billy Wilder"
expected_file2_v6['template']['variables'][1]['choices'] = [
    'Billy Wilder',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
    'John Ford',
]

expected_file2_v7 = deepcopy(expected_file2_v0)
expected_file2_v7['template']['variables'][1]['default'] = "Peter Sellers"
expected_file2_v7['template']['variables'][1]['choices'] = [
    'Peter Sellers',
    'Allan Smithe',
    'Ridley Scott',
    'Victor Fleming',
    'John Houston',
]


def context_data_serializer():
    """
    Creates a generator of combination:
        ((input file, additional params), expected output)
    """
    context = (
        {'context_file': 'tests/test-generate-context-v2/test.json'},
        {"test": expected_file1_v0},
    )

    context_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {
                'full_name': 'James Patrick Morgan',
                'this_key_ignored': 'not_in_context',
            },
        },
        {"test": expected_file1_v1},
    )

    context_with_extra = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'extra_context': {'email': 'jpm@chase.bk'},
        },
        {"test": expected_file1_v2},
    )

    context_choices_with_default = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
        },
        {
            "test_choices": OrderedDict(
                [
                    ("version", "2.0"),
                    (
                        "template",
                        OrderedDict(
                            [
                                ("name", "cookiecutter-pytest-plugin"),
                                (
                                    "variables",
                                    [
                                        OrderedDict(
                                            [
                                                ("name", "license"),
                                                ("type", "string"),
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
                        ),
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
        {"test": expected_file1_v3},
    )

    context_choices_with_default_not_in_choices = (
        {
            'context_file': 'tests/test-generate-context-v2/test.json',
            'default_context': {'orientation': 'landscape'},
        },
        {"test": expected_file1_v0},
    )
    yield context
    yield context_with_default
    yield context_with_extra
    yield context_with_default_and_extra
    yield context_choices_with_default
    yield context_choices_with_default_not_in_choices


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data_serializer())
def test_generate_context(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    assert generate.generate_context(**input_params) == expected_context


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

    yield context_choices_with_default
    yield context_choices_with_extra


@pytest.mark.usefixtures('clean_system')
@pytest.mark.parametrize('input_params, expected_context', context_data_misses())
def test_generate_context_misses(input_params, expected_context):
    """
    Test the generated context for several input parameters against the
    according expected context.
    """
    generated_context = generate.generate_context(**input_params)
    assert generated_context == expected_context


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
        True,
    )
    context_choices_with_extra_value_error = (
        {
            'context_file': 'tests/test-generate-context-v2/test_choices.json',
            'default_context': {'license': 'Apache2'},
            'extra_context': [{'name': 'license', 'default': 'MIT'}],
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
    yield context_choices_with_default_value_error
    yield context_choices_with_extra_value_error


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

    msg = "Extra context must be a dictionary or a list of dictionaries"
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
